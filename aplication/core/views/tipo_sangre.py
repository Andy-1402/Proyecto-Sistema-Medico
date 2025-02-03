from django.urls import reverse_lazy
from aplication.core.forms.tipo_sangre import TipoSangreForm  # Asegúrate de tener este formulario
from aplication.core.models import TipoSangre
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from doctor.utils import save_audit

class TipoSangreListView(PermissionRequiredMixin, LoginRequiredMixin, ListViewMixin, ListView):
    template_name = "core/tipo_sangre/list.html"
    model = TipoSangre
    permission_required = 'core.view_tiposangre'  # Permiso necesario
    context_object_name = 'tipos_sangre'
    paginate_by = 10

    def get_queryset(self):
        # Aquí podrías aplicar alguna lógica de filtrado si es necesario
        q1 = self.request.GET.get('q')
        if q1:
            return self.model.objects.filter(tipo__icontains=q1).order_by('tipo')
        return self.model.objects.all().order_by('tipo')

class TipoSangreCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
    model = TipoSangre
    template_name = 'core/tipo_sangre/form.html'
    form_class = TipoSangreForm
    success_url = reverse_lazy('core:tipo_sangre_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Tipo de Sangre'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_sangre = self.object
        save_audit(self.request, tipo_sangre, action='A')
        messages.success(self.request, f"Éxito al crear el tipo de sangre {tipo_sangre.tipo}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class TipoSangreUpdateView(LoginRequiredMixin, UpdateViewMixin, UpdateView):
    model = TipoSangre
    template_name = 'core/tipo_sangre/form.html'
    form_class = TipoSangreForm
    success_url = reverse_lazy('core:tipo_sangre_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Tipo de Sangre'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_sangre = self.object
        save_audit(self.request, tipo_sangre, action='M')
        messages.success(self.request, f"Éxito al modificar el tipo de sangre {tipo_sangre.tipo}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class TipoSangreDeleteView(LoginRequiredMixin, DeleteViewMixin, DeleteView):
    model = TipoSangre
    success_url = reverse_lazy('core:tipo_sangre_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Tipo de Sangre'
        context['description'] = f"¿Desea eliminar el tipo de sangre: {self.object.tipo}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente el tipo de sangre {self.object.tipo}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class TipoSangreDetailView(LoginRequiredMixin, DetailView):
    model = TipoSangre

    def get(self, request, *args, **kwargs):
        tipo_sangre = self.get_object()
        data = {
            'id': tipo_sangre.id,
            'tipo': tipo_sangre.tipo,
            'descripcion': tipo_sangre.descripcion,
        }
        return JsonResponse(data)
