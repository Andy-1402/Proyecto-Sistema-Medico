from django.urls import reverse_lazy
from aplication.core.forms.empleado import EmpleadoForm
from aplication.core.models import Empleado
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q

class EmpleadoListView(ListView):
    template_name = "core/empleado/empleado_list.html"
    model = Empleado
    context_object_name = 'empleados'
    paginate_by = 10

    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q')
        if q1:
            self.query.add(Q(nombres__icontains=q1), Q.OR)
            self.query.add(Q(apellidos__icontains=q1), Q.OR)
            self.query.add(Q(cedula__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('nombres')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Empleados"
        context['title1'] = "Consulta de Empleados"
        return context

class EmpleadoCreateView(CreateView):
    model = Empleado
    template_name = 'core/empleado/empleado_form.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('core:empleado_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'Crear Empleado'
        context['grabar'] = 'Grabar Empleado'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        empleado = self.object
        messages.success(self.request, f"Éxito al crear el empleado {empleado.nombres} {empleado.apellidos}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class EmpleadoUpdateView(UpdateView):
    model = Empleado
    template_name = 'core/empleado/empleado_form.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('core:empleado_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Empleado'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        empleado = self.object
        messages.success(self.request, f"Éxito al modificar el empleado {empleado.nombres} {empleado.apellidos}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class EmpleadoDeleteView(DeleteView):
    model = Empleado
    success_url = reverse_lazy('core:empleado_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Empleado'
        context['description'] = f"¿Desea eliminar al empleado: {self.object.nombres} {self.object.apellidos}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente al empleado {self.object.nombres} {self.object.apellidos}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class EmpleadoDetailView(DetailView):
    model = Empleado

    def get(self, request, *args, **kwargs):
        empleado = self.get_object()
        data = {
            'id': empleado.id,
            'nombres': empleado.nombres,
            'apellidos': empleado.apellidos,
            'cedula': empleado.cedula,
            'fecha_nacimiento': empleado.fecha_nacimiento,
            'cargo': empleado.cargo.nombre,
            'sueldo': empleado.sueldo,
            'direccion': empleado.direccion,
            'latitud': empleado.latitud,
            'longitud': empleado.longitud,
            'activo': empleado.activo,
        }
        return JsonResponse(data)
    

