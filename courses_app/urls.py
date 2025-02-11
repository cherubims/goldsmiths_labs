from django.urls import path
from . import views  # Importing views module

urlpatterns = [
    # Teacher-specific URLs
    path('teacher/courses/', views.teacher_courses_view, name='teacher_courses'),
    path('teacher/courses/create/', views.create_course_view, name='create_course'),
    path('teacher/courses/<int:course_id>/upload/', views.upload_material_view, name='upload_material'),
    path('teacher/material/<int:material_id>/delete/', views.delete_material_view, name='delete_material'),
    path('teacher/courses/<int:course_id>/students/', views.view_enrolled_students_view, name='view_enrolled_students'),
    path('teacher/courses/<int:course_id>/progress/', views.teacher_progress_view, name='teacher_progress'),
    path('teacher/courses/<int:course_id>/feedback/', views.view_feedback_view, name='view_feedback'),
    path('teacher/announcements/', views.teacher_announcements, name='teacher_announcements'),  
    path('teacher/announcements/create/', views.create_announcement, name='create_announcement'),
    path('teacher/announcements/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('teacher/announcements/<int:pk>/edit/', views.edit_announcement, name='edit_announcement'),
    path('teacher/feedback/', views.view_all_feedback, name='view_all_feedback'),
    path('teacher/courses/<int:course_id>/toggle_block/<int:student_id>/', views.toggle_block, name='toggle_block'),

    # Student-specific URLs
    path('student/homepage/', views.student_homepage_view, name='student_homepage'),
    path('student/courses/', views.student_courses_view, name='student_courses'),
    path('student/courses/enroll/<int:course_id>/', views.enroll_course_view, name='enroll_course'),
    path('student/courses/<int:course_id>/feedback/', views.leave_feedback_view, name='leave_feedback'),
    path('student/courses/<int:course_id>/progress/', views.student_progress_view, name='student_progress'),
    path('student/courses/<int:course_id>/materials/', views.course_materials_view, name='course_materials'),
    path('student/homepage/status/update/', views.post_status_update_view, name='post_status_update'),

    # Shared URL for course details
    path('course/<int:course_id>/', views.course_detail_view, name='course_detail'),
]
