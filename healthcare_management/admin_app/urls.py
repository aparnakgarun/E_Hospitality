from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path("facilities/", views.facility_list, name="facility_list"),
    path("facilities/add/", views.add_facility, name="add_facility"),
    path("facilities/edit/<int:facility_id>/", views.edit_facility, name="edit_facility"),
    path("facilities/delete/<int:facility_id>/", views.delete_facility, name="delete_facility"),
    path("appointments/", views.manage_appointments, name="manage_appointments"),
    path("appointments/add/", views.add_appointment, name="add_appointment"),
    path("appointments/edit/<int:appointment_id>/", views.edit_appointment, name="edit_appointment"),
    path("appointments/delete/<int:appointment_id>/", views.delete_appointment, name="delete_appointment"),
]

