from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from courses_app.models import Course

User = get_user_model()

class CourseViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(username="teacher", password="pass123", is_teacher=True)
        self.student = User.objects.create_user(username="student", password="pass123", is_student=True)
        self.course = Course.objects.create(name="Django Basics", teacher=self.teacher)

    def test_teacher_can_access_dashboard(self):
        self.client.login(username="teacher", password="pass123")
        response = self.client.get("/auth/teacher/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Basics")  # Checks if course is listed

    def test_student_cannot_access_teacher_dashboard(self):
        self.client.login(username="student", password="pass123")
        response = self.client.get("/auth/teacher/dashboard/")
        self.assertEqual(response.status_code, 403)  # Forbidden
