from django.contrib import admin
from .models import Course, Material, Progress, Feedback

# Register models
admin.site.register(Course)
admin.site.register(Material)
admin.site.register(Progress)
admin.site.register(Feedback)
