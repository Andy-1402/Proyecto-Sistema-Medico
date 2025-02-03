from django import forms
from django.forms import ModelForm, ValidationError
from aplication.attention.models import ExamenSolicitado

class ExamenSolicitadoForm(ModelForm):
    class Meta:
        model = ExamenSolicitado
        fields = ["nombre_examen", "paciente", "resultado", "comentario", "estado"]

        # Mensajes de error personalizados
        error_messages = {
            "nombre_examen": {
                "required": "El nombre del examen es obligatorio.",
                "max_length": "El nombre del examen no puede exceder los 255 caracteres.",
            },
            "estado": {
                "required": "Debe seleccionar un estado para el examen.",
            },
        }

        # Personalización de widgets
        widgets = {
            "nombre_examen": forms.TextInput(
                attrs={
                    "id": "id_nombre_examen",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full",
                }
            ),
            "paciente": forms.Select(
                attrs={
                    "id": "id_paciente",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full",
                }
            ),
            "resultado": forms.FileInput(
                attrs={
                    "id": "id_resultado",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full",
                }
            ),
            "comentario": forms.Textarea(
                attrs={
                    "id": "id_comentario",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full",
                    "rows": 3,
                }
            ),
            "estado": forms.Select(
                attrs={
                    "id": "id_estado",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full",
                }
            ),
        }

        labels = {
            "nombre_examen": "Nombre del Examen",
            "paciente": "Paciente",
            "resultado": "Resultado del Examen (Archivo)",
            "comentario": "Comentario",
            "estado": "Estado del Examen",
        }

    # Método de limpieza para validaciones adicionales
    def clean_nombre_examen(self):
        nombre_examen = self.cleaned_data.get("nombre_examen")
        if len(nombre_examen) > 255:
            raise ValidationError("El nombre del examen es demasiado largo.")
        return nombre_examen

    def clean_resultado(self):
        resultado = self.cleaned_data.get("resultado")
        if resultado and not resultado.name.endswith(('.pdf', '.jpg', '.png')):
            raise ValidationError("El archivo de resultado debe ser un PDF o una imagen (.jpg, .png).")
        return resultado
