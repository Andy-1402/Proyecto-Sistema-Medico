from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.attention.forms.cita_medica import CitaMedicaForm
from aplication.attention.models import CitaMedica
from doctor.utils import save_audit

class CitaMedicaListView(ListView):
    model = CitaMedica
    template_name = "attention/cita_medica/list.html"
    context_object_name = 'citas'
    paginate_by = 10
    
    def get_queryset(self):
        return self.model.objects.select_related('paciente').all().order_by('fecha', 'hora_cita')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Gestión de Citas Médicas"
        context['title1'] = "Lista de Citas Médicas"
        return context

class CitaMedicaCreateView(CreateView):
    model = CitaMedica
    template_name = 'attention/cita_medica/form.html'
    form_class = CitaMedicaForm
    success_url = reverse_lazy('attention:cita_medica_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Citas Médicas"
        context['title1'] = 'Agregar Nueva Cita Médica'
        context['grabar'] = 'Guardar Cita'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        cita = self.object
        save_audit(self.request, cita, action='A')
        messages.success(self.request, f"Éxito al crear la cita médica para {cita.paciente}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class CitaMedicaUpdateView(UpdateView):
    model = CitaMedica
    template_name = 'attention/cita_medica/form.html'
    form_class = CitaMedicaForm
    success_url = reverse_lazy('attention:cita_medica_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Citas Médicas"
        context['title1'] = 'Editar Cita Médica'
        context['grabar'] = 'Actualizar Cita'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        cita = self.object
        save_audit(self.request, cita, action='M')
        messages.success(self.request, f"Éxito al actualizar la cita médica de {cita.paciente}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class CitaMedicaDeleteView(DeleteView):
    model = CitaMedica
    success_url = reverse_lazy('attention:cita_medica_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Citas Médicas"
        context['grabar'] = 'Eliminar Cita'
        context['description'] = f"¿Desea eliminar la cita de {self.object.paciente}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar la cita médica de {self.object.paciente}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class CitaMedicaDetailView(DetailView):
    model = CitaMedica
    
    
    def get(self, request, *args, **kwargs):
        cita = self.get_object()
        print(f"Paciente: {cita.paciente}, Tipo: {type(cita.paciente)}")
        data = {
            'id': cita.id,
            'paciente': cita.paciente.nombre_completo(),  # Asume que el modelo Paciente tiene un método para mostrar el nombre completo
            'fecha': cita.fecha,
            'hora_cita': cita.hora_cita,
            'estado': cita.get_estado_display(),  # Para mostrar la representación legible del estado
            # Añade más campos si es necesario
        }
        return JsonResponse(data)

