from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.attention.forms.servicios_adicionales import ServiciosAdicionalesForm
from aplication.attention.models import ServiciosAdicionales
from doctor.utils import save_audit

class ServiciosAdicionalesListView(ListView):
    model = ServiciosAdicionales
    template_name = "attention/servicios_adicionales/list.html"
    context_object_name = 'servicios'
    paginate_by = 10  # Cambia según sea necesario

    def get_queryset(self):
        return self.model.objects.all().order_by('nombre_servicio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Gestión de Servicios Adicionales"
        context['title1'] = "Lista de Servicios Adicionales"
        return context

class ServiciosAdicionalesCreateView(CreateView):
    model = ServiciosAdicionales
    template_name = 'attention/servicios_adicionales/form.html'
    form_class = ServiciosAdicionalesForm
    success_url = reverse_lazy('attention:servicios_adicionales_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Servicios Adicionales"
        context['title1'] = 'Agregar Nuevo Servicio Adicional'
        context['grabar'] = 'Guardar Servicio'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        servicio = self.object
        save_audit(self.request, servicio, action='A')
        messages.success(self.request, f"Éxito al crear el servicio adicional: {servicio.nombre_servicio}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class ServiciosAdicionalesUpdateView(UpdateView):
    model = ServiciosAdicionales
    template_name = 'attention/servicios_adicionales/form.html'
    form_class = ServiciosAdicionalesForm
    success_url = reverse_lazy('attention:servicios_adicionales_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Servicios Adicionales"
        context['title1'] = 'Editar Servicio Adicional'
        context['grabar'] = 'Actualizar Servicio'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        servicio = self.object
        save_audit(self.request, servicio, action='M')
        messages.success(self.request, f"Éxito al actualizar el servicio adicional: {servicio.nombre_servicio}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class ServiciosAdicionalesDeleteView(DeleteView):
    model = ServiciosAdicionales
    success_url = reverse_lazy('attention:servicios_adicionales_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Servicios Adicionales"
        context['grabar'] = 'Eliminar Servicio'
        context['description'] = f"¿Desea eliminar el servicio adicional: {self.object.nombre_servicio}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar el servicio adicional: {self.object.nombre_servicio}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class ServiciosAdicionalesDetailView(DetailView):
    model = ServiciosAdicionales

    def get(self, request, *args, **kwargs):
        servicio = self.get_object()
        data = {
            'id': servicio.id,
            'nombre_servicio': servicio.nombre_servicio,
            'costo_servicio': servicio.costo_servicio,
            'descripcion': servicio.descripcion,
            'activo': servicio.activo,
        }
        return JsonResponse(data)
