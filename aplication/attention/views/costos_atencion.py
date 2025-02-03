from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from aplication.attention.models import CostosAtencion, CostoAtencionDetalle
from aplication.attention.forms.costos_atencion import CostosAtencionForm, CostoAtencionDetalleForm
from doctor.utils import save_audit  # Suponiendo que tienes este método para auditoría


# Listar CostosAtencion
class CostosAtencionListView(ListView):
    model = CostosAtencion
    template_name = "attention/costos_atencion/list.html"
    context_object_name = 'costos'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.all().order_by('-fecha_pago')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Gestión de Costos de Atención"
        context['title1'] = "Lista de Costos de Atención"
        return context


# Crear CostosAtencion
class CostosAtencionCreateView(CreateView):
    model = CostosAtencion
    template_name = "attention/costos_atencion/form.html"
    form_class = CostosAtencionForm
    success_url = reverse_lazy('attention:costos_atencion_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Gestión de Costos de Atención"
        context['title1'] = "Agregar Nuevo Costo"
        context['grabar'] = "Guardar Costo"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, action='A')  # Auditoría
        messages.success(self.request, f"Éxito al crear el costo: {self.object.total}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))


# Editar CostosAtencion
class CostosAtencionUpdateView(UpdateView):
    model = CostosAtencion
    template_name = "attention/costos_atencion_form.html"
    form_class = CostosAtencionForm
    success_url = reverse_lazy('attention:costos_atencion_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Gestión de Costos de Atención"
        context['title1'] = "Editar Costo"
        context['grabar'] = "Actualizar Costo"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, action='M')  # Auditoría
        messages.success(self.request, f"Éxito al actualizar el costo: {self.object.total}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))


# Eliminar CostosAtencion
class CostosAtencionDeleteView(DeleteView):
    model = CostosAtencion
    success_url = reverse_lazy('attention:costos_atencion_list')
    template_name = "costos_atencion/costos_atencion_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Gestión de Costos de Atención"
        context['description'] = f"¿Desea eliminar el costo de {self.object.total}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, f"Éxito al eliminar el costo: {self.object.total}.")
        return super().delete(request, *args, **kwargs)


# Detalle de CostosAtencion (para respuestas JSON)
class CostosAtencionDetailView(DetailView):
    model = CostosAtencion

    def get(self, request, *args, **kwargs):
        costo = self.get_object()
        data = {
            'id': costo.id,
            'atencion': str(costo.atencion),
            'total': costo.total,
            'fecha_pago': costo.fecha_pago,
            'activo': costo.activo,
        }
        return JsonResponse(data)
