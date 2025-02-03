from django import forms
from django.forms import ModelForm, ValidationError
from aplication.core.models import Especialidad  # Asegúrate de importar el modelo adecuado

class EspecialidadForm(ModelForm):
    class Meta:
        model = Especialidad
        fields = ["nombre", "descripcion", "activo"]  # Los campos deben ir en orden y van estar incluidos en el formulario
        
        # Personalización de los widgets para los campos del formulario HTML
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Nombre de la especialidad",
                    "id": "id_nombre",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "placeholder": "Descripción breve de la especialidad",
                    "id": "id_descripcion",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    "rows": 3  # Puedes ajustar el tamaño de la caja de texto según lo necesites
                }
            ),
            "activo": forms.CheckboxInput(
                attrs={
                    "id": "id_activo",
                    "class": "form-check-input",
                }
            ),
        }

    # Validación personalizada para el campo "descripcion"
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get("descripcion")
        if descripcion and len(descripcion) < 5:
            raise ValidationError("La descripción debe tener al menos 5 caracteres.")
        
        return descripcion.capitalize()

    # Validación personalizada para el campo "nombre" (si es necesario)
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if not nombre:
            raise ValidationError("El nombre de la especialidad es obligatorio.")
        return nombre.capitalize()  # Puedes usar .capitalize() o cualquier otra transformación que prefieras
