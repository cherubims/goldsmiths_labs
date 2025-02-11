from notifications_app.models import Notification

def notifications_context(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(
            recipient=request.user, is_read=False
        ).order_by('-created_at')
    else:
        notifications = []
    return {'unread_notifications': notifications}
