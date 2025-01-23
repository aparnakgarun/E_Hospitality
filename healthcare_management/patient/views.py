from django.shortcuts import render, redirect
from .models import Patient
from .models import Appointment
from django.shortcuts import render
from patient.models import Patient, Appointment
from django.shortcuts import redirect
from doctor.models import Doctor
from patient.models import Appointment
from patient.models import MedicalHistory
import stripe
from django.conf import settings
from datetime import date
from .models import Billing
def patient_dashboard(request):
    username = request.session.get("username")
    patient = Patient.objects.filter(username=username).first()
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.filter(patient=patient)
    medical_history = MedicalHistory.objects.filter(patient=patient)
    health_resources = [
        {"title": "Heart Health", "url": "https://www.youtube.com/watch?v=SBtRkjXSMmk"},
        {"title": "Daily intake food calculations", "url": "https://www.youtube.com/watch?v=LekBg-o9Cp0"},
        {"title": "Exercise for Wellness", "url": "https://www.youtube.com/watch?v=H2U3HwAyBXg"},
        {"title": "Life style diseases", "url": "https://www.youtube.com/watch?v=hsmxtbdyjQU"},
    ]
    billing_details = Billing.objects.filter(patient=patient)

    return render(request, "patient/dashboard.html", {
        "patient": patient,
        "doctors": doctors,
        "appointments": appointments,
        "medical_history": medical_history,
        "health_resources": health_resources,
        "billing_details": billing_details,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
    })


def patient_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")

        Patient.objects.create(
            username=username,
            password=password,
            phone=phone,
            email=email,
            address=address
        )
        return redirect("login")

    return render(request, 'patient/register.html')

def manage_appointments(request):
    if request.method == "POST":
        if "edit" in request.POST:
            appointment_id = request.POST.get("appointment_id")
            return redirect(f'/patient/appointments/{appointment_id}/edit/')
        elif "delete" in request.POST:
            appointment_id = request.POST.get("appointment_id")
            Appointment.objects.filter(id=appointment_id).delete()

    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'patient/book_appointment.html', {'appointments': appointments})

def book_appointment(request):
    if request.method == "POST":
        username = request.session.get("username")
        patient = Patient.objects.filter(username=username).first()
        doctor_id = request.POST.get("doctor")
        appointment_date = request.POST.get("appointment_date")
        details = request.POST.get("details")


        doctor = Doctor.objects.get(id=doctor_id)
        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            details=details,
        )

        return redirect("patient_dashboard")

    return redirect("patient_dashboard")


def edit_appointment(request, appointment_id):
    if request.method == "POST":
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.appointment_date = request.POST.get("appointment_date")
        appointment.details = request.POST.get("details")
        appointment.save()
        return redirect("patient_dashboard")
    return render(request, "patient/edit_appointment.html", {"appointment": appointment})

def delete_appointment(request, appointment_id):
    if request.method == "POST":
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.delete()
        return redirect("patient_dashboard")


def patient_medical_history(request):
    username = request.session.get("username")
    if not username:
        return redirect("login")

    patient = Patient.objects.filter(username=username).first()
    if not patient:
        return redirect("login")

    medical_history = MedicalHistory.objects.filter(patient=patient)

    return render(request, "patient/medical_history.html", {
        "patient": patient,
        "medical_history": medical_history,
    })


stripe.api_key = settings.STRIPE_SECRET_KEY

def billing_dashboard(request):
    username = request.session.get("username")
    if not username:
        return redirect("login")


    patient = Patient.objects.filter(username=username).first()
    if not patient:
        return redirect("login")


    return render(request, "patient/billing_dashboard.html", {
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
    })

def create_checkout_session(request):
    if request.method == "POST":

        amount = int(float(request.POST.get("amount")) * 100)
        bill_number = request.POST.get("bill_number")
        bill_date = request.POST.get("bill_date")


        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "INR",
                        "product_data": {
                            "name": f"Bill #{bill_number} ({bill_date})",
                        },
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url="http://127.0.0.1:8000/patient/billing-success/",
            cancel_url="http://127.0.0.1:8000/patient/billing-cancel/",
        )
        return redirect(session.url, code=303)

    return redirect("billing_dashboard")

def billing_success(request):
    return render(request, "patient/billing_success.html", {"message": "Payment successful!"})


def billing_cancel(request):
    return render(request, "patient/billing_cancel.html", {"message": "Payment canceled. Try again!"})


def add_bill(request):
    if request.method == "POST":
        username = request.session.get("username")
        if not username:
            return redirect("login")

        # Fetch the patient
        patient = Patient.objects.filter(username=username).first()
        if not patient:
            return redirect("login")


        Billing.objects.create(
            patient=patient,
            bill_number=request.POST.get("bill_number"),
            bill_date=request.POST.get("bill_date"),
            amount=request.POST.get("amount"),
        )
        print("New bill added successfully")
        return redirect("billing_dashboard")
