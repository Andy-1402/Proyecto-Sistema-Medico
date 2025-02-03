from django import forms
from django.forms import ModelForm, ValidationError
from aplication.core.models import Doctor, Especialidad  # Asegúrate de importar los modelos adecuados

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = [
            "nombres", "apellidos", "cedula", "fecha_nacimiento", "direccion", 
            "latitud", "longitud", "codigoUnicoDoctor", "especialidad", 
            "telefonos", "email", "horario_atencion", "duracion_cita", 
            "curriculum", "firmaDigital", "foto", "imagen_receta", "activo"
        ]
        
        # Personalización de los widgets para los campos del formulario HTML
        widgets = {
            "nombres": forms.TextInput(
                attrs={
                    "placeholder": "Nombre(s) del doctor",
                    "class": "form-control",
                }
            ),
            "apellidos": forms.TextInput(
                attrs={
                    "placeholder": "Apellido(s) del doctor",
                    "class": "form-control",
                }
            ),
            "cedula": forms.TextInput(
                attrs={
                    "placeholder": "Cédula de identidad",
                    "class": "form-control",
                }
            ),
            "fecha_nacimiento": forms.DateInput(
                attrs={
                    "placeholder": "Fecha de nacimiento",
                    "class": "form-control",
                    "type": "date"
                }
            ),
            "direccion": forms.TextInput(
                attrs={
                    "placeholder": "Dirección del trabajo",
                    "class": "form-control",
                }
            ),
            "latitud": forms.NumberInput(
                attrs={
                    "placeholder": "Latitud",
                    "class": "form-control",
                    "step": "any"
                }
            ),
            "longitud": forms.NumberInput(
                attrs={
                    "placeholder": "Longitud",
                    "class": "form-control",
                    "step": "any"
                }
            ),
            "codigoUnicoDoctor": forms.TextInput(
                attrs={
                    "placeholder": "Código único del doctor",
                    "class": "form-control",
                }
            ),
            "especialidad": forms.SelectMultiple(
                attrs={
                    "class": "form-control",
                }
            ),
            "telefonos": forms.TextInput(
                attrs={
                    "placeholder": "Número(s) de teléfono",
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Correo electrónico",
                    "class": "form-control",
                }
            ),
            "horario_atencion": forms.Textarea(
                attrs={
                    "placeholder": "Horario de atención",
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "duracion_cita": forms.NumberInput(
                attrs={
                    "placeholder": "Duración de la cita en minutos",
                    "class": "form-control",
                }
            ),
            "curriculum": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf,.doc,.docx,.txt",  # Especifica los tipos de archivo permitidos
                }
            ),
            "firmaDigital": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",  # Aceptar solo imágenes
                }
            ),
            "foto": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",  # Aceptar solo imágenes
                }
            ),
            "imagen_receta": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",  # Aceptar solo imágenes
                }
            ),
            "activo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    # Validación personalizada para los campos
    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula")
        if len(cedula) != 10:
            raise ValidationError("La cédula debe tener 10 dígitos.")
        return cedula

    def clean_telefono(self):
        telefonos = self.cleaned_data.get("telefonos")
        # Puedes agregar validaciones para los teléfonos si lo deseas
        return telefonos

    def clean_direccion(self):
        direccion = self.cleaned_data.get("direccion")
        # Si se requiere alguna validación adicional, puedes agregarla aquí
        return direccion.capitalize()

    def clean_horario_atencion(self):
        horario_atencion = self.cleaned_data.get("horario_atencion")
        # Puedes agregar validación para el horario si es necesario
        return horario_atencion

    def clean_duracion_cita(self):
        duracion_cita = self.cleaned_data.get("duracion_cita")
        if duracion_cita <= 0:
            raise ValidationError("La duración de la cita debe ser mayor a 0 minutos.")
        return duracion_cita

    def clean_email(self):
        email = self.cleaned_data.get("email")
       
        return email
