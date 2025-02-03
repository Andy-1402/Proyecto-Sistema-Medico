from django.views.generic import TemplateView
from aplication.core.models import Paciente, Doctor, Empleado, Cargo, TipoSangre
from aplication.attention.models import Atencion,  CitaMedica, ExamenSolicitado, HorarioAtencion, ServiciosAdicionales
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {"title1": "SaludSync", "title2": "Sistema Medico"}
        
        
        user = self.request.user
        context["usuario"] = user
        context['perfil'] = getattr(user, 'perfil', None) 
        
        
        context["can_paci"] = Paciente.cantidad_pacientes()
        context["can_doc"] = Doctor.cantidad_doctores()
        context["can_emp"] = Empleado.cantidad_empleados()
        context["can_car"] = Cargo.cantidad_cargos()
        context["can_tip"] = TipoSangre.cantidad_sangre()
        context["can_cit"] = CitaMedica.cantidad_citas()
        
        
        
        return context
    
