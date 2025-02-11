from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserRegistrationTests(APITestCase):

    def test_register_valid_user(self):
        """Test successful user registration"""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123",
            "password2": "securepassword123",
            "is_student": True
        }
        response = self.client.post("/api/register/", data)
        print("DEBUG Registration Response:", response.status_code, response.data)  # Debugging

        # Allow both 200 and 201 for success
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])



    def test_register_existing_user(self):
        """Test registering a username that already exists"""
        User.objects.create_user(username="existinguser", email="user@example.com", password="securepassword")
        data = {
            "username": "existinguser",
            "email": "newuser@example.com",
            "password1": "securepassword123",
            "password2": "securepassword123",
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_invalid_email(self):
        """Test registration with an invalid email format"""
        data = {
            "username": "invalidemail",
            "email": "not-an-email",
            "password1": "securepassword123",
            "password2": "securepassword123",
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_mismatched_passwords(self):
        """Test registration when passwords do not match"""
        data = {
            "username": "mismatchuser",
            "email": "mismatch@example.com",
            "password1": "securepassword123",
            "password2": "wrongpassword",
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




class UserLoginTests(APITestCase):

    def setUp(self):
        """Create a test user"""
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")

    def test_login_valid_credentials(self):
        """Test successful login"""
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post("/api/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)  # Require a token

    def test_login_invalid_password(self):
        """Test login with wrong password"""
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post("/api/login/", data)
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED])

    def test_login_nonexistent_user(self):
        """Test login for a non-existent user"""
        data = {"username": "doesnotexist", "password": "testpass123"}
        response = self.client.post("/api/login/", data)
        print("DEBUG Response:", response.status_code, response.data)  # Debugging
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED])



class UserProfileTests(APITestCase):

    def setUp(self):
        """Create and authenticate a user"""
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.force_authenticate(user=self.user)  # Ensure the user is authenticated

    def generate_image_file(self):
        """Generate an in-memory image file"""
        image = Image.new("RGB", (100, 100), color=(255, 0, 0))
        image_io = io.BytesIO()
        image.save(image_io, format="JPEG")
        image_io.seek(0)
        return SimpleUploadedFile("test.jpg", image_io.read(), content_type="image/jpeg")



class APITests(APITestCase):

    def setUp(self):
        """Set up a test user and authenticate"""
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")  # Authenticate using token

    def test_get_courses(self):
        """Test fetching courses with authentication"""
        response = self.client.get("/api/courses/") 
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
