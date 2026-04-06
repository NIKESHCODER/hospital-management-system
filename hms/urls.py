from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_home, name='home'),
    path('about/', views.view_about, name='about'),
    path('services/', views.view_services, name='services'),
    path('departments/', views.view_departments, name='departments'),
    path('doctors/', views.view_doctors, name='doctors'),

    path('appointments/', views.view_appointments, name='appointments'),
    path('add/', views.add_appointment, name='add_appointment'),
    path('edit/<int:id>/', views.edit_appointment, name='edit_appointment'),
    path('delete/<int:id>/', views.delete_appointment, name='delete_appointment'),
    # API URLs
    path('api/appointments/', views.api_appointments),
    path('api/add/', views.api_add_appointment),
]