from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ComplaintForm, UserUpdateForm, ProfileUpdateForm
from .models import Complaint


# ===========================
# HOME PAGE
# ===========================
def home(request):
    return render(request, 'complaints/home.html')


# ===========================
# LOGIN
# ===========================
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'complaints/login.html')


# ===========================
# REGISTER
# ===========================
def user_register(request):
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        full_name = request.POST.get("Full Name")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "complaints/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "complaints/register.html")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
        )
        user.save()

        messages.success(request, "Registration Successful! Login now.")
        return redirect("login")

    return render(request, "complaints/register.html")


# ===========================
# DASHBOARD (Show user complaints)
# ===========================
@login_required
def dashboard(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'complaints/dashboard.html', {
        'complaints': complaints
    })


# ===========================
# VIEW COMPLAINTS (Separate page)
# ===========================
@login_required
def view_complaints(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'complaints/view_complaints.html', {
        'complaints': complaints
    })


# ===========================
# SUBMIT COMPLAINT
# ===========================
@login_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)

        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()

            messages.success(request, "Complaint submitted successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Error! Please fill all fields correctly.")

    else:
        form = ComplaintForm()

    return render(request, 'complaints/submit_complaint.html', {'form': form})


# ===========================
# PROFILE PAGE
# ===========================
@login_required
def profile(request):
    user = request.user
    profile = user.profile  # Access user's profile

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Error updating profile. Please check your inputs.")
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile)

    return render(request, "complaints/profile.html", {
        "u_form": u_form,
        "p_form": p_form,
    })


# ===========================
# LOGOUT
# ===========================
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')
