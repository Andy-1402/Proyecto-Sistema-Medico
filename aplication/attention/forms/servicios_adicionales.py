from django import forms
from django.forms import ModelForm, ValidationError
from aplication.attention.models import ServiciosAdicionales

class ServiciosAdicionalesForm(ModelForm):
    class Meta:
        model = ServiciosAdicionales
        fields = ["nombre_servicio", "costo_servicio", "descripcion", "activo"]

        # Mensajes de error personalizados para ciertos campos
        error_messages = {
            "nombre_servicio": {
                "required": "El nombre del servicio es obligatorio.",
            },
            "costo_servicio": {
                "required": "El costo del servicio es obligatorio.",
                "invalid": "Ingrese un costo válido para el servicio.",
            },
        }

        # Personalización de widgets
        widgets = {
            "nombre_servicio": forms.TextInput(
                attrs={
                    "id": "id_nombre_servicio",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "costo_servicio": forms.NumberInput(
                attrs={
                    "id": "id_costo_servicio",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    "step": "0.01",  # Permitir decimales
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "id": "id_descripcion",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    "rows": 3,  # Número de filas
                }
            ),
            "activo": forms.CheckboxInput(
                attrs={
                    "id": "id_activo",
                    "class": "form-check-input",
                }
            ),
        }

        labels = {
            "nombre_servicio": "Nombre del Servicio",
            "costo_servicio": "Costo del Servicio",
            "descripcion": "Descripción",
            "activo": "Activo",
        }

    # Método de limpieza para validar el costo del servicio
    def clean_costo_servicio(self):
        costo_servicio = self.cleaned_data.get("costo_servicio")
        if costo_servicio < 0:
            raise ValidationError("El costo del servicio no puede ser negativo.")
        return costo_servicio
