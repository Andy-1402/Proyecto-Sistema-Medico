import paypalrestsdk
from django.conf import settings

def configurar_paypal():
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE, 
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET
    })

def crear_pago(monto, descripcion):
    pago = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:8000/pago/ejecutar",
            "cancel_url": "http://localhost:8000/pago/cancelar"
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

    return pago