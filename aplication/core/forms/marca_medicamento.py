from django.forms import ModelForm, ValidationError
from django import forms
from aplication.core.models import MarcaMedicamento

class MarcaMedicamentoForm(ModelForm):
    class Meta:
        model = MarcaMedicamento
        # Campos que se mostrarán en el formulario
        fields = ["nombre", "descripcion", "activo"]

        # Mensajes de error personalizados
        error_messages = {
            "nombre": {
                "unique": "Ya existe una marca de medicamento con este nombre",
                "required": "El nombre de la marca de medicamento es requerido",
            },
            "descripcion": {
                "required": "La descripción es requerida",
            },
        }

        # Personalización de los widgets
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el nombre de la marca de medicamento",
                    "id": "id_nombre",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "placeholder": "Digite la descripción",
                    "id": "id_descripcion",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "activo": forms.CheckboxInput(
                attrs={
                    "id": "id_activo",
                    "class": "form-checkbox h-4 w-4 text-blue-600 transition duration-150 ease-in-out",
                }
            ),
        }

        labels = {
            "nombre": "Nombre de la Marca de Medicamento",
            "descripcion": "Descripción",
            "activo": "¿Activo?",
        }

    # Métodos de limpieza
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if not nombre or len(nombre) < 3:
            raise ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre.capitalize()

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get("descripcion")
        if descripcion and len(descripcion) < 10:
            raise ValidationError("La descripción debe tener al menos 10 caracteres.")
        return descripcion.capitalize()
