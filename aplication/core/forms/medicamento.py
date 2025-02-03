from django.forms import ModelForm, ValidationError
from django import forms
from aplication.core.models import Medicamento

class MedicamentoForm(ModelForm):
    class Meta:
        model = Medicamento
        fields = [
            "tipo",
            "marca_medicamento",
            "nombre",
            "descripcion",
            "concentracion",
            "cantidad",
            "precio",
            "comercial",
            "activo",
        ]
        # Personalización de los widgets para los campos del formulario HTML
        widgets = {
            "tipo": forms.Select(
                attrs={
                    "id": "id_tipo",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "marca_medicamento": forms.Select(
                attrs={
                    "id": "id_marca",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "nombre": forms.TextInput(
                attrs={
                    "id": "id_nombre",
                    "placeholder": "Ingrese el nombre del medicamento",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "id": "id_descripcion",
                    "placeholder": "Ingrese una descripción del medicamento",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    "rows": 3,
                }
            ),
            "concentracion": forms.TextInput(
                attrs={
                    "id": "id_concentracion",
                    "placeholder": "Concentración del medicamento (ej: 500mg)",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "cantidad": forms.NumberInput(
                attrs={
                    "id": "id_cantidad",
                    "placeholder": "Stock disponible",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "precio": forms.NumberInput(
                attrs={
                    "id": "id_precio",
                    "placeholder": "Precio del medicamento",
                    "step": "0.01",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "comercial": forms.CheckboxInput(
                attrs={
                    "id": "id_comercial",
                    "class": "focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded dark:focus:ring-blue-500 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 dark:bg-principal dark:border-gray-600",
                }
            ),
            "activo": forms.CheckboxInput(
                attrs={
                    "id": "id_activo",
                    "class": "focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded dark:focus:ring-blue-500 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 dark:bg-principal dark:border-gray-600",
                }
            ),
        }

    # Validación personalizada para el campo "nombre"
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if len(nombre) < 3:
            raise ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre.capitalize()
