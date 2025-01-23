from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    is_active = models.BooleanField(default=True)
    auto_id = models.CharField(max_length=10, unique=True, editable=False)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def save(self, *args, **kwargs):
        if not self.auto_id:
            self.auto_id = f"PAT-{Patient.objects.count() + 1:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Appointment(models.Model):
    patient = models.ForeignKey("patient.Patient", on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey("doctor.Doctor", on_delete=models.CASCADE, related_name='doctor_patient_appointments')
    appointment_date = models.DateField()
    details = models.TextField()
    #department = models.CharField(max_length=255)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor_name} on {self.appointment_date}"


class MedicalHistory(models.Model):
    patient = models.ForeignKey(
        "patient.Patient",
        on_delete=models.CASCADE,
        related_name="medical_history"
    )
    doctor = models.ForeignKey(
        "doctor.Doctor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="medical_records"
    )
    diagnosis = models.TextField()
    medications = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    treatment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Medical History for {self.patient.username} on {self.treatment_date}"

class Billing(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE, related_name="billings")
    bill_number = models.CharField(max_length=50)
    bill_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("Paid", "Paid"), ("Pending", "Pending")], default="Pending")

    def __str__(self):
        return f"Bill #{self.bill_number} - {self.status}"
