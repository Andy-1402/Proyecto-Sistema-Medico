from django.forms import ModelForm, ValidationError
from django import forms
from aplication.core.models import TipoSangre

class TipoSangreForm(ModelForm):
    class Meta:
        model = TipoSangre
        fields = ["tipo", "descripcion"]  # Los campos deben ir en orden y van estar incluidos en el formulario
        
        # Personalización de los widgets para los campos del formulario HTML
        widgets = {
            "tipo": forms.Select(
                attrs={
                    "id": "id_tipo",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "descripcion": forms.TextInput(
                attrs={
                    "placeholder": "Descripción breve",
                    "id": "id_descripcion",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
        }
    
    # Validación personalizada para el campo "descripcion"
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get("descripcion")
        if not descripcion or len(descripcion) < 5:
            raise ValidationError("La descripción debe tener al menos 5 caracteres.")
        
        return descripcion.capitalize()
