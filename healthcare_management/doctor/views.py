from django.shortcuts import render,redirect
from .models import Appointment  # Assuming an Appointment model exists
from django.shortcuts import render, get_object_or_404
from patient.models import Patient  # Assuming the Patient model is defined in patient/models.py
from patient.models import Appointment  # Assuming Appointments are linked to patients
from django.contrib.auth.decorators import login_required
from doctor.models import Doctor
from patient.models import MedicalHistory
from django.contrib import messages

#@login_required(login_url='/auth/login/')

def doctor_dashboard(request):
    username = request.session.get("username")  # Fetch username from session
    print(f"Session username: {username}")  # Debugging: Check if username is retrieved

    if not username:
        print("No username found in session. Redirecting to login.")
        return redirect("login")  # Redirect if not logged in

    # Fetch the logged-in doctor's details
    doctor = Doctor.objects.filter(username=username).first()
    if not doctor:
        print("Doctor not found. Redirecting to login.")
        return redirect("login")

    # Fetch appointments for the logged-in doctor
    appointments = Appointment.objects.filter(doctor=doctor).select_related("patient")

    return render(request, "doctor/dashboard.html", {
        "doctor": doctor,
        "appointments": appointments,

    })


def view_appointments(request):
    # Fetch appointments for the logged-in doctor
    appointments = Appointment.objects.filter(doctor=request.user)
    return render(request, 'doctor/appointments.html', {'appointments': appointments})

def patient_details(request, patient_id):
    # Fetch the patient using their auto_id
    patient = get_object_or_404(Patient, auto_id=patient_id)

    # Fetch the patient's appointments or other related data
    appointments = Appointment.objects.filter(patient=patient)

    return render(request, 'doctor/patient_details.html', {
        'patient': patient,
        'appointments': appointments,
    })

def doctor_manage_medical_history(request, patient_id):
    username = request.session.get("username")
    if not username:
        return redirect("login")

    doctor = Doctor.objects.filter(username=username).first()
    if not doctor:
        return redirect("login")

    patient = Patient.objects.filter(id=patient_id).first()
    if not patient:
        return redirect("doctor_dashboard")

    medical_history = MedicalHistory.objects.filter(patient=patient)

    if request.method == "POST":
        # Handle edit or add logic
        diagnosis = request.POST.get("diagnosis")
        medications = request.POST.get("medications")
        allergies = request.POST.get("allergies")
        history_id = request.POST.get("history_id")
        if history_id:
            history_record = get_object_or_404(MedicalHistory, id=history_id, doctor=doctor)
            #history_record = MedicalHistory.objects.filter(id=history_id).first()
            if history_record:
                history_record.diagnosis = diagnosis
                history_record.medications = medications
                history_record.allergies = allergies
                history_record.doctor = doctor
                history_record.save()
        else:
            MedicalHistory.objects.create(
                patient=patient,
                doctor=doctor,
                diagnosis=diagnosis,
                medications=medications,
                allergies=allergies,
            )
            messages.success(request, "New medical history added successfully.")
        return redirect("doctor_manage_medical_history", patient_id=patient.id)

    return render(request, "doctor/manage_medical_history.html", {
        "doctor": doctor,
        "patient": patient,
        "medical_history": medical_history,
    })

def doctor_delete_medical_history(request, history_id):
    username = request.session.get("username")
    if not username:
        return redirect("login")

    history_record = MedicalHistory.objects.filter(id=history_id).first()
    if history_record and history_record.doctor == doctor:
        history_record.delete()
        messages.success(request, "Medical history deleted successfully.")
    else:
        messages.error(request, "Not allowed to delete this medical history.")

    return redirect("doctor_dashboard")

# Create your views here.
