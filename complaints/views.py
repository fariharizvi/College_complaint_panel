from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ComplaintForm
from .models import Complaint
from django.contrib import messages

def home(request):
    return render(request, 'complaints/home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # or any dashboard view you have
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'complaints/login.html')

def user_register(request):
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "complaints/register.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "complaints/register.html", {"error": "Username already taken"})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        return redirect("login")

    return render(request, "complaints/register.html")

@login_required
def dashboard(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        if subject and description:
            Complaint.objects.create(user=request.user, subject=subject, description=description)
            return redirect('dashboard')

    # Show complaints by current user
    complaints = Complaint.objects.filter(user=request.user).order_by('-updated_on')
    return render(request, 'complaints/dashboard.html', {'complaints': complaints})

@login_required
def profile(request):
    # Get complaints submitted by the logged-in user
    complaints = Complaint.objects.filter(user=request.user).order_by('-updated_on')

    context = {
        'complaints': complaints,
    }

    return render(request, 'complaints/profile.html', context)


@login_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.user = request.user
            comp.save()
            return redirect('dashboard')
    else:
        form = ComplaintForm()
    return render(request, 'complaints/submit_complaint.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def view_complaints(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-updated_on')
    return render(request, 'complaints/view_complaints.html', {'complaints': complaints})

