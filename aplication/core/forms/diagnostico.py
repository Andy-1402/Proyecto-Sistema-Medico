from django.forms import ModelForm, ValidationError
from django import forms
from aplication.core.models import Diagnostico

class DiagnosticoForm(ModelForm):
    class Meta:
        model = Diagnostico
        fields = [
            "codigo",
            "descripcion",
            "datos_adicionales",
            "activo",
        ]
        # Personalización de los widgets para los campos del formulario HTML
        widgets = {
            "codigo": forms.TextInput(
                attrs={
                    "id": "id_codigo",
                    "placeholder": "Ingrese el código del diagnóstico",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "descripcion": forms.TextInput(
                attrs={
                    "id": "id_descripcion",
                    "placeholder": "Ingrese la descripción del diagnóstico",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "datos_adicionales": forms.Textarea(
                attrs={
                    "id": "id_datos_adicionales",
                    "placeholder": "Ingrese datos adicionales relevantes (opcional)",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    "rows": 3,
                }
            ),
            "activo": forms.CheckboxInput(
                attrs={
                    "id": "id_activo",
                    "class": "focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded dark:focus:ring-blue-500 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 dark:bg-principal dark:border-gray-600",
                }
            ),
        }

    # Validación personalizada para el campo "codigo"
    def clean_codigo(self):
        codigo = self.cleaned_data.get("codigo")
        if len(codigo) < 5:
            raise ValidationError("El código debe tener al menos 5 caracteres.")
        return codigo.upper()
