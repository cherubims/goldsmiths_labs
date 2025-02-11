from django import forms
from .models import Course, Material, Progress, Feedback, Announcement

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'file', 'video_url']

class CourseSearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False, label="Search Courses")


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Course Description'}),
        }

from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your feedback here...'}),
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'message']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Announcement Title'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type your announcement here...', 'rows': 4}),
        }