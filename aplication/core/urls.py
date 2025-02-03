from django.urls import path
from aplication.core.views.home import HomeTemplateView
from aplication.core.views.patient import PatientCreateView, PatientDeleteView, PatientDetailView, PatientListView, PatientUpdateView, mapa_patient
from aplication.core.views.tipo_sangre import TipoSangreCreateView, TipoSangreDeleteView, TipoSangreDetailView, TipoSangreListView, TipoSangreUpdateView
from aplication.core.views.especialidad import EspecialidadCreateView, EspecialidadDeleteView, EspecialidadDetailView, EspecialidadListView, EspecialidadUpdateView  # Importa las vistas de Especialidad
from aplication.core.views.doctor import DoctorCreateView, DoctorDeleteView, DoctorDetailView, DoctorListView, DoctorUpdateView
from aplication.core.views.tipo_medicamento import TipoMedicamentoListView, TipoMedicamentoCreateView, TipoMedicamentoUpdateView,TipoMedicamentoDeleteView, TipoMedicamentoDetailView
from .views.marca_medicamento import MarcaMedicamentoListView, MarcaMedicamentoCreateView,MarcaMedicamentoUpdateView, MarcaMedicamentoDeleteView,MarcaMedicamentoDetailView
from aplication.core.views.empleado import EmpleadoListView, EmpleadoCreateView, EmpleadoUpdateView,EmpleadoDeleteView, EmpleadoDetailView
from aplication.core.views.cargo import CargoListView, CargoCreateView, CargoUpdateView,CargoDeleteView, CargoDetailView
from aplication.core.views.medicamento import MedicamentoListView,MedicamentoCreateView,MedicamentoUpdateView,MedicamentoDeleteView,MedicamentoDetailView
from aplication.core.views.diagnostico import DiagnosticoListView,DiagnosticoCreateView,DiagnosticoUpdateView,DiagnosticoDeleteView,DiagnosticoDetailView
from aplication.core.views.audit import AuditUserCreateView, AuditUserDeleteView, AuditUserDetailView, AuditUserListView, AuditUserUpdateView

app_name = 'core'  # define un espacio de nombre para la aplicacion
urlpatterns = [
    # Ruta principal
    
    path('', HomeTemplateView.as_view(), name='home'),
    
    # Rutas de pacientes
    path('patient_list/', PatientListView.as_view(), name="patient_list"),
    path('patient_create/', PatientCreateView.as_view(), name="patient_create"),
    path('patient_update/<int:pk>/', PatientUpdateView.as_view(), name='patient_update'),
    path('patient_delete/<int:pk>/', PatientDeleteView.as_view(), name='patient_delete'),
    path('patient_detail/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('patient_map/<int:pk>/', mapa_patient, name='patient_map'),

    # Rutas de Tipos de Sangre
    path('tipo_sangre_list/', TipoSangreListView.as_view(), name='tipo_sangre_list'),
    path('tipo_sangre_create/', TipoSangreCreateView.as_view(), name='tipo_sangre_create'),
    path('tipo_sangre_update/<int:pk>/', TipoSangreUpdateView.as_view(), name='tipo_sangre_update'),
    path('tipo_sangre_delete/<int:pk>/', TipoSangreDeleteView.as_view(), name='tipo_sangre_delete'),
    path('tipo_sangre_detail/<int:pk>/', TipoSangreDetailView.as_view(), name='tipo_sangre_detail'),

    # Rutas de Especialidades
    path('especialidad_list/', EspecialidadListView.as_view(), name='especialidad_list'),
    path('especialidad_create/', EspecialidadCreateView.as_view(), name='especialidad_create'),
    path('especialidad_update/<int:pk>/', EspecialidadUpdateView.as_view(), name='especialidad_update'),
    path('especialidad_delete/<int:pk>/', EspecialidadDeleteView.as_view(), name='especialidad_delete'),
    path('especialidad_detail/<int:pk>/', EspecialidadDetailView.as_view(), name='especialidad_detail'),
    
    
    # Rutas de Doctor
    
    path('doctor_list/', DoctorListView.as_view(), name='doctor_list'),
    path('doctor_create/', DoctorCreateView.as_view(), name='doctor_create'),
    path('doctor_update/<int:pk>/', DoctorUpdateView.as_view(), name='doctor_update'),
    path('doctor_delete/<int:pk>/', DoctorDeleteView.as_view(), name='doctor_delete'),
    path('doctor_detail/<int:pk>/', DoctorDetailView.as_view(), name='doctor_detail'),
    
     # Rutas de tipo de medicamento
    path('tipo_medicamento_list/', TipoMedicamentoListView.as_view(), name="tipo_medicamento_list"),
    path('tipo_medicamento_create/', TipoMedicamentoCreateView.as_view(), name="tipo_medicamento_create"),
    path('tipo_medicamento_update/<int:pk>/', TipoMedicamentoUpdateView.as_view(), name='tipo_medicamento_update'),
    path('tipo_medicamento_delete/<int:pk>/', TipoMedicamentoDeleteView.as_view(), name='tipo_medicamento_delete'),
    path('tipo_medicamento_detail/<int:pk>/', TipoMedicamentoDetailView.as_view(), name='tipo_medicamento_detail'),
    
    # Rutas de Marca de medicamento
    
    path('marca_medicamento_list/', MarcaMedicamentoListView.as_view(), name="marca_medicamento_list"),
    path('marca_medicamento_create/', MarcaMedicamentoCreateView.as_view(), name="marca_medicamento_create"),
    path('marca_medicamento_update/<int:pk>/', MarcaMedicamentoUpdateView.as_view(), name='marca_medicamento_update'),
    path('marca_medicamento_delete/<int:pk>/', MarcaMedicamentoDeleteView.as_view(), name='marca_medicamento_delete'),
    path('marca_medicamento_detail/<int:pk>/', MarcaMedicamentoDetailView.as_view(), name='marca_medicamento_detail'),
    
    # Rutas de empleados
    path('empleado_list/', EmpleadoListView.as_view(), name="empleado_list"),
    path('empleado_create/', EmpleadoCreateView.as_view(), name="empleado_create"),
    path('empleado_update/<int:pk>/', EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('empleado_delete/<int:pk>/', EmpleadoDeleteView.as_view(), name='empleado_delete'),
    path('empleado_detail/<int:pk>/', EmpleadoDetailView.as_view(), name='empleado_detail'),
    
    

     # Rutas de cargos
    path('cargo_list/', CargoListView.as_view(), name="cargo_list"),
    path('cargo_create/', CargoCreateView.as_view(), name="cargo_create"),
    path('cargo_update/<int:pk>/', CargoUpdateView.as_view(), name='cargo_update'),
    path('cargo_delete/<int:pk>/', CargoDeleteView.as_view(), name='cargo_delete'),
    path('cargo_detail/<int:pk>/', CargoDetailView.as_view(), name='cargo_detail'),

    # Rutas para Medicamentos
    path('medicamento_list/', MedicamentoListView.as_view(), name='medicamento_list'),  
    path('medicamento_create/', MedicamentoCreateView.as_view(), name='medicamento_create'), 
    path('medicamento_update/<int:pk>/', MedicamentoUpdateView.as_view(), name='medicamento_update'), 
    path('medicamento_delete/<int:pk>/', MedicamentoDeleteView.as_view(), name='medicamento_delete'),  
    path('medicamento_detail/<int:pk>/', MedicamentoDetailView.as_view(), name='medicamento_detail'),  

    #Rutas de Diagnostico
    path('diagnostico_list/', DiagnosticoListView.as_view(), name='diagnostico_list'),
    path('diagnostico_create/', DiagnosticoCreateView.as_view(), name='diagnostico_create'),
    path('diagnostico_update/<int:pk>/', DiagnosticoUpdateView.as_view(), name='diagnostico_update'),
    path('diagnostico_delete/<int:pk>/', DiagnosticoDeleteView.as_view(), name='diagnostico_delete'),
    path('diagnostico_detail/<int:pk>/', DiagnosticoDetailView.as_view(), name='diagnostico_detail'),
    
    # Rutas de Auditorías de Usuarios (AuditUser)
    path('audit_user_list/', AuditUserListView.as_view(), name='audit_user_list'),
    path('audit_user_create/', AuditUserCreateView.as_view(), name='audit_user_create'),
    path('audit_user_update/<int:pk>/', AuditUserUpdateView.as_view(), name='audit_user_update'),
    path('audit_user_delete/<int:pk>/', AuditUserDeleteView.as_view(), name='audit_user_delete'),
    path('audit_user_detail/<int:pk>/', AuditUserDetailView.as_view(), name='audit_user_detail'),
    
    



]
