from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Service, Project, WasteMaterial, UserProfile
from django.contrib import messages

# Home Views
def home(request):
    services = Service.objects.all()
    return render(request, 'home.html', {'services': services})

def home2(request):
    services = Service.objects.all()
    return render(request, 'home2.html', {'services': services})

def about_us(request):
    return render(request, 'about_us.html')

def faq(request):
    return render(request, 'faq.html')

# User Registration
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['user_type']
        profile_picture = request.FILES.get('profile_picture')  # Handle the uploaded profile picture

        # Create the user and associated profile
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(
            user=user,
            user_type=user_type,
            profile_picture=profile_picture
        )

        messages.success(request, 'Registration successful!')
        login(request, user)  # Log the user in automatically
        return redirect('dashboard')  # Redirect to the dashboard
    return render(request, 'register.html')

# User Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Redirect to home2 page after successful login
            return redirect('home2')
        messages.error(request, 'Invalid credentials!')
    return render(request, 'login.html')

@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    projects = Project.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'user_profile': user_profile, 'projects': projects})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

# CRUD Operations for Service
@login_required
def add_service(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        image = request.FILES.get('image')
        Service.objects.create(title=title, description=description, price=price, image=image)
        return redirect('home')
    return render(request, 'add_service.html')

@login_required
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        service.title = request.POST['title']
        service.description = request.POST['description']
        service.price = request.POST['price']
        if 'image' in request.FILES:
            service.image = request.FILES['image']
        service.save()
        return redirect('home')
    return render(request, 'edit_service.html', {'service': service})

@login_required
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    return redirect('home')
