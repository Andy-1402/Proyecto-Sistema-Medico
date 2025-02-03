from django.urls import path
from .views import (
    PayPalPagoView, 
    PayPalEjecutarPagoView, 
    PayPalCancelarPagoView
)

app_name = 'pagos'

urlpatterns = [
    path('iniciar/<int:paciente_id>/', PayPalPagoView.as_view(), name='iniciar_pago'),
    path('ejecutar/', PayPalEjecutarPagoView.as_view(), name='ejecutar_pago'),
    path('cancelar/', PayPalCancelarPagoView.as_view(), name='cancelar_pago'),
]