from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register CustomUser using Django's UserAdmin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Display fields in the admin list view
    list_display = ('username', 'email', 'is_teacher', 'is_student', 'is_staff')
    
    # Add filters for easier navigation in admin
    list_filter = ('is_teacher', 'is_student', 'is_staff')
    
    # Fields to show when creating or editing a user
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('is_teacher', 'is_student', 'profile_picture'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('is_teacher', 'is_student', 'profile_picture'),
        }),
    )
