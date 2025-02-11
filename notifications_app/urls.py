from django.urls import path
from .views import get_notifications_page, mark_notification_as_read, notifications_list

urlpatterns = [
    path('', get_notifications_page, name='notifications'),
    path('read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
    # Retrieve notifications (optional if not being used actively)
    path('get/', get_notifications_page, name='get_notifications'),

    # Endpoint to mark a specific notification as read
    path('mark-as-read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),

    # Display all notifications
    path('all/', notifications_list, name='notifications_list'),
]
