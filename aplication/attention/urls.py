from django.urls import path
from aplication.attention.views.medical_attention import AtencionPDFView, AttentionCreateView, AttentionDetailView, AttentionListView, AttentionUpdateView
from aplication.core.views.home import HomeTemplateView
from aplication.attention.views.horario_atencion import HorarioAtencionListView, HorarioAtencionCreateView, HorarioAtencionUpdateView,HorarioAtencionDeleteView, HorarioAtencionDetailView
from aplication.attention.views.cita_medica import CitaMedicaListView, CitaMedicaCreateView, CitaMedicaUpdateView, CitaMedicaDeleteView, CitaMedicaDetailView  
from aplication.attention.views.examen_solicitado import ExamenSolicitadoListView, ExamenSolicitadoCreateView, ExamenSolicitadoUpdateView,ExamenSolicitadoDeleteView, ExamenSolicitadoDetailView  
from aplication.attention.views.servicios_adicionales import ServiciosAdicionalesListView, ServiciosAdicionalesCreateView, ServiciosAdicionalesUpdateView, ServiciosAdicionalesDeleteView, ServiciosAdicionalesDetailView
from aplication.attention.views.api import ActividadRecienteView, ProximasCitasView
from aplication.attention.views.costos_atencion import CostosAtencionListView, CostosAtencionCreateView, CostosAtencionUpdateView, CostosAtencionDeleteView, CostosAtencionDetailView
 

app_name='attention' # define un espacio de nombre para la aplicacion
urlpatterns = [
  # rutas de atenciones
  path('attention_list/',AttentionListView.as_view() ,name="attention_list"),
  path('attention_create/', AttentionCreateView.as_view(),name="attention_create"),
  path('attention_update/<int:pk>/', AttentionUpdateView.as_view(),name='attention_update'),
  path('attention_detail/<int:pk>/', AttentionDetailView.as_view(),name='attention_detail'),
  
  path('pdf/atencion/<int:pk>/', AtencionPDFView.as_view(), name='atencion_pdf'),
  
  # path('patient_delete/<int:pk>/', PatientDeleteView.as_view(),name='patient_delete'),
  
  # Rutas para Horario de Atención
    path('horario_atencion_list/', HorarioAtencionListView.as_view(), name='horario_atencion_list'),
    path('horario_atencion_create/', HorarioAtencionCreateView.as_view(), name='horario_atencion_create'),
    path('horario_atencion_update/<int:pk>/', HorarioAtencionUpdateView.as_view(), name='horario_atencion_update'),
    path('horario_atencion_delete/<int:pk>/', HorarioAtencionDeleteView.as_view(), name='horario_atencion_delete'),
    path('horario_atencion_detail/<int:pk>/', HorarioAtencionDetailView.as_view(), name='horario_atencion_detail'),
    
   # Rutas para Cita Médica
    path('cita_medica_list/', CitaMedicaListView.as_view(), name='cita_medica_list'),
    path('cita_medica_create/', CitaMedicaCreateView.as_view(), name='cita_medica_create'),
    path('cita_medica_update/<int:pk>/', CitaMedicaUpdateView.as_view(), name='cita_medica_update'),
    path('cita_medica_delete/<int:pk>/', CitaMedicaDeleteView.as_view(), name='cita_medica_delete'),
    path('cita_medica_detail/<int:pk>/', CitaMedicaDetailView.as_view(), name='cita_medica_detail'),  
    
   # Rutas para Examen Solicitado
    path('examen_solicitado_list/', ExamenSolicitadoListView.as_view(), name='examen_solicitado_list'),
    path('examen_solicitado_create/', ExamenSolicitadoCreateView.as_view(), name='examen_solicitado_create'),
    path('examen_solicitado_update/<int:pk>/', ExamenSolicitadoUpdateView.as_view(), name='examen_solicitado_update'),
    path('examen_solicitado_delete/<int:pk>/', ExamenSolicitadoDeleteView.as_view(), name='examen_solicitado_delete'),
    path('examen_solicitado_detail/<int:pk>/', ExamenSolicitadoDetailView.as_view(), name='examen_solicitado_detail'),
  
  # Rutas para Servicios Adicionales
    path('servicios_adicionales_list/', ServiciosAdicionalesListView.as_view(), name='servicios_adicionales_list'),
    path('servicios_adicionales_create/', ServiciosAdicionalesCreateView.as_view(), name='servicios_adicionales_create'),
    path('servicios_adicionales_update/<int:pk>/', ServiciosAdicionalesUpdateView.as_view(), name='servicios_adicionales_update'),
    path('servicios_adicionales_delete/<int:pk>/', ServiciosAdicionalesDeleteView.as_view(), name='servicios_adicionales_delete'),
    path('servicios_adicionales_detail/<int:pk>/', ServiciosAdicionalesDetailView.as_view(), name='servicios_adicionales_detail'),
  
  #Rutas para actividades recientes y proximas citas
    path('actividad_reciente/', ActividadRecienteView.as_view(), name='actividad_reciente'),
    path('proximas_citas/', ProximasCitasView.as_view(), name='proximas_citas'),  
  
  # Rutas de Costos de Atención
    path('costos_atencion_list/', CostosAtencionListView.as_view(), name='costos_atencion_list'),
    path('costos_atencion_create/', CostosAtencionCreateView.as_view(), name='costos_atencion_create'),
    path('costos_atencion_update/<int:pk>/', CostosAtencionUpdateView.as_view(), name='costos_atencion_update'),
    path('costos_atencion_delete/<int:pk>/', CostosAtencionDeleteView.as_view(), name='costos_atencion_delete'),
    path('costos_atencion_detail/<int:pk>/', CostosAtencionDetailView.as_view(), name='costos_atencion_detail'),

]