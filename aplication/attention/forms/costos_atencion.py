from django import forms
from django.forms import ModelForm, ValidationError
from aplication.attention.models import CostosAtencion, CostoAtencionDetalle

class CostosAtencionForm(ModelForm):
    class Meta:
        model = CostosAtencion
        fields = ["atencion", "total", "activo"]

        # Personalización de widgets
        widgets = {
            "atencion": forms.Select(
                attrs={
                    "id": "id_atencion",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "total": forms.NumberInput(
                attrs={
                    "type": "number",
                    "placeholder": "Ingrese el total",
                    "id": "id_total",
                    "step": "0.01",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "activo": forms.CheckboxInput(
                attrs={
                    "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
        }
        labels = {
            "atencion": "Atención Médica",
            "total": "Costo Total",
            "activo": "Activo",
        }

    # Validación personalizada para el campo total
    def clean_total(self):
        total = self.cleaned_data.get("total")
        if total and total < 0:
            raise ValidationError("El total no puede ser un valor negativo.")
        return total


class CostoAtencionDetalleForm(ModelForm):
    class Meta:
        model = CostoAtencionDetalle
        fields = ["costo_atencion", "servicios_adicionales", "costo_servicio"]

        # Personalización de widgets
        widgets = {
            "costo_atencion": forms.Select(
                attrs={
                    "id": "id_costo_atencion",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "servicios_adicionales": forms.Select(
                attrs={
                    "id": "id_servicios_adicionales",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "costo_servicio": forms.NumberInput(
                attrs={
                    "type": "number",
                    "placeholder": "Ingrese el costo del servicio",
                    "id": "id_costo_servicio",
                    "step": "0.01",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
        }
        labels = {
            "costo_atencion": "Costo Atención",
            "servicios_adicionales": "Servicios Adicionales",
            "costo_servicio": "Costo del Servicio",
        }

    # Validación personalizada para el costo del servicio
    def clean_costo_servicio(self):
        costo_servicio = self.cleaned_data.get("costo_servicio")
        if costo_servicio and costo_servicio <= 0:
            raise ValidationError("El costo del servicio debe ser mayor que cero.")
        return costo_servicio
