from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def chat_home(request):
    # Get search query
    search_query = request.GET.get("search", "").strip()

    # Exclude glsadmin from the list of users
    users = User.objects.exclude(username='glsadmin')

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Separate users into Teachers and Students
    teachers = users.filter(is_teacher=True)
    students = users.filter(is_student=True)

    return render(request, 'realtime_app/chat_home.html', {
        "teachers": teachers,
        "students": students,
        "search_query": search_query,
    })



@login_required
def chat_room(request, username):
    other_user = get_object_or_404(User, username=username)
    room_name = f"{min(request.user.username, other_user.username)}_{max(request.user.username, other_user.username)}"

    # Fetch messages between the two users
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    return render(request, 'realtime_app/chat_room.html', {
        'other_user': other_user,
        'room_name': room_name,
        'messages': messages,
    })
