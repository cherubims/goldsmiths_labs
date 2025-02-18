from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from courses_app.models import Course, Material, Progress, Feedback
from courses_app.serializers import CourseSerializer
from notifications_app.models import Notification
from .serializers import MaterialSerializer, RegisterSerializer, LoginSerializer, UserSerializer, ProgressSerializer, FeedbackSerializer, NotificationSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Endpoint to Register a New User"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Endpoint to Log In a User and Get a Token"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data})
        return Response({"error": "Invalid Credentials"}, status=400)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def logout_user(request):
    """Endpoint to Log Out a User"""
    request.user.auth_token.delete()
    logout(request)
    return Response({"message": "Successfully logged out"})

@api_view(['GET'])
def course_list_api(request):
    """Endpoint to fetch all courses"""
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

class MaterialListCreateView(generics.ListCreateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class ProgressListCreateView(generics.ListCreateAPIView):
    """Endpoint to Fetch and Update Student Progress"""
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class FeedbackListCreateView(generics.ListCreateAPIView):
    """Endpoint to Fetch and Submit Feedback"""
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class NotificationListView(generics.ListAPIView):
    """Endpoint to Fetch User Notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')

class MarkNotificationAsReadView(generics.UpdateAPIView):
    """Endpoint to Mark a Notification as Read"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(recipient=self.request.user)