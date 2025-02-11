from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from notifications_app.models import Notification
from rest_framework.authtoken.models import Token

User = get_user_model()

class NotificationTests(APITestCase):

    def setUp(self):
        # Create users for testing
        self.teacher = User.objects.create_user(username="teacher", password="pass123", is_teacher=True)
        self.student = User.objects.create_user(username="student", password="pass123", is_student=True)

        # Create a notification for the student
        self.notification = Notification.objects.create(
            message="Test Notification for Student",
            recipient=self.student
        )

        # Generate token for authentication
        self.student_token = Token.objects.create(user=self.student)
        self.teacher_token = Token.objects.create(user=self.teacher)

    def test_create_notification(self):
        # Test that notification is created successfully
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.message, "Test Notification for Student")
        self.assertEqual(notification.recipient, self.student)
        self.assertFalse(notification.is_read)

    def test_retrieve_notifications_for_user(self):
        # Test that notifications for a user can be retrieved
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.student_token.key)  # Adding token to request
        response = self.client.get(f"/api/notifications/?user_id={self.student.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["message"], "Test Notification for Student")
        self.assertEqual(response.data[0]["is_read"], False)

    def test_create_notification_for_teacher(self):
        # Create a notification for the teacher
        notification_for_teacher = Notification.objects.create(
            message="Test Notification for Teacher",
            recipient=self.teacher
        )
        self.assertEqual(Notification.objects.count(), 2)
        self.assertEqual(notification_for_teacher.message, "Test Notification for Teacher")
        self.assertEqual(notification_for_teacher.recipient, self.teacher)
        self.assertFalse(notification_for_teacher.is_read)

    def test_user_gets_no_notifications(self):
        # Test that a user who has no notifications returns an empty list
        user_without_notifications = User.objects.create_user(username="newuser", password="newpassword")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.teacher_token.key)  # Add the token to request
        response = self.client.get(f"/api/notifications/?user_id={user_without_notifications.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No notifications

    def test_notification_count(self):
        # Create multiple notifications for the student
        Notification.objects.create(message="Notification 1", recipient=self.student)
        Notification.objects.create(message="Notification 2", recipient=self.student)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.student_token.key)  # Adding token to request
        response = self.client.get(f"/api/notifications/?user_id={self.student.id}")
        self.assertEqual(len(response.data), 3)  # Including the initial one
