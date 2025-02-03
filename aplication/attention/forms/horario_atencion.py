from django.forms import ModelForm, ValidationError
from django import forms
from aplication.attention.models import HorarioAtencion

class Horario_AtencionForm(ModelForm):
    class Meta:
        model = HorarioAtencion
        fields = ["dia_semana", "hora_inicio", "hora_fin", "Intervalo_desde", "Intervalo_hasta", "activo"]

        # Mensajes de error personalizados para ciertos campos
        error_messages = {
            "hora_inicio": {
                "invalid": "Ingrese una hora válida para el inicio.",
            },
            "hora_fin": {
                "invalid": "Ingrese una hora válida para el fin.",
            },
        }

        # Personalización de widgets
        widgets = {
            "dia_semana": forms.Select(
                attrs={
                    "id": "id_dia_semana",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "hora_inicio": forms.TimeInput(
                attrs={
                    "type": "time",
                    "placeholder": "Ingrese la hora de inicio",
                    "id": "id_hora_inicio",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "hora_fin": forms.TimeInput(
                attrs={
                    "type": "time",
                    "placeholder": "Ingrese la hora de fin",
                    "id": "id_hora_fin",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "Intervalo_desde": forms.TimeInput(
                attrs={
                    "type": "time",
                    "placeholder": "Ingrese intervalo desde",
                    "id": "id_intervalo_desde",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "Intervalo_hasta": forms.TimeInput(
                attrs={
                    "type": "time",
                    "placeholder": "Ingrese intervalo hasta",
                    "id": "id_intervalo_hasta",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "activo": forms.CheckboxInput(
                attrs={
                    "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
        }
        labels = {
            "dia_semana": "Día de la Semana",
            "hora_inicio": "Hora de Inicio",
            "hora_fin": "Hora de Fin",
            "Intervalo_desde": "Intervalo Desde",
            "Intervalo_hasta": "Intervalo Hasta",
            "activo": "Activo",
        }

    # Método de limpieza para validar la coherencia de la hora de inicio y fin
    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fin = cleaned_data.get("hora_fin")

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise ValidationError("La hora de inicio debe ser anterior a la hora de fin.")

        return cleaned_data

    