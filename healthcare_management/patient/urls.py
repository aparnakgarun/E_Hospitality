from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('register/', views.patient_register, name='patient_register'),
    path('appointments/', views.manage_appointments, name='manage_appointments'),
    path("book-appointment/", views.book_appointment, name="book_appointment"),
    path("edit-appointment/<int:appointment_id>/", views.edit_appointment, name="edit_appointment"),
    path("medical-history/", views.patient_medical_history, name="patient_medical_history"),
    path("delete-appointment/<int:appointment_id>/", views.delete_appointment, name="delete_appointment"),
    path("billing/", views.billing_dashboard, name="billing_dashboard"),
    path("create-checkout-session/", views.create_checkout_session, name="create_checkout_session"),
    path("billing-success/", views.billing_success, name="billing_success"),
    path("billing-cancel/", views.billing_cancel, name="billing_cancel"),
    path("add-bill/", views.add_bill, name="add_bill"),

]
