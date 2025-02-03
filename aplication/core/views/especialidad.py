from django.urls import reverse_lazy
from aplication.core.forms.especialidad import EspecialidadForm  
from aplication.core.models import Especialidad
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from doctor.utils import save_audit

# Vista para listar especialidades
class EspecialidadListView(LoginRequiredMixin, ListViewMixin, ListView):
    template_name = "core/especialidad/list.html"
    model = Especialidad
    context_object_name = 'especialidades'
    paginate_by = 10

    def get_queryset(self):
        # Lógica para filtrar si es necesario
        q1 = self.request.GET.get('q')
        if q1:
            return self.model.objects.filter(nombre__icontains=q1).order_by('nombre')
        return self.model.objects.all().order_by('nombre')

# Vista para crear una nueva especialidad
class EspecialidadCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
    model = Especialidad
    template_name = 'core/especialidad/form.html'
    form_class = EspecialidadForm
    success_url = reverse_lazy('core:especialidad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Especialidad'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        especialidad = self.object
        save_audit(self.request, especialidad, action='A')  # Guarda auditoría de la creación
        messages.success(self.request, f"Éxito al crear la especialidad {especialidad.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

# Vista para actualizar una especialidad existente
class EspecialidadUpdateView(LoginRequiredMixin, UpdateViewMixin, UpdateView):
    model = Especialidad
    template_name = 'core/especialidad/form.html'
    form_class = EspecialidadForm
    success_url = reverse_lazy('core:especialidad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Especialidad'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        especialidad = self.object
        save_audit(self.request, especialidad, action='M')  # Guarda auditoría de la modificación
        messages.success(self.request, f"Éxito al modificar la especialidad {especialidad.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

# Vista para eliminar una especialidad
class EspecialidadDeleteView(LoginRequiredMixin, DeleteViewMixin, DeleteView):
    model = Especialidad
    success_url = reverse_lazy('core:especialidad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Especialidad'
        context['description'] = f"¿Desea eliminar la especialidad: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente la especialidad {self.object.nombre}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

# Vista para ver los detalles de una especialidad (JSON)
class EspecialidadDetailView(LoginRequiredMixin, DetailView):
    model = Especialidad

    def get(self, request, *args, **kwargs):
        especialidad = self.get_object()
        data = {
            'id': especialidad.id,
            'nombre': especialidad.nombre,
            'descripcion': especialidad.descripcion,
            'activo': especialidad.activo
        }
        return JsonResponse(data)
