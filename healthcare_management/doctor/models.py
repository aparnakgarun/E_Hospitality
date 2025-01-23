from django.db import models
from django.contrib.auth.models import User
from django.db import models
#from patient.models import Patient  # Import the Patient model
#from doctor.models import Doctor   # Import the Doctor model

class Doctor(models.Model):
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=150)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()

class Appointment(models.Model):
    patient = models.ForeignKey("patient.Patient", on_delete=models.CASCADE, related_name='doctor_appointments')
    doctor = models.ForeignKey("doctor.Doctor", on_delete=models.CASCADE, related_name='doctor_appointments',default=1)
    appointment_date = models.DateField()
    details = models.TextField()

    def __str__(self):
        return f"Appointment for {self.patient.username} with Dr. {self.doctor.name} on {self.appointment_date}"
# Create your models here.
