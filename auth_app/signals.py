from django.db.models.signals import pre_save
from django.dispatch import receiver
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from .models import CustomUser

@receiver(pre_save, sender=CustomUser)
def resize_profile_picture(sender, instance, **kwargs):
    """Resize profile picture to 150x150 pixels before saving."""
    if instance.profile_picture:
        img = Image.open(instance.profile_picture)
        img = img.convert("RGB")  # Ensure the image is in RGB mode

        # Resize image (square)
        img.thumbnail((150, 150))

        # Save resized image back
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        instance.profile_picture.save(instance.profile_picture.name, ContentFile(buffer.getvalue()), save=False)
