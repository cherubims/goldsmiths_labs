from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Count, Q
from .models import Course, Progress, Material, StatusUpdate, Announcement, Feedback, Enrollment
from .forms import CourseForm, MaterialForm, CourseSearchForm, FeedbackForm, AnnouncementForm
from notifications_app.models import Notification

User = get_user_model()

@login_required
def teacher_courses_view(request):
    if not request.user.is_teacher:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('dashboard')

    query = request.GET.get('query', '')
    print(f"Search Query: {query}")  # Debug: Check the query parameter

    if query:
        courses = Course.objects.filter(teacher=request.user, name__icontains=query)
    else:
        courses = Course.objects.filter(teacher=request.user)
    
    print(f"Fetched Courses: {courses}")  # Debug: Check the fetched courses

    form = CourseSearchForm(initial={'query': query})
    return render(request, 'courses_app/teacher_courses.html', {'courses': courses, 'form': form})


@login_required
def create_course_view(request):
    if not request.user.is_teacher:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('dashboard')
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            messages.success(request, "Course created successfully!")
            return redirect('teacher_courses')
    else:
        form = CourseForm()
    return render(request, 'courses_app/create_course.html', {'form': form})


@login_required
def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    materials = course.materials.all()
    progress = None

    # If the user is a student, fetch their progress
    if request.user.is_student:
        progress = Progress.objects.filter(student=request.user, course=course).first()

    return render(request, 'courses_app/course_detail.html', {
        'course': course,
        'materials': materials,
        'progress': progress
    })


@login_required
def upload_material_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    materials = course.materials.all()  # Fetch all materials for this course

    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.save()

            # Create notifications for all enrolled students
            enrolled_students = Enrollment.objects.filter(course=course)
            for enrollment in enrolled_students:
                student = enrollment.student
                Notification.objects.create(
                    recipient=student,
                    message=f"New material uploaded in {course.name}: {material.title}."
                )

            messages.success(request, "Material uploaded successfully!")
            return redirect('upload_material', course_id=course.id)
    else:
        form = MaterialForm()

    return render(request, 'courses_app/upload_material.html', {
        'form': form,
        'course': course,
        'materials': materials,
    })


@login_required
def delete_material_view(request, material_id):
    material = get_object_or_404(Material, id=material_id, course__teacher=request.user)
    course_id = material.course.id  # Get the course ID for redirection
    material.delete()
    messages.success(request, "Material deleted successfully!")
    return redirect('upload_material', course_id=course_id)


@login_required
def teacher_courses_view(request):
    if not request.user.is_teacher:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('dashboard')

    # Get the search query from the request
    search_query = request.GET.get('query', '')

    # Filter courses by the search query
    courses = request.user.courses_created.filter(name__icontains=search_query)

    context = {
        'courses': courses,
        'search_query': search_query,  # Pass the query back to the template
    }
    return render(request, 'courses_app/teacher_courses.html', context)

@login_required
def create_course_view(request):
    if not request.user.is_teacher:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user  # Assign the logged-in teacher
            course.save()
            messages.success(request, "Course created successfully!")
            return redirect('teacher_courses')
        else:
            messages.error(request, "Failed to create course. Please check the form.")
    else:
        form = CourseForm()

    return render(request, 'courses_app/create_course.html', {'form': form})


@login_required
def student_homepage_view(request):
    # Fetch the enrolled courses from the Enrollment model
    enrolled_courses = Enrollment.objects.filter(student=request.user, is_blocked=False).select_related('course')

    # Fetch notifications for the logged-in user
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')

    progress_data = []
    for enrollment in enrolled_courses:
        course = enrollment.course
        total_materials = course.materials.count()  # Fetch materials from the course
        completed_materials = Progress.objects.filter(
            student=request.user, material__course=course, completed=True
        ).count()
        completed_percent = (completed_materials / total_materials * 100) if total_materials > 0 else 0
        progress_data.append({
            'course': course,
            'completed_percent': completed_percent,
            'remaining_percent': 100 - completed_percent,
            'is_completed': completed_percent == 100,
        })

    # Search functionality for announcements
    search_query = request.GET.get("search", "")  # Get the search query from the GET parameters
    if search_query:
        announcements = Announcement.objects.filter(
            Q(title__icontains=search_query) | 
            Q(message__icontains=search_query) |
            Q(created_at__icontains=search_query)
        ).order_by('-created_at')  # Filter announcements based on search query
    else:
        announcements = Announcement.objects.all().order_by('-created_at')

    # Fetch student's status updates
    status_updates = StatusUpdate.objects.filter(student=request.user).order_by('-timestamp')

    # Build context dictionary
    context = {
        'progress_data': progress_data,
        'announcements': announcements,
        'status_updates': status_updates,
        'search_query': search_query,  # Pass the search query back to the template
        'notifications': notifications,  # Include notifications in the context
    }

    return render(request, 'courses_app/student_homepage.html', context)


@login_required
def student_courses_view(request):
    if not request.user.is_student:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('dashboard')

    # Fetch all the enrolled courses (including blocked courses)
    enrolled_courses = Enrollment.objects.filter(student=request.user).select_related('course')

    # Fetch all available courses (including courses the student is not enrolled in)
    available_courses = Course.objects.exclude(enrollments__student=request.user)

    # Search functionality for enrolled and available courses
    search_query = request.GET.get('query', '')
    if search_query:
        enrolled_courses = enrolled_courses.filter(course__name__icontains=search_query)
        available_courses = available_courses.filter(name__icontains=search_query)

    # Progress Data for enrolled courses
    enrolled_courses_with_progress = []
    for enrollment in enrolled_courses:
        course = enrollment.course  # Get the course object
        total_materials = course.materials.count()
        completed_materials = Progress.objects.filter(
            student=request.user, material__course=course, completed=True
        ).count()
        is_completed = total_materials > 0 and completed_materials == total_materials

        enrolled_courses_with_progress.append({
            'course': course,
            'total_materials': total_materials,
            'completed_materials': completed_materials,
            'completed_percent': (completed_materials / total_materials * 100) if total_materials > 0 else 0,
            'is_completed': is_completed,
            'is_blocked': enrollment.is_blocked,
        })

    # Build the context
    context = {
        'enrolled_courses_with_progress': enrolled_courses_with_progress,
        'available_courses': available_courses,
        'search_query': search_query,
    }

    return render(request, 'courses_app/student_courses.html', context)


@login_required
def enroll_course_view(request, course_id):
    if not request.user.is_student:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('dashboard')

    # Fetch the course the student is trying to enroll in
    course = get_object_or_404(Course, id=course_id)

    # Check if the student is already enrolled in the course
    if Enrollment.objects.filter(course=course, student=request.user).exists():
        messages.error(request, f"You are already enrolled in {course.name}.")
        return redirect('student_courses')

    # Create a new enrollment record
    Enrollment.objects.create(course=course, student=request.user)

    # Notify the teacher about the student's enrollment
    Notification.objects.create(
        recipient=course.teacher,
        message=f"{request.user.username} has enrolled in your course: {course.name}."
    )

    messages.success(request, f"You have successfully enrolled in {course.name}!")
    return redirect('student_courses')


@login_required
def view_enrolled_students_view(request, course_id):
    if not request.user.is_teacher:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('dashboard')

    course = get_object_or_404(Course, id=course_id, teacher=request.user)

    # Fetch all enrolled students (including blocked students)
    enrolled_students = Enrollment.objects.filter(course=course).select_related('student')

    return render(request, 'courses_app/enrolled_students.html', {'course': course, 'enrolled_students': enrolled_students})


@login_required
def toggle_block(request, course_id, student_id):
    # Ensure the current user is the teacher of the course
    if not request.user.is_teacher:
        return HttpResponseForbidden("You do not have permission to perform this action.")

    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    enrollment = get_object_or_404(Enrollment, course=course, student__id=student_id)

    # Toggle the block status
    enrollment.is_blocked = not enrollment.is_blocked
    enrollment.save()

    # Notify the teacher about the action
    if enrollment.is_blocked:
        messages.success(request, f"{enrollment.student.username} has been blocked from the course.")
    else:
        messages.success(request, f"{enrollment.student.username} has been unblocked from the course.")

    # Return a JSON response with the updated block status
    return JsonResponse({
        'is_blocked': enrollment.is_blocked,
        'student_id': student_id,
        'course_id': course.id
    })


@login_required
def leave_feedback_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, students=request.user)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.course = course
            feedback.student = request.user
            feedback.save()
            messages.success(request, "Your feedback has been submitted!")
            return redirect('student_dashboard')  # Redirect back to the student dashboard
    else:
        form = FeedbackForm()

    return render(request, 'courses_app/leave_feedback.html', {'form': form, 'course': course})


@login_required
def student_progress_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, students=request.user)
    progress = Progress.objects.filter(student=request.user, course=course).first()

    context = {
        'course': course,
        'progress': progress,
    }
    return render(request, 'courses_app/student_progress.html', context)


@login_required
def teacher_progress_view(request, course_id):
    if not request.user.is_teacher:
        return HttpResponseForbidden("You do not have access to this page.")
    
    # Get the course
    course = get_object_or_404(Course, id=course_id, teacher=request.user)

    # Query progress related to the materials of the course
    progress_records = Progress.objects.filter(
        material__course=course
    ).select_related('student', 'material')

    # Calculate progress for each student
    student_progress = {}
    for record in progress_records:
        student_id = record.student.id
        if student_id not in student_progress:
            student_progress[student_id] = {
                "student": record.student,
                "completed_count": 0,
                "total_count": course.materials.count(),
            }
        if record.completed:
            student_progress[student_id]["completed_count"] += 1

    # Add progress percentages
    for progress in student_progress.values():
        if progress["total_count"] > 0:
            progress["progress_percentage"] = (
                progress["completed_count"] / progress["total_count"] * 100
            )
        else:
            progress["progress_percentage"] = 0

    context = {
        'course': course,
        'student_progress': student_progress.values(),
    }

    return render(request, 'courses_app/teacher_progress.html', context)


@login_required
def course_materials_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, students=request.user)
    materials = course.materials.all()

    # Fetch completed materials for the logged-in student
    completed_material_ids = Progress.objects.filter(
        student=request.user, material__course=course, completed=True
    ).values_list('material_id', flat=True)

    # Handle "Mark as Complete" form submission
    if request.method == 'POST':
        material_id = request.POST.get('material_id')
        material = get_object_or_404(Material, id=material_id, course=course)
        
        # Mark material as completed
        Progress.objects.update_or_create(
            student=request.user,
            material=material,
            defaults={'completed': True},
        )

        # Check if the student has completed all materials
        total_materials = course.materials.count()
        completed_materials = Progress.objects.filter(
            student=request.user, material__course=course, completed=True
        ).count()

        if total_materials > 0 and completed_materials == total_materials:
            print(f"✅ {request.user.username} has completed {course.name}. Sending notification...")  # Debugging..

            # Notify the teacher
            notification = Notification.objects.create(
                recipient=course.teacher,
                message=f"{request.user.username} has completed the course '{course.name}'!"
            )
            notification.save()

        messages.success(request, f'Marked "{material.title}" as complete!')
        return redirect('course_materials', course_id=course.id)

    # Progress calculation
    total_materials = materials.count()
    completed_materials = len(completed_material_ids)

    context = {
        'course': course,
        'materials': materials,
        'completed_material_ids': completed_material_ids,
        'total_materials': total_materials,
        'completed_materials': completed_materials,
    }
    return render(request, 'courses_app/course_materials.html', context)


@login_required
def submit_feedback_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, students=request.user)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.course = course
            feedback.student = request.user
            feedback.save()
            messages.success(request, "Feedback submitted successfully!")
            return redirect('student_dashboard')
    else:
        form = FeedbackForm()

    return render(request, 'courses_app/submit_feedback.html', {'form': form, 'course': course})


@login_required
def view_feedback_view(request, course_id):
    """
    View feedback for a course, accessible only by the teacher who created the course.
    """
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    feedback_list = course.feedback.all()  # Fetch all feedback for the course

    context = {
        'course': course,
        'feedback_list': feedback_list,
    }

    return render(request, 'courses_app/view_feedback.html', context)


@login_required
def leave_feedback_view(request, course_id):
    # Ensure that the student is enrolled in the course before they can leave feedback
    course = get_object_or_404(Course, id=course_id)
    
    # Check if the student is enrolled in this course
    enrollment = Enrollment.objects.filter(course=course, student=request.user, is_blocked=False).first()

    if not enrollment:
        messages.error(request, "You are not enrolled in this course or you're blocked.")
        return redirect('student_courses')  # Redirect to student courses page if not enrolled

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.course = course
            feedback.student = request.user
            feedback.save()
            messages.success(request, "Your feedback has been submitted!")
            return redirect('student_dashboard')  # Redirect back to the student dashboard
    else:
        form = FeedbackForm()

    return render(request, 'courses_app/leave_feedback.html', {'form': form, 'course': course})



@login_required
def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    materials = course.materials.all()

    # Handle POST request for marking materials as complete
    if request.method == "POST":
        material_id = request.POST.get("material_id")
        material = get_object_or_404(Material, id=material_id)
        Progress.objects.get_or_create(student=request.user, material=material, completed=True)

    # Get completed material IDs
    completed_material_ids = Progress.objects.filter(student=request.user, material__in=materials, completed=True).values_list('material_id', flat=True)

    # Calculate progress
    completed_materials = len(completed_material_ids)
    total_materials = materials.count()

    return render(request, 'courses_app/course_detail.html', {
        'course': course,
        'materials': materials,
        'completed_material_ids': completed_material_ids,
        'completed_materials': completed_materials,
        'total_materials': total_materials,
    })


@login_required
def post_status_update_view(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        if content:
            StatusUpdate.objects.create(
                student=request.user,  # Assuming `request.user` is a student
                content=content
            )
            return redirect('student_homepage')  # Redirect back to the homepage
        else:
            return JsonResponse({'error': 'Status content cannot be empty'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=405)


def is_teacher(user):
    return user.is_authenticated and user.is_teacher


@login_required
@user_passes_test(is_teacher)
def teacher_announcements(request):
    announcements = Announcement.objects.filter(teacher=request.user).order_by('-created_at')
    return render(request, 'courses_app/teacher_announcements.html', {'announcements': announcements})

def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, 'courses_app/announcement_detail.html', {'announcement': announcement})

def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)

    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcement_detail', pk=announcement.pk)
    else:
        form = AnnouncementForm(instance=announcement)
    
    return render(request, 'courses_app/edit_announcement.html', {'form': form, 'announcement': announcement})


@login_required
@user_passes_test(is_teacher)
def create_announcement(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.teacher = request.user
            announcement.save()
            return redirect('teacher_announcements')
    else:
        form = AnnouncementForm()
    return render(request, 'courses_app/announcement_form.html', {'form': form})


@login_required
def view_all_feedback(request):
    if not request.user.is_teacher:
        return HttpResponseForbidden("You do not have access to this page.")
    
    # Fetch all feedback for courses created by the teacher
    feedback_list = Feedback.objects.filter(course__teacher=request.user).select_related('course', 'student')

    return render(request, 'courses_app/view_all_feedback.html', {
        'feedback_list': feedback_list,
    })
