from django.urls import reverse_lazy
from aplication.core.forms.doctor import DoctorForm  # Asegúrate de tener este formulario
from aplication.core.models import Doctor
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from doctor.utils import save_audit

# Vista para listar los doctores
class DoctorListView(LoginRequiredMixin, ListViewMixin, ListView):
    template_name = "core/doctor/list.html"
    model = Doctor
    context_object_name = 'doctores'
    paginate_by = 10

    def get_queryset(self):
        # Aquí podrías aplicar alguna lógica de filtrado si es necesario
        q1 = self.request.GET.get('q')
        if q1:
            return self.model.objects.filter(nombres__icontains=q1).order_by('nombres')
        return self.model.objects.all().order_by('nombres')

# Vista para crear un nuevo doctor
class DoctorCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
    model = Doctor
    template_name = 'core/doctor/form.html'
    form_class = DoctorForm
    success_url = reverse_lazy('core:doctor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Doctor'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        doctor = self.object
        save_audit(self.request, doctor, action='A')
        messages.success(self.request, f"Éxito al crear el doctor {doctor.nombres} {doctor.apellidos}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

# Vista para actualizar la información de un doctor
class DoctorUpdateView(LoginRequiredMixin, UpdateViewMixin, UpdateView):
    model = Doctor
    template_name = 'core/doctor/form.html'
    form_class = DoctorForm
    success_url = reverse_lazy('core:doctor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Doctor'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        doctor = self.object
        save_audit(self.request, doctor, action='M')
        messages.success(self.request, f"Éxito al modificar el doctor {doctor.nombres} {doctor.apellidos}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

# Vista para eliminar un doctor
class DoctorDeleteView(LoginRequiredMixin, DeleteViewMixin, DeleteView):
    model = Doctor
    success_url = reverse_lazy('core:doctor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Doctor'
        context['description'] = f"¿Desea eliminar al doctor {self.object.nombres} {self.object.apellidos}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente al doctor {self.object.nombres} {self.object.apellidos}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

# Vista para ver los detalles de un doctor (usando JsonResponse)
class DoctorDetailView(LoginRequiredMixin, DetailView):
    model = Doctor

    def get(self, request, *args, **kwargs):
        doctor = self.get_object()
        
        especialidades = [esp.nombre for esp in doctor.especialidad.all()]
        
        
        data = {
            'id': doctor.id,
            'nombres': doctor.nombres,
            'apellidos': doctor.apellidos,
            'cedula': doctor.cedula,
            'fecha_nacimiento': doctor.fecha_nacimiento,
            'direccion': doctor.direccion,
            'telefono': doctor.telefonos,
            'email': doctor.email,
            'especialidades': especialidades,
        }
        return JsonResponse(data)
