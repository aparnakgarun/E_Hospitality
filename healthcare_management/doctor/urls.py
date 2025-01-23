from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),  # Doctor Dashboard
    path('appointments/', views.view_appointments, name='view_appointments'),  # View Appointments
    path("medical-history/<int:patient_id>/", views.doctor_manage_medical_history, name="doctor_manage_medical_history"),
    path("medical-history/delete/<int:history_id>/", views.doctor_delete_medical_history, name="doctor_delete_medical_history"),
    path('patient/<str:patient_id>/', views.patient_details, name='patient_details'),  # View Patient Details
]
