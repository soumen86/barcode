from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.qr_gen, name='qr_gen'),
    path('foodscan/', views.foodscan, name='qr_gen'),
    path('scancode/<code>/', views.scancode)
]
