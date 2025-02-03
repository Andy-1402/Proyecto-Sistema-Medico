from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages

from aplication.core.forms.audit import AuditUserForm
from aplication.core.models import AuditUser
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from doctor.utils import save_audit

class AuditUserListView(PermissionRequiredMixin, LoginRequiredMixin, ListViewMixin, ListView):
    template_name = "core/audit_user/list.html"
    model = AuditUser
    permission_required = 'core.view_audituser'
    context_object_name = 'audits'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return self.model.objects.filter(tabla__icontains=query).order_by('-fecha', '-hora')
        return self.model.objects.all().order_by('-fecha', '-hora')

class AuditUserCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
    model = AuditUser
    template_name = 'core/audit_user/form.html'
    form_class = AuditUserForm
    success_url = reverse_lazy('core:audit_user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Registrar Auditoría'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, action='A')
        messages.success(self.request, f"Éxito al registrar auditoría en la tabla {self.object.tabla}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class AuditUserUpdateView(LoginRequiredMixin, UpdateViewMixin, UpdateView):
    model = AuditUser
    template_name = 'core/audit_user/form.html'
    form_class = AuditUserForm
    success_url = reverse_lazy('core:audit_user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Auditoría'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, action='M')
        messages.success(self.request, f"Éxito al modificar la auditoría en la tabla {self.object.tabla}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class AuditUserDeleteView(LoginRequiredMixin, DeleteViewMixin, DeleteView):
    model = AuditUser
    success_url = reverse_lazy('core:audit_user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Auditoría'
        context['description'] = f"¿Desea eliminar la auditoría en la tabla: {self.object.tabla}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, f"Éxito al eliminar la auditoría en la tabla {self.object.tabla}.")
        return super().delete(request, *args, **kwargs)

class AuditUserDetailView(LoginRequiredMixin, DetailView):
    model = AuditUser

    def get(self, request, *args, **kwargs):
        audit = self.get_object()
        data = {
            'id': audit.id,
            'usuario': audit.usuario.username if audit.usuario else "Usuario no asignado",
            'tabla': audit.tabla,
            'registroid': audit.registroid,
            'accion': audit.accion,
            'fecha': audit.fecha.isoformat(),
            'hora': audit.hora.isoformat(),
            'estacion': audit.estacion,
        }
        return JsonResponse(data)
