from django.shortcuts import render, redirect
from patient.models import Patient
from doctor.models import Doctor
from admin_app.models import Admin
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib import messages


def home_view(request):
    return redirect("login")

def login_view(request):
    print("Login view accessed")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")
        print(f"Role: {role}, Username: {username}, Password: {password}")

        if role == "patient":
            user = Patient.objects.filter(username=username, password=password).first()
            if user:
                request.session["username"] = username
                return redirect("patient_dashboard")

        elif role == "doctor":
            user = Doctor.objects.filter(username=username, password=password).first()
            if user:
                print("Doctor authenticated successfully")
                request.session["username"] = username
                return redirect("doctor_dashboard")
        elif role == "admin":
            user = Admin.objects.filter(username=username, password=password).first()
            if user:
                request.session["username"] = username
                return redirect("admin_dashboard")


        print("Invalid credentials or role")
        return render(request, "authentication/login.html", {"error": "Invalid credentials or role"})

    return render(request, "authentication/login.html")

def register_view(request):
    if request.method == "POST":
        role = request.POST.get("role")
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if role == "patient":
            Patient.objects.create(username=username, password=password, email=email)
        elif role == "doctor":
            Doctor.objects.create(username=username, password=password, email=email)
        elif role == "admin":
            Admin.objects.create(username=username, password=password, email=email)

        return redirect("login")

    #return render(request, "authentication/login.html")
    return render(request, "authentication/register.html")


def change_password(request):
    if request.method == "POST":
        username = request.session.get("username")
        role = request.session.get("role")

        if not username or not role:
            messages.error(request, "You must be logged in to change your password.")
            return redirect("login")

        user_model = None
        if role == "patient":
            user_model = Patient
        elif role == "doctor":
            user_model = Doctor
        elif role == "admin":
            user_model = Admin

        if user_model:
            user = user_model.objects.filter(username=username).first()
            if not user:
                messages.error(request, "User not found.")
                return redirect("login")


            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")


            if not check_password(old_password, user.password):
                messages.error(request, "Incorrect old password.")
                return redirect("change_password")


            if new_password != confirm_password:
                messages.error(request, "New password and confirmation do not match.")
                return redirect("change_password")


            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Password updated successfully.")
            return redirect("login")

    return render(request, "authentication/change_password.html")



# Create your views here.
