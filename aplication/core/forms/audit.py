from django import forms
from django.forms import ModelForm, ValidationError
from aplication.core.models import AuditUser

class AuditUserForm(ModelForm):
    class Meta:
        model = AuditUser
        fields = ['usuario', 'tabla', 'registroid', 'accion', 'fecha', 'hora', 'estacion']
        
        widgets = {
            'usuario': forms.Select(
                attrs={
                    'id': 'id_usuario',
                    'class': 'form-control',
                }
            ),
            'tabla': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre de la tabla',
                    'id': 'id_tabla',
                    'class': 'form-control',
                }
            ),
            'registroid': forms.NumberInput(
                attrs={
                    'placeholder': 'ID del registro',
                    'id': 'id_registroid',
                    'class': 'form-control',
                }
            ),
            'accion': forms.Select(
                attrs={
                    'id': 'id_accion',
                    'class': 'form-control',
                }
            ),
            'fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'id': 'id_fecha',
                    'class': 'form-control',
                }
            ),
            'hora': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'id': 'id_hora',
                    'class': 'form-control',
                }
            ),
            'estacion': forms.TextInput(
                attrs={
                    'placeholder': 'Estación',
                    'id': 'id_estacion',
                    'class': 'form-control',
                }
            ),
        }

    def clean_estacion(self):
        estacion = self.cleaned_data.get('estacion')
        if not estacion or len(estacion) < 3:
            raise ValidationError("La estación debe tener al menos 3 caracteres.")
        return estacion.capitalize()
