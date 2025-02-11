from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import CustomUserCreationForm, ProfileUpdateForm, CustomAuthenticationForm
from .decorators import role_required
from courses_app.models import Course, Feedback
from courses_app.views import student_courses_view

# Register View
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)  # Automatically log in the user
                messages.success(request, "Registration successful!")
                return redirect('profile')  # Redirect to the profile page
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth_app/register.html', {'form': form})


# Login View
def login_view(request):
    role = request.GET.get('role')  # Get role from query parameters (teacher or student)

    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user:
                # If role is passed, check if user matches the role
                if role:
                    if (role.lower() == 'teacher' and not user.is_teacher) or (role.lower() == 'student' and not user.is_student):
                        messages.error(request, "The selected role does not match your account.")
                        return render(request, 'auth_app/login.html', {'form': form, 'role': role})

                # Log the user in and display a success message
                login(request, user)
                messages.success(request, f"Welcome back, {role.capitalize() if role else 'User'}!")
                return redirect('dashboard')  # Redirect to the unified dashboard
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'auth_app/login.html', {'form': form, 'role': role})


# Logout View
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

# Home view
def home_view(request):
    return render(request, 'auth_app/home.html')

# Unified Home View
def home_view(request):
    # If the user is authenticated, redirect based on role
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teacher_dashboard')
        elif request.user.is_student:
            return redirect('student_dashboard')

    # For non-authenticated users, render the public homepage
    return render(request, 'auth_app/public_home.html')


@login_required
def profile_view(request):
    """Handles user profile updates, including uploading and deleting profile pictures."""
    user = request.user

    if request.method == 'POST':
        if 'delete_picture' in request.POST:  # Handle profile picture deletion
            if user.profile_picture:
                user.delete_profile_picture()
                messages.success(request, "Profile picture removed successfully.")
            else:
                messages.error(request, "No profile picture to remove.")
            return redirect('profile')

        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Failed to update profile. Please check the form.")
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'auth_app/profile.html', {'form': form})

# Role-Based Dashboards
@role_required('teacher')
def teacher_dashboard(request):
    return render(request, 'auth_app/teacher_dashboard.html')

@login_required
def student_dashboard(request):
    return redirect('student_courses')

@login_required
def dashboard_view(request):
    if request.user.is_student:
        return student_courses_view(request)
    elif request.user.is_teacher:
        return redirect('teacher_dashboard')
    else:
        return redirect('home')  # Default fallback for other roles
    

@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher:
        return HttpResponseForbidden("You do not have access to this page.")

    # Fetch courses created by the teacher
    courses = Course.objects.filter(teacher=request.user)

    return render(request, 'courses_app/teacher_dashboard.html', {
        'courses': courses,
    })


def custom_page_not_found_view(request, exception):
    return render(request, "404.html", status=404)

def custom_server_error_view(request):
    return render(request, "500.html", status=500)