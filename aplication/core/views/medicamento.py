from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.core.forms.medicamento import MedicamentoForm
from aplication.core.models import Medicamento
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from doctor.utils import save_audit

class MedicamentoListView(PermissionRequiredMixin, LoginRequiredMixin, ListViewMixin, ListView):
    template_name = "core/medicamento/list.html"
    model = Medicamento
    permission_required = 'core.view_medicamento'
    context_object_name = 'medicamentos'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return self.model.objects.filter(nombre__icontains=query).order_by('nombre')
        return self.model.objects.all().order_by('nombre')


class MedicamentoCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
    model = Medicamento
    template_name = 'core/medicamento/form.html'
    form_class = MedicamentoForm
    success_url = reverse_lazy('core:medicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        medicamento = self.object
        save_audit(self.request, medicamento, action='A')
        messages.success(self.request, f"Éxito al crear el medicamento {medicamento.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))


class MedicamentoUpdateView(LoginRequiredMixin, UpdateViewMixin, UpdateView):
    model = Medicamento
    template_name = 'core/medicamento/form.html'
    form_class = MedicamentoForm
    success_url = reverse_lazy('core:medicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        medicamento = self.object
        save_audit(self.request, medicamento, action='M')
        messages.success(self.request, f"Éxito al modificar el medicamento {medicamento.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))


class MedicamentoDeleteView(LoginRequiredMixin, DeleteViewMixin, DeleteView):
    model = Medicamento
    success_url = reverse_lazy('core:medicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Medicamento'
        context['description'] = f"¿Desea eliminar el medicamento: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente el medicamento {self.object.nombre}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)


class MedicamentoDetailView(LoginRequiredMixin, DetailView):
    model = Medicamento

    def get(self, request, *args, **kwargs):
        medicamento = self.get_object()
        data = {
            'id': medicamento.id,
            'nombre': medicamento.nombre,
            'descripcion': medicamento.descripcion,
            'concentracion': medicamento.concentracion,
            'cantidad': medicamento.cantidad,
            'precio': str(medicamento.precio),
            'tipo': medicamento.tipo.tipo if medicamento.tipo else None,
            'marca': medicamento.marca_medicamento.nombre if medicamento.marca_medicamento else None,
            'comercial': medicamento.comercial,
            'activo': medicamento.activo,
        }
        return JsonResponse(data)
