from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    is_blocked = models.BooleanField(default=False)  # New field to mark a student as blocked
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'student')  # Prevents multiple enrollments for the same student and course

    def __str__(self):
        return f"{self.student.username} in {self.course.name}"


class Material(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="materials",
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="materials/", blank=True, null=True)  # PDFs or documents
    video_url = models.URLField(blank=True, null=True)  # Video links
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.name})"


# MaterialProgress
class MaterialProgress(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="material_progress",
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="material_progress_records",  # Custom related_name to avoid clash
    )
    progress_percentage = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.student.username} - {self.material.title}: {self.progress_percentage}%"


class Progress(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_progress",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="progress",
        null=True,  # Allow null temporarily
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="progress_records",  # Custom related_name to avoid clash
        null=True,
    )
    progress_percentage = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("student", "course", "material")

    def __str__(self):
        course_name = self.course.name if self.course else "No course"
        material_title = self.material.title if self.material else "No material"
        return f"{self.student.username} - {course_name} - {material_title}: {self.progress_percentage}%"




class Feedback(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="feedback",  # Reverse accessor for feedback on a course
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="feedback_given",  # Reverse accessor for feedback given by a student
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.student.username} for {self.course.name}"


class StatusUpdate(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="status_updates")
    content = models.TextField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)  # Linked to the teacher
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
