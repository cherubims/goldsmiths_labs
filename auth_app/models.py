from django.db import models
from django.contrib.auth.models import AbstractUser
import os

class CustomUser(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username

    def get_role_display(self):
        if self.is_teacher:
            return "Teacher"
        elif self.is_student:
            return "Student"
        return "Unknown Role"

    def get_profile_picture_url(self):
        """Return the profile picture URL, or a default based on the user's role."""
        if self.profile_picture and self.profile_picture.url:
            return self.profile_picture.url
        elif self.is_teacher:
            return "/media/profile_pics/teacher-default.png"
        return "/media/profile_pics/student-default.png"

    def delete_profile_picture(self):
        """Deletes the profile picture from storage."""
        if self.profile_picture:
            file_path = self.profile_picture.path
            if os.path.exists(file_path):
                os.remove(file_path)
            self.profile_picture = None
            self.save()

