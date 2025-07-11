from django.utils import timezone
from decimal import Decimal
import json
from django.urls import reverse_lazy
from django.db import transaction
from aplication.attention.forms.medical_attention import AttentionForm
from aplication.attention.models import Atencion, DetalleAtencion
from aplication.core.forms.patient import PatientForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from aplication.core.models import Diagnostico, Medicamento
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from doctor.utils import custom_serializer, save_audit

class AttentionListView(LoginRequiredMixin,ListViewMixin,ListView):
    template_name = "attention/medical_attention/list.html"
    model = Atencion
    context_object_name = 'atenciones'
    # query = None
    paginate_by = 10
    
    def get_queryset(self):
        # self.query = Q()
        q1 = self.request.GET.get('q') # ver
        sex= self.request.GET.get('sex')
        if q1 is not None: 
            self.query.add(Q(paciente__nombres__icontains=q1), Q.OR) 
            self.query.add(Q(paciente__apellidos__icontains=q1), Q.OR) 
            self.query.add(Q(paciente__cedula__icontains=q1), Q.OR) 
        if sex == "M" or sex=="F": self.query.add(Q(paciente__sexo__icontains=sex), Q.AND)   
        return self.model.objects.filter(self.query).order_by('-fecha_atencion')
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
        # context['title'] = "SaludSync"
        # context['title1'] = "Consulta de Pacientes"
        # return context
    
class AttentionCreateView(LoginRequiredMixin,CreateViewMixin, CreateView):
    model = Atencion
    template_name = 'attention/medical_attention/form.html'
    form_class = AttentionForm
    success_url = reverse_lazy('attention:attention_list')
    # permission_required = 'add_supplier' # en PermissionMixn se verfica si un grupo tiene el permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['detail_atencion'] =[]
        context["medications"] = Medicamento.active_medication.order_by('nombre')
        
        return context
    
    def post(self, request, *args, **kwargs):
        # Convertir el cuerpo de la solicitud a un diccionario Python
        data = json.loads(request.body)
        print(data)
        medicamentos = data['medicamentos']  
        print(medicamentos)
        #Crear una instancia del formulario y poblarla con los datos JSON
        try:
            with transaction.atomic():
                # Crear la instancia del modelo Atencion
                print("entro atencion")
                atencion=Atencion.objects.create(
                    paciente_id=int(data['paciente']),
                    presion_arterial=data['presionArterial'],
                    pulso=int(data['pulso']),
                    temperatura=Decimal(data['temperatura']),
                    frecuencia_respiratoria=int(data['frecuenciaRespiratoria']),
                    saturacion_oxigeno=Decimal(data['saturacionOxigeno']),
                    peso=Decimal(data['peso']),
                    altura=Decimal(data['altura']),
                    motivo_consulta=data['motivoConsulta'],
                    sintomas=data['sintomas'],
                    tratamiento=data['tratamiento'],
                    examen_fisico=data['examenFisico'],
                    examenes_enviados=data['examenesEnviados'],
                    comentario_adicional=data['comentarioAdicional'],
                    fecha_atencion= timezone.now()
                )
                diagnostico_ids = data.get('diagnostico', [])
                diagnosticos = Diagnostico.objects.filter(id__in=diagnostico_ids)
                atencion.diagnostico.set(diagnosticos)
                atencion.save()
                # Ahora procesamos el arreglo de medicamentos
                print("voy a medicamentos")
                for medicamento in medicamentos:
                    #Crear el detalle de atención para cada medicamento
                    DetalleAtencion.objects.create(
                        atencion=atencion,
                        medicamento_id=int(medicamento['codigo']),
                        cantidad=int(medicamento['cantidad']),
                        prescripcion=medicamento['prescripcion'],
                        # Si necesitas la duración del tratamiento, puedes agregarla aquí
                    )
                
                save_audit(request, atencion, "A")
                messages.success(self.request, f"Éxito al registrar la atención médica #{atencion.id}")
                return JsonResponse({"msg": "Éxito al registrar la atención médica."}, status=200)

        except Exception as ex:
            messages.error(self.request, f"Érro al registrar la atención médica")
            return JsonResponse({"msg": str(ex)}, status=400)
        
      

class AttentionUpdateView(LoginRequiredMixin,UpdateViewMixin,UpdateView):
    model = Atencion
    template_name = 'attention/medical_attention/form.html'
    form_class = AttentionForm
    success_url = reverse_lazy('attention:attention_list')
    # permission_required = 'add_supplier' # en PermissionMixn se verfica si un grupo tiene el permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # Obtiene una lista de medicamentos activos usando un método del modelo Medicamento.
        # Extrae solo los campos 'id' y 'nombre', y los ordena alfabéticamente por 'nombre'
        context["medications"] = Medicamento.active_medication.values('id','nombre').order_by('nombre')
        # Obtiene una lista de detalles de atención relacionados con la atención actual (self.object.id)
        # Filtra por el ID de la atención y selecciona los campos 'medicamento_id', 'medicamento_nombre',
        # 'cantidad' y 'prescripcion' para optimizar la consulta
        detail_atencion =list(DetalleAtencion.objects.filter(atencion_id=self.object.id).values("medicamento_id","medicamento__nombre","cantidad","prescripcion"))
        # Convierte la lista de diccionarios en una cadena JSON para que pueda ser usada en JavaScript.
        # Utiliza un serializador personalizado 'custom_serializer' para manejar tipos de datos especiales
        detail_atencion=json.dumps(detail_atencion,default=custom_serializer)
        # Agrega los detalles de la atención al contexto con la clave 'detail_atencion'
        # El resultado será un string JSON como: '[{"id": 1, "nombre": "aspirina"}, {...}, {...}]'
        context['detail_atencion']=detail_atencion 
        return context
    
    def post(self, request, *args, **kwargs):
        # Convertir el cuerpo de la solicitud a un diccionario Python
        data = json.loads(request.body)
        print(data)
        medicamentos = data['medicamentos']  
        print(medicamentos)
        try:
             atencion = Atencion.objects.get(id=self.kwargs.get('pk'))
             print(atencion)
             with transaction.atomic():
                # Crear la instancia del modelo Atencion
                atencion.paciente_id=int(data['paciente'])
                atencion.presion_arterial=data['presionArterial']
                atencion.pulso=int(data['pulso'])
                atencion.temperatura=Decimal(data['temperatura'])
                atencion.frecuencia_respiratoria=int(data['frecuenciaRespiratoria'])
                atencion.saturacion_oxigeno=Decimal(data['saturacionOxigeno'])
                atencion.peso=Decimal(data['peso'])
                atencion.altura=Decimal(data['altura'])
                atencion.motivo_consulta=data['motivoConsulta']
                atencion.sintomas=data['sintomas']
                atencion.tratamiento=data['tratamiento']
                atencion.examen_fisico=data['examenFisico']
                atencion.examenes_enviados=data['examenesEnviados']
                atencion.comentario_adicional=data['comentarioAdicional']
                print("datos de diagnostico")
                diagnostico_ids = data.get('diagnostico', [])
                print("diag=",diagnostico_ids)
                diagnosticos = Diagnostico.objects.filter(id__in=diagnostico_ids)
                atencion.diagnostico.set(diagnosticos)
                atencion.save()
                print("grabo atencion")
                # borrar el detalle asociado a esa atencion
                DetalleAtencion.objects.filter(atencion_id=atencion.id).delete()
                # Ahora procesamos el arreglo de medicamentos
                print("voy a medicamentos update")
                for medicamento in medicamentos:
                    #Crear el detalle de atención para cada medicamento
                    DetalleAtencion.objects.create(
                        atencion=atencion,
                        medicamento_id=int(medicamento['codigo']),
                        cantidad=int(medicamento['cantidad']),
                        prescripcion=medicamento['prescripcion'],
                        # Si necesitas la duración del tratamiento, puedes agregarla aquí
                    )
                
                save_audit(request, atencion, "M")
                messages.success(self.request, f"Éxito al Actualizar la atención médica #{atencion.id}")
                return JsonResponse({"msg": "Éxito al Actualizar la atención médica."}, status=200)
        except Exception as ex:
            messages.error(self.request, f"Érro al actualizar la atención médica")
            return JsonResponse({"msg": str(ex)}, status=400)
        
class AttentionDetailView(LoginRequiredMixin,DetailView):
    model = Atencion
    
    def get(self, request, *args, **kwargs):
        print("entro get")
        atencion = self.get_object()
        print(atencion)
        detail_atencion =list(DetalleAtencion.objects.filter(atencion_id=atencion.id).values("medicamento_id","medicamento__nombre","cantidad","prescripcion"))
        detail_atencion=json.dumps(detail_atencion,default=custom_serializer)
        data = {
            'id': atencion.id,
            'nombres': atencion.paciente.nombre_completo,
            'foto': atencion.paciente.get_image(),
            'detalle_atencion': detail_atencion
        }
        print(data)
        return JsonResponse(data)
    
    

from django.http import HttpResponse
from django.views import View
from reportlab.pdfgen import canvas
from aplication.attention.models import Atencion

class AtencionPDFView(View):
    def get(self, request, pk, *args, **kwargs):
        # Obtén la atención médica específica por su ID
        atencion = Atencion.objects.select_related('paciente').get(pk=pk)

        # Configura la respuesta como PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="atencion_{atencion.id}.pdf"'

        # Genera el PDF
        p = canvas.Canvas(response)
        p.setFont("Helvetica", 12)

        # Encabezado
        p.drawString(100, 800, "Ficha de Atención Médica")
        p.line(100, 795, 400, 795)

        # Información del Paciente
        p.drawString(100, 760, f"Paciente: {atencion.paciente}")
        p.drawString(100, 740, f"Fecha de Atención: {atencion.fecha_atencion.strftime('%d/%m/%Y %H:%M')}")
        p.drawString(100, 720, f"Motivo de Consulta: {atencion.motivo_consulta}")

        # Signos vitales
        p.drawString(100, 700, f"Presión Arterial: {atencion.presion_arterial}")
        p.drawString(100, 680, f"Pulso: {atencion.pulso} ppm")
        p.drawString(100, 660, f"Temperatura: {atencion.temperatura} °C")
        p.drawString(100, 640, f"Frecuencia Respiratoria: {atencion.frecuencia_respiratoria} rpm")
        p.drawString(100, 620, f"Saturación de Oxígeno: {atencion.saturacion_oxigeno}%")
        p.drawString(100, 600, f"Peso: {atencion.peso} kg")
        p.drawString(100, 580, f"Altura: {atencion.altura} m")
        p.drawString(100, 560, f"IMC Calculado: {atencion.calcular_imc if atencion.calcular_imc else 'N/A'}")

        # Detalles clínicos
        p.drawString(100, 540, "Síntomas:")
        text = p.beginText(120, 520)
        text.setFont("Helvetica", 10)
        for line in atencion.sintomas.splitlines():
            text.textLine(line)
        p.drawText(text)

        p.drawString(100, 500, "Plan de Tratamiento:")
        text = p.beginText(120, 480)
        text.setFont("Helvetica", 10)
        for line in atencion.tratamiento.splitlines():
            text.textLine(line)
        p.drawText(text)

        # Diagnósticos
        p.drawString(100, 460, f"Diagnósticos: {atencion.get_diagnosticos}")

        # Examen físico
        p.drawString(100, 440, "Examen Físico:")
        text = p.beginText(120, 420)
        text.setFont("Helvetica", 10)
        for line in atencion.examen_fisico.splitlines():
            text.textLine(line)
        p.drawText(text)

        # Exámenes enviados
        p.drawString(100, 400, "Exámenes Enviados:")
        text = p.beginText(120, 380)
        text.setFont("Helvetica", 10)
        for line in atencion.examenes_enviados.splitlines():
            text.textLine(line)
        p.drawText(text)

        # Comentarios adicionales
        p.drawString(100, 360, "Comentarios Adicionales:")
        text = p.beginText(120, 340)
        text.setFont("Helvetica", 10)
        for line in atencion.comentario_adicional.splitlines():
            text.textLine(line)
        p.drawText(text)

        # Finaliza el PDF
        p.showPage()
        p.save()

        return response

    

