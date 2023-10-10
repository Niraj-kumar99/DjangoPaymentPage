from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_request_view, name='payment_request'),
    path('payment_response/', views.payment_response_view, name='payment_request'),
] 