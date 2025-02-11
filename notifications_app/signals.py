from django.db.models.signals import post_save
from django.dispatch import receiver
from realtime_app.models import Message  
from courses_app.models import Progress  
from .models import Notification  

# Signal to handle course completion notifications
@receiver(post_save, sender=Progress)
def create_course_completion_notification(sender, instance, created, **kwargs):
    if created and instance.progress_percentage == 100:  # If progress is 100%
        Notification.objects.create(
            recipient=instance.course.teacher,  # Notify the teacher
            message=f"{instance.student.username} has completed the course {instance.course.name}."
        )


