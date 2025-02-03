# views.py
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import RegistroUsuarioForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from aplication.security.utils.email import enviar_email_resend
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView



class HomeView(TemplateView):
    template_name = "components/security_base.html" 

class RegistroView(CreateView):
    model = User
    form_class = RegistroUsuarioForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('security:login')

    def form_valid(self, form):
        # Guarda el usuario en la base de datos
        response = super().form_valid(form)

        # Aquí, self.object hace referencia al objeto 'User' recién guardado
        # Debe tener el correo electrónico correctamente disponible
        email = self.object.email  # Accede al email del usuario creado
        nombre_completo = self.object.get_full_name()  # Nombre completo del usuario
        tipo_usuario = self.object.perfil.get_tipo_usuario_display()  # Tipo de usuario del perfil

        # Crear el contenido del correo en HTML
        contenido_html = (
            f"<p>Hola <strong>{nombre_completo}</strong>,</p>"
            f"<p>Tu cuenta ha sido creada exitosamente.</p>"
            f"<p><strong>Usuario:</strong> {self.object.username}</p>"
            f"<p><strong>Tipo de usuario:</strong> {tipo_usuario}</p>"
            f"<p>¡Bienvenido al sistema!</p>"
        )

        # Llamada para enviar el correo
        enviar_email_resend(
            destinatarios=[email],
            asunto="Bienvenido al Sistema Médico",
            contenido_html=contenido_html,
        )

        return response



class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    


    def get_success_url(self):
        # Redirige al home por el momento
        return reverse_lazy('core:home') 
    
    
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        logout(request)  # Cierra la sesión del usuario
        return HttpResponseRedirect(reverse_lazy('security:login'))
    
    
    

class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = "registration/perfil.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Agregamos al contexto los datos del usuario
        context['usuario'] = user
        context['perfil'] = getattr(user, 'perfil', None)  # Asume que tienes un perfil relacionado al usuario
        context['telefono'] = getattr(user, 'telefono', None)
        context['direccion'] = getattr(user, 'direccion', None)
        return context
    
    
    
    
    
    



    








