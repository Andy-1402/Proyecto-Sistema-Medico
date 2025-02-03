from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.core.forms.diagnostico import DiagnosticoForm
from aplication.core.models import Diagnostico
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from doctor.utils import save_audit

class DiagnosticoListView(PermissionRequiredMixin, LoginRequiredMixin, ListViewMixin, ListView):
    template_name = "core/diagnostico/list.html"
    model = Diagnostico
    permission_required = 'core.view_diagnostico'
    context_object_name = 'diagnostico'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return self.model.objects.filter(descripcion__icontains=query).order_by('codigo')
        return self.model.objects.all().order_by('codigo')


class DiagnosticoCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
    model = Diagnostico
    template_name = 'core/diagnostico/form.html'
    form_class = DiagnosticoForm
    success_url = reverse_lazy('core:diagnostico_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Diagnóstico'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        diagnostico = self.object
        save_audit(self.request, diagnostico, action='A')
        messages.success(self.request, f"Éxito al crear el diagnóstico {diagnostico.codigo}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))


class DiagnosticoUpdateView(LoginRequiredMixin, UpdateViewMixin, UpdateView):
    model = Diagnostico
    template_name = 'core/diagnostico/form.html'
    form_class = DiagnosticoForm
    success_url = reverse_lazy('core:diagnostico_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Diagnóstico'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        diagnostico = self.object
        save_audit(self.request, diagnostico, action='M')
        messages.success(self.request, f"Éxito al modificar el diagnóstico {diagnostico.codigo}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))


class DiagnosticoDeleteView(LoginRequiredMixin, DeleteViewMixin, DeleteView):
    model = Diagnostico
    success_url = reverse_lazy('core:diagnostico_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Diagnóstico'
        context['description'] = f"¿Desea eliminar el diagnóstico: {self.object.codigo}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente el diagnóstico {self.object.codigo}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)


class DiagnosticoDetailView(LoginRequiredMixin, DetailView):
    model = Diagnostico

    def get(self, request, *args, **kwargs):
        diagnostico = self.get_object()
        data = {
            'id': diagnostico.id,
            'codigo': diagnostico.codigo,
            'descripcion': diagnostico.descripcion,
            'datos_adicionales': diagnostico.datos_adicionales,
            'activo': diagnostico.activo,
        }
        return JsonResponse(data)
