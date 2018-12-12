from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('payment/cancel', views.payment_cancel, name='payment_cancel'),
    path('payment/checkout', views.payment_checkout, name='payment_checkout'),
]
