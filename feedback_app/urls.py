from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Student Management
    path('manage-students/', views.manage_students, name='manage_students'),
    path('add-student/', views.add_student, name='add_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    
    # Teacher Management
    path('manage-teachers/', views.manage_teachers, name='manage_teachers'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('delete-teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    
    # Feedback Management
    path('view-feedback/', views.view_feedback, name='view_feedback'),

    # Student URLs
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('thank-you/', views.thank_you, name='thank_you'),
]