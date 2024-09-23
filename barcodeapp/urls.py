from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.qr_gen, name='qr_gen'),
    path('foodscan/', views.foodscan, name='qr_gen'),
    path('scancode/<code>/', views.scancode),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('footballclubs/', views.footballclubs),
    path('member/', views.member, name='member'),
    path('member/fetchmember/<int:ID>', views.fetchmember,  name='fetchmember'),
    path('invalidation/<code>', views.invalidation,  name='invalidation'),
    path('viewcode/<code>/', views.viewcode),
    path('viewinfo/', views.viewinfo, name='viewinfo'),
]
