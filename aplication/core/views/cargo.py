from django.urls import reverse_lazy
from aplication.core.forms.cargo import CargoForm
from aplication.core.models import Cargo
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from doctor.utils import save_audit

class CargoListView(ListView):
    template_name = "core/cargo/cargo_list.html"
    model = Cargo
    context_object_name = 'cargos'
    paginate_by = 10
    
    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q')  # Búsqueda
  
        if q1:
            self.query.add(Q(nombre__icontains=q1), Q.OR)  # Filtra por nombre
            self.query.add(Q(descripcion__icontains=q1), Q.OR)  # Filtra por descripción
        
        return self.model.objects.filter(self.query).order_by('nombre')  # Ordenar por 'nombre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Cargos"  # Título de la página
        context['title1'] = "Consulta de Cargos"  # Subtítulo de la página
        return context

class CargoCreateView(CreateView):
    model = Cargo
    template_name = 'core/cargo/cargo_form.html'
    form_class = CargoForm
    success_url = reverse_lazy('core:cargo_list') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'Crear Cargo'  
        context['grabar'] = 'Grabar Cargo' 
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        cargo = self.object  
        save_audit(self.request, cargo, action='A')
        messages.success(self.request, f"Éxito al crear el cargo {cargo.nombre}.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class CargoUpdateView(UpdateView):
    model = Cargo
    template_name = 'core/cargo/cargo_form.html'
    form_class = CargoForm
    success_url = reverse_lazy('core:cargo_list') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Cargo' 
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        cargo = self.object  
        save_audit(self.request, cargo, action='M')
        messages.success(self.request, f"Éxito al modificar el cargo {cargo.nombre}.")  
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class CargoDeleteView(DeleteView):
    model = Cargo
    success_url = reverse_lazy('core:cargo_list')  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Cargo'  
        context['description'] = f"¿Desea eliminar el cargo: {self.object.nombre}? "  
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente el cargo {self.object.nombre}." 
        messages.success(self.request, success_message)
        # Aquí puedes manejar el estado de eliminado lógico si es necesario
        # self.object.deleted = True
        # self.object.save()
        return super().delete(request, *args, **kwargs)

class CargoDetailView(DetailView):
    model = Cargo
    
    def get(self, request, *args, **kwargs):
        cargo = self.get_object()
        data = {
            'id': cargo.id,
            'nombre': cargo.nombre,
            'descripcion': cargo.descripcion,
            'activo': cargo.activo,
        }
        return JsonResponse(data)
