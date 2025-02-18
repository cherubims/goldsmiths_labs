from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    register_view, 
    login_view, 
    logout_view, 
    teacher_dashboard, 
    student_dashboard, 
    profile_view, 
    dashboard_view, 
    home_view,
)

urlpatterns = [
    # Home page
    path('', home_view, name='home'),
    
    # Authentication views
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Profile and dashboard views
    path('profile/', profile_view, name='profile'),
    path('dashboard/', dashboard_view, name='dashboard'),  # Unified dashboard (handles role-based redirect)
    path('teacher/dashboard/', teacher_dashboard, name='teacher_dashboard'),  # Teacher-specific dashboard
    path('student/dashboard/', student_dashboard, name='student_dashboard'),  # Student-specific dashboard

]
