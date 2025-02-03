from django.views.generic import View, TemplateView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import paypalrestsdk
from django.conf import settings

class PayPalPagoView(LoginRequiredMixin, View):
    """Vista para iniciar un pago con PayPal"""
    def get(self, request, paciente_id):
        # Configurar PayPal
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE, 
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })
        
        # Obtener detalles del paciente (simular consulta)
        monto = 50.00
        descripcion = f"Consulta médica - Paciente {paciente_id}"
        
        # Crear pago
        pago = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse_lazy('pagos:ejecutar_pago')),
                "cancel_url": request.build_absolute_uri(reverse_lazy('pagos:cancelar_pago'))
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": descripcion,
                        "sku": "item",
                        "price": str(monto),
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": str(monto),
                    "currency": "USD"
                },
                "description": descripcion
            }]
        })

        # Intentar crear el pago
        if pago.create():
            # Buscar el enlace de aprobación
            for enlace in pago.links:
                if enlace.rel == "approval_url":
                    return redirect(enlace.href)
        
        # Si falla, mostrar error
        return render(request, 'pagos/error_pago.html', {'errores': pago.error})

class PayPalEjecutarPagoView(LoginRequiredMixin, View):
    """Vista para ejecutar el pago de PayPal"""
    def get(self, request):
        # Configurar PayPal
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE, 
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })
        
        # Obtener parámetros de la URL
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')
        
        # Buscar el pago
        pago = paypalrestsdk.Payment.find(payment_id)
        
        # Ejecutar el pago
        if pago.execute({"payer_id": payer_id}):
            # Pago exitoso
            return render(request, 'pagos/pago_exitoso.html', {
                'payment_id': payment_id
            })
        else:
            # Error en el pago
            return render(request, 'pagos/error_pago.html', {
                'errores': pago.error
            })

class PayPalCancelarPagoView(LoginRequiredMixin, TemplateView):
    """Vista para mostrar cuando se cancela un pago"""
    template_name = 'pagos/pago_cancelado.html'