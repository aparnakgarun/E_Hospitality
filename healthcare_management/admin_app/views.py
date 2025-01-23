from patient.models import Patient,Appointment
from doctor.models import Doctor
from admin_app.models import Admin
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Facility
from django.contrib import messages
def admin_dashboard(request):

    username = request.session.get("username")
    if not username:
        return redirect("login")


    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_facilities = Facility.objects.count()
    total_appointments = Appointment.objects.count()

    return render(request, 'admin_app/dashboard.html', {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_facilities": total_facilities,
        "total_appointments": total_appointments,
    })
def manage_users(request):
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    admins = Admin.objects.all()

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user_type = request.POST.get("user_type")
        action = request.POST.get("action")

        if user_type == "patient":
            user = get_object_or_404(Patient, id=user_id)
        elif user_type == "doctor":
            user = get_object_or_404(Doctor, id=user_id)
        elif user_type == "admin":
            user = get_object_or_404(Admin, id=user_id)
        else:
            return redirect("manage_users")

        if action == "deactivate":
            user.is_active = False
            user.save()
        elif action == "activate":
            user.is_active = True
            user.save()
        elif action == "reset_password":
            user.password = "123"
            user.save()

        return redirect("manage_users")

    return render(request, "admin_app/manage_users.html", {
        "patients": patients,
        "doctors": doctors,
        "admins": admins,
    })


def facility_list(request):
    facilities = Facility.objects.all()
    return render(request, "admin_app/facility_list.html", {"facilities": facilities})

# Add a new facility
def add_facility(request):
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        department = request.POST.get("department")
        resources = request.POST.get("resources")

        Facility.objects.create(
            name=name,
            location=location,
            department=department,
            resources=resources,
        )
        return redirect("facility_list")

    return render(request, "admin_app/add_facility.html")

def edit_facility(request, facility_id):
    facility = get_object_or_404(Facility, id=facility_id)

    if request.method == "POST":
        facility.name = request.POST.get("name")
        facility.location = request.POST.get("location")
        facility.department = request.POST.get("department")
        facility.resources = request.POST.get("resources")
        facility.save()
        return redirect("facility_list")

    return render(request, "admin_app/edit_facility.html", {"facility": facility})

def delete_facility(request, facility_id):
    facility = get_object_or_404(Facility, id=facility_id)
    facility.delete()
    return redirect("facility_list")

def manage_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, "admin_app/manage_appointments.html", {"appointments": appointments})

def add_appointment(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient")
        doctor_id = request.POST.get("doctor")
        #department = request.POST.get("department")
        appointment_date = request.POST.get("appointment_date")
        details = request.POST.get("details")

        patient = get_object_or_404(Patient, id=patient_id)
        doctor = get_object_or_404(Doctor, id=doctor_id)

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            department=department,
            appointment_date=appointment_date,
            details=details
        )
        messages.success(request, "Appointment added successfully!")
        return redirect("manage_appointments")

    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    return render(request, "admin_app/add_appointment.html", {"patients": patients, "doctors": doctors})

def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == "POST":
        appointment.patient_id = request.POST.get("patient")
        appointment.doctor_id = request.POST.get("doctor")
        #appointment.department = request.POST.get("department")
        appointment.appointment_date = request.POST.get("appointment_date")
        appointment.details = request.POST.get("details")
        appointment.save()
        messages.success(request, "Appointment updated successfully!")
        return redirect("manage_appointments")

    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    return render(request, "admin_app/edit_appointment.html", {
        "appointment": appointment,
        "patients": patients,
        "doctors": doctors
    })

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    messages.success(request, "Appointment deleted successfully!")
    return redirect("manage_appointments")

# Create your views here.
