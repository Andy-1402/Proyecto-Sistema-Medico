from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from aplication.security.models import Perfil


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    tipo_usuario = forms.ChoiceField(choices=Perfil.TIPOS_USUARIO)
    telefono = forms.CharField(max_length=20, required=False)
    direccion = forms.CharField(widget=forms.Textarea, required=False)
    foto = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        perfil_data = {
            'tipo_usuario': self.cleaned_data['tipo_usuario'],
            'telefono': self.cleaned_data.get('telefono', ''),
            'direccion': self.cleaned_data.get('direccion', ''),
        }
        # Manejar archivo opcional de foto
        if self.cleaned_data.get('foto'):
            perfil_data['foto'] = self.cleaned_data['foto']

        Perfil.objects.create(user=user, **perfil_data)
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email
