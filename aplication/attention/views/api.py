from django.views.generic.list import ListView
from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from aplication.attention.models import CitaMedica, Atencion
from aplication.core.models import Paciente


class ActividadRecienteView(ListView):
    def get(self, request, *args, **kwargs):
        recientes = []

        # Nuevos pacientes registrados
        nuevos_pacientes = Paciente.objects.order_by('-id')[:5]  # Toma los últimos 5 registros
        recientes += [{"tipo": "Nuevo paciente", "detalle": f"{paciente.nombres} {paciente.apellidos}", "tiempo": "Recientemente"} for paciente in nuevos_pacientes]

        # Citas completadas recientemente
        citas_completadas = CitaMedica.objects.filter(estado="R", fecha__gte=now() - timedelta(days=1))
        recientes += [{"tipo": "Cita completada", "detalle": str(cita), "tiempo": "Hace poco"} for cita in citas_completadas]

        # Atenciones recientes
        nuevas_atenciones = Atencion.objects.filter(fecha_atencion__gte=now() - timedelta(days=1))
        recientes += [{"tipo": "Nueva atención", "detalle": str(atencion), "tiempo": "Hace poco"} for atencion in nuevas_atenciones]

        return JsonResponse({"actividades": recientes})

class ProximasCitasView(ListView):
    def get(self, request, *args, **kwargs):
        hoy = now().date()
        citas = CitaMedica.objects.filter(fecha=hoy, estado="P").order_by('hora_cita')
        resultado = [{"paciente": str(cita.paciente), "hora": cita.hora_cita.strftime('%I:%M %p')} for cita in citas]

        return JsonResponse({"citas": resultado})
