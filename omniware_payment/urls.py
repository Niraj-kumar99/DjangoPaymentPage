from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_request_view, name='payment_request'),
] 