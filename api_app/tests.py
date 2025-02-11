from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from courses_app.models import Course
from rest_framework.authtoken.models import Token 

User = get_user_model()

class APITests(APITestCase):

    def setUp(self):
        # Create users (teacher and student)
        self.teacher = User.objects.create_user(username="teacher", password="pass123", is_teacher=True)
        self.student = User.objects.create_user(username="student", password="pass123", is_student=True)
        
        # Create course and associate it with teacher
        self.course = Course.objects.create(name="React Fundamentals", teacher=self.teacher)

        # Create a token for the teacher and student
        self.teacher_token = Token.objects.create(user=self.teacher)
        self.student_token = Token.objects.create(user=self.student)

    def test_get_courses_as_teacher(self):
        # Use teacher's token in Authorization header
        response = self.client.get("/api/courses/", HTTP_AUTHORIZATION="Token " + self.teacher_token.key)
        
        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  

    def test_get_courses_as_student(self):
        # Use student's token in Authorization header
        response = self.client.get("/api/courses/", HTTP_AUTHORIZATION="Token " + self.student_token.key)
        
        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1) 

