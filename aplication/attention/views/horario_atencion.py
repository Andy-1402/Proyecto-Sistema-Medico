from django.urls import reverse_lazy
from aplication.attention.forms.horario_atencion import Horario_AtencionForm
from aplication.attention.models import HorarioAtencion
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from doctor.utils import save_audit

class HorarioAtencionListView(ListView):
    template_name = "attention/horario_atencion/list.html"
    model = HorarioAtencion
    context_object_name = 'horarios'
    paginate_by = 10
    
    def get_queryset(self):
        return self.model.objects.all().order_by('dia_semana')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Gestión de Horarios"
        context['title1'] = "Lista de Horarios de Atención"
        return context

class HorarioAtencionCreateView(CreateView):
    model = HorarioAtencion
    template_name = 'attention/horario_atencion/form.html'
    form_class = Horario_AtencionForm
    success_url = reverse_lazy('attention:horario_atencion_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Horarios"
        context['title1'] = 'Agregar Nuevo Horario'
        context['grabar'] = 'Guardar Horario'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        horario = self.object
        save_audit(self.request, horario, action='A')
        messages.success(self.request, f"Éxito al crear el horario de {horario.dia_semana}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class HorarioAtencionUpdateView(UpdateView):
    model = HorarioAtencion
    template_name = 'attention/horario_atencion/form.html'
    form_class = Horario_AtencionForm
    success_url = reverse_lazy('attention:horario_atencion_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Horarios"
        context['title1'] = 'Editar Horario de Atención'
        context['grabar'] = 'Actualizar Horario'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        horario = self.object
        save_audit(self.request, horario, action='M')
        messages.success(self.request, f"Éxito al actualizar el horario de {horario.dia_semana}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class HorarioAtencionDeleteView(DeleteView):
    model = HorarioAtencion
    success_url = reverse_lazy('attention:horario_atencion_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Horarios"
        context['grabar'] = 'Eliminar Horario'
        context['description'] = f"¿Desea eliminar el horario del día {self.object.dia_semana}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente el horario del día {self.object.dia_semana}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class HorarioAtencionDetailView(DetailView):
    model = HorarioAtencion
    
    def get(self, request, *args, **kwargs):
        horario = self.get_object()
        data = {
            'id': horario.id,
            'dia_semana': horario.dia_semana,
            'hora_inicio': horario.hora_inicio,
            'hora_fin': horario.hora_fin,
            'Intervalo_desde': horario.Intervalo_desde,
            'Intervalo_hasta': horario.Intervalo_hasta,
            'activo': horario.activo,
            # Añade más campos si es necesario
        }
        return JsonResponse(data)
