from django.urls import path
from rest_framework.schemas import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view as yasg_schema_view
from drf_yasg import openapi
from .views import (
    course_list_api,
    MaterialListCreateView,
    register_user,
    login_user,
    logout_user,
    ProgressListCreateView,
    FeedbackListCreateView,
    NotificationListView,
    MarkNotificationAsReadView,
)

# Swagger Schema View
schema_view = yasg_schema_view(
    openapi.Info(
        title="Goldsmiths Labs API",
        default_version='v1',
        description="API documentation for Goldsmiths Labs",
        contact=openapi.Contact(email="support@goldsmithslabs.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

# URL Patterns
urlpatterns = [
    path('register/', register_user, name='register_api'),
    path('login/', login_user, name='login_api'),
    path('logout/', logout_user, name='logout_api'),
    
    # Courses API
    path('courses/', course_list_api, name='course_list_api'),
    path('courses/<int:course_id>/materials/', MaterialListCreateView.as_view(), name='course-materials-api'),
    
    # Progress API
    path('progress/', ProgressListCreateView.as_view(), name='progress_api'),
    
    # Feedback API
    path('feedback/', FeedbackListCreateView.as_view(), name='feedback_api'),
    
    # Notifications API
    path('notifications/', NotificationListView.as_view(), name='notifications_api'),
    path('notifications/<int:pk>/mark-as-read/', MarkNotificationAsReadView.as_view(), name='mark_notification_read_api'),
    
    # Swagger API Docs
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_docs'),
]
