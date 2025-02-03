from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.attention.forms.examen_solicitado import ExamenSolicitadoForm
from aplication.attention.models import ExamenSolicitado
from doctor.utils import save_audit

class ExamenSolicitadoListView(ListView):
    model = ExamenSolicitado
    template_name = "attention/examen_solicitado/list.html"
    context_object_name = 'examenes'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.select_related('paciente').all().order_by('-fecha_solicitud')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Gestión de Exámenes Solicitados"
        context['title1'] = "Lista de Exámenes Solicitados"
        return context

class ExamenSolicitadoCreateView(CreateView):
    model = ExamenSolicitado
    template_name = 'attention/examen_solicitado/form.html'
    form_class = ExamenSolicitadoForm
    success_url = reverse_lazy('attention:examen_solicitado_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Exámenes Solicitados"
        context['title1'] = 'Agregar Nuevo Examen Solicitado'
        context['grabar'] = 'Guardar Examen'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        examen = self.object
        save_audit(self.request, examen, action='A')
        messages.success(self.request, f"Éxito al crear el examen solicitado para {examen.paciente}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class ExamenSolicitadoUpdateView(UpdateView):
    model = ExamenSolicitado
    template_name = 'attention/examen_solicitado/form.html'
    form_class = ExamenSolicitadoForm
    success_url = reverse_lazy('attention:examen_solicitado_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Exámenes Solicitados"
        context['title1'] = 'Editar Examen Solicitado'
        context['grabar'] = 'Actualizar Examen'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        examen = self.object
        save_audit(self.request, examen, action='M')
        messages.success(self.request, f"Éxito al actualizar el examen solicitado de {examen.paciente}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class ExamenSolicitadoDeleteView(DeleteView):
    model = ExamenSolicitado
    success_url = reverse_lazy('attention:examen_solicitado_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Exámenes Solicitados"
        context['grabar'] = 'Eliminar Examen'
        context['description'] = f"¿Desea eliminar el examen de {self.object.paciente}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar el examen solicitado de {self.object.paciente}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class ExamenSolicitadoDetailView(DetailView):
    model = ExamenSolicitado

    def get(self, request, *args, **kwargs):
        examen = self.get_object()
        data = {
            'id': examen.id,
            'nombre_examen': examen.nombre_examen,
            'paciente': examen.paciente.nombre_completo(),  # Asume que el modelo Paciente tiene un método para mostrar el nombre completo
            'fecha_solicitud': examen.fecha_solicitud,
            'resultado': examen.resultado.url if examen.resultado else None,
            'comentario': examen.comentario,
            'estado': examen.get_estado_display(),  # Para mostrar la representación legible del estado
            # Añade más campos si es necesario
        }
        return JsonResponse(data)
