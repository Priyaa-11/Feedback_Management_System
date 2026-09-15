from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Teacher, Feedback
from accounts.models import Student
from django.contrib.auth.models import User


# Helper function to check if user is admin
def is_admin(user):
    return user.is_staff

# Helper function to check if user is a student (not admin)
def is_student(user):
    return not user.is_staff

@login_required
@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_feedback = Feedback.objects.count()
    recent_feedback = Feedback.objects.order_by('-created_at')[:5] # Get last 5
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_feedback': total_feedback,
        'recent_feedback': recent_feedback,
    }
    return render(request, 'admin_panel/dashboard.html', context)

# --- STUDENT MANAGEMENT ---
@login_required
@user_passes_test(is_admin, login_url='login')
def manage_students(request):
    students = Student.objects.all().order_by('roll_number')
    return render(request, 'admin_panel/manage_students.html', {'students': students})

@login_required
@user_passes_test(is_admin, login_url='login')
def add_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        roll_number = request.POST.get('roll_number')
        name = request.POST.get('name')
        department = request.POST.get('department')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Create Django User
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('manage_students')
            
        user = User.objects.create_user(username=username, password=password)
        
        # Create Student Profile
        Student.objects.create(
            user=user, roll_number=roll_number, name=name, 
            department=department, email=email, phone=phone, address=address
        )
        messages.success(request, "Student added successfully.")
        return redirect('manage_students')
    return render(request, 'admin_panel/add_student.html')

@login_required
@user_passes_test(is_admin, login_url='login')
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.user.delete() # This deletes the Django User and cascades to Student
    messages.success(request, "Student deleted successfully.")
    return redirect('manage_students')

# --- TEACHER MANAGEMENT ---
@login_required
@user_passes_test(is_admin, login_url='login')
def manage_teachers(request):
    teachers = Teacher.objects.all().order_by('name')
    return render(request, 'admin_panel/manage_teachers.html', {'teachers': teachers})

@login_required
@user_passes_test(is_admin, login_url='login')
def add_teacher(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        department = request.POST.get('department')
        email = request.POST.get('email')
        Teacher.objects.create(name=name, department=department, email=email)
        messages.success(request, "Teacher added successfully.")
        return redirect('manage_teachers')
    return render(request, 'admin_panel/add_teacher.html')

@login_required
@user_passes_test(is_admin, login_url='login')
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.delete()
    messages.success(request, "Teacher deleted successfully.")
    return redirect('manage_teachers')

# --- FEEDBACK MANAGEMENT ---
@login_required
@user_passes_test(is_admin, login_url='login')
def view_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/view_feedback.html', {'feedbacks': feedbacks})

# --- STUDENT VIEWS ---
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Teacher, Feedback
from accounts.models import Student
from django.contrib import messages
from django.utils import timezone

@login_required
@user_passes_test(is_student, login_url='login')
def student_dashboard(request):
    # Get the student profile of the logged-in user
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found. Please contact admin.")
        return redirect('login')

    # Get feedback submitted by this student
    my_feedback = Feedback.objects.filter(student=student).order_by('-created_at')

    context = {
        'student': student,
        'my_feedback': my_feedback,
    }
    return render(request, 'student/dashboard.html', context)

@login_required
@user_passes_test(is_student, login_url='login')
def submit_feedback(request):
    # Get the student profile
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('login')

    # Security: Prevent admins from submitting feedback as a student
    if request.user.is_staff:
        messages.error(request, "Admins cannot submit feedback.")
        return redirect('admin_dashboard')

    # Only show teachers that the student has NOT given feedback to yet
    already_given_teacher_ids = Feedback.objects.filter(student=student).values_list('teacher_id', flat=True)
    teachers = Teacher.objects.exclude(id__in=already_given_teacher_ids)

    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        rating = request.POST.get('rating')
        description = request.POST.get('description')

        # Server-side validation
        if not teacher_id or not rating or not description.strip():
            messages.error(request, "Please fill in all fields.")
        elif not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            messages.error(request, "Rating must be a number between 1 and 5.")
        else:
            try:
                teacher = Teacher.objects.get(id=teacher_id)
                
                # Double-check duplicate (in case of race conditions or manual URL manipulation)
                if Feedback.objects.filter(student=student, teacher=teacher).exists():
                    messages.error(request, f"You have already submitted feedback for {teacher.name}.")
                else:
                    Feedback.objects.create(
                        student=student,
                        teacher=teacher,
                        rating=int(rating),
                        description=description.strip()
                    )
                    messages.success(request, "Feedback submitted successfully!")
                    return redirect('thank_you')
            except Teacher.DoesNotExist:
                messages.error(request, "Selected teacher does not exist.")

    context = {
        'student': student,
        'teachers': teachers,
    }
    return render(request, 'student/feedback_form.html', context)

@login_required
@user_passes_test(is_student, login_url='login')
def thank_you(request):
    return render(request, 'student/thank_you.html')