from django import forms
from django.forms import ModelForm, ValidationError
from aplication.attention.models import CitaMedica

class CitaMedicaForm(ModelForm):
    class Meta:
        model = CitaMedica
        fields = ["paciente", "fecha", "hora_cita", "estado"]

        # Mensajes de error personalizados para ciertos campos
        error_messages = {
            "fecha": {
                "invalid": "Ingrese una fecha válida para la cita.",
                "required": "La fecha de la cita es obligatoria.",
            },
            "hora_cita": {
                "invalid": "Ingrese una hora válida para la cita.",
                "required": "La hora de la cita es obligatoria.",
            },
            "estado": {
                "required": "Debe seleccionar un estado para la cita.",
            },
        }

        # Personalización de widgets
        widgets = {
            "paciente": forms.Select(
                attrs={
                    "id": "id_paciente",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "fecha": forms.DateInput(
                attrs={
                    "type": "date",
                    "id": "id_fecha",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "hora_cita": forms.TimeInput(
                attrs={
                    "type": "time",
                    "id": "id_hora_cita",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "estado": forms.Select(
                attrs={
                    "id": "id_estado",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
        }
        labels = {
            "paciente": "Paciente",
            "fecha": "Fecha de la Cita",
            "hora_cita": "Hora de la Cita",
            "estado": "Estado de la Cita",
        }

    # Método de limpieza para validar la coherencia de la fecha y hora de la cita
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get("fecha")
        hora_cita = cleaned_data.get("hora_cita")

        # Validación adicional (ejemplo: evitar citas en el pasado)
        if fecha and hora_cita:
            from datetime import datetime, date
            cita_datetime = datetime.combine(fecha, hora_cita)
            if cita_datetime < datetime.now():
                raise ValidationError("No se pueden agendar citas en el pasado.")

        return cleaned_data
