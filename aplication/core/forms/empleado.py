from django.forms import ModelForm, ValidationError
from django import forms
from aplication.core.models import Empleado


class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleado
        fields = [
            "nombres", "apellidos", "cedula", "fecha_nacimiento",
            "cargo", "sueldo", "direccion", "latitud", "longitud", "foto", "activo"
        ]

        error_messages = {
            "nombres": {
                "required": "El nombre del empleado es requerido",
            },
            "apellidos": {
                "required": "El apellido del empleado es requerido",
            },
            "cedula": {
                "unique": "Ya existe un empleado con esta cédula",
                "required": "La cédula es requerida",
            },
            "sueldo": {
                "required": "El sueldo es un campo obligatorio",
            },
            "direccion": {
                "required": "La dirección es obligatoria",
            },
        }

        widgets = {
            "nombres": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese los nombres del empleado",
                    "id": "id_nombres",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "apellidos": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese los apellidos del empleado",
                    "id": "id_apellidos",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "cedula": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese la cédula",
                    "id": "id_cedula",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "fecha_nacimiento": forms.DateInput(
                attrs={
                    "type": "date",
                    "id": "id_fecha_nacimiento",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "cargo": forms.Select(
                attrs={
                    "id": "id_cargo",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "sueldo": forms.NumberInput(
                attrs={
                    "placeholder": "Ingrese el sueldo",
                    "id": "id_sueldo",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "direccion": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese la dirección",
                    "id": "id_direccion",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "latitud": forms.NumberInput(
                attrs={
                    "placeholder": "Latitud de la residencia",
                    "id": "id_latitud",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "longitud": forms.NumberInput(
                attrs={
                    "placeholder": "Longitud de la residencia",
                    "id": "id_longitud",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "foto": forms.ClearableFileInput(
                attrs={
                    "id": "id_foto",
                    "class": "block w-full text-sm text-gray-500 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 focus:outline-none dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500",
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
            "nombres": "Nombre del Empleado",
            "apellidos": "Apellido del Empleado",
            "cedula": "Cédula",
            "fecha_nacimiento": "Fecha de Nacimiento",
            "cargo": "Cargo",
            "sueldo": "Sueldo",
            "direccion": "Dirección",
            "latitud": "Latitud",
            "longitud": "Longitud",
            "foto": "Foto del Empleado",
            "activo": "¿Activo?",
        }

    # Métodos de limpieza personalizados
    def clean_nombres(self):
        nombres = self.cleaned_data.get("nombres")
        # Verificar si el campo tiene menos de 2 caracteres
        if not nombres or len(nombres) < 2:
            raise ValidationError(
                "El nombre debe tener al menos 2 caracteres.")
        return nombres.upper()

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get("apellidos")
        # Verificar si el campo tiene menos de 1 carácter
        if not apellidos or len(apellidos) < 1:
            raise ValidationError(
                "El apellido debe tener al menos 1 carácter.")
        return apellidos.upper()

    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula")
        if not cedula.isdigit() or len(cedula) != 10:
            raise ValidationError(
                "La cédula debe ser numérica y contener 10 dígitos.")
        return cedula
