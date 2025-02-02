"""
Grading System Views
Author: Robin L. Saldo
Description: View functions for handling grading system operations
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, Course, Grade, Instructor, Enrollment
from .forms import StudentRegistrationForm, InstructorRegistrationForm
from django.urls import reverse
from .decorators import role_required, instructor_required

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Changed this line
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
@instructor_required
def student_list(request):
    """View for listing all students (instructor only)"""
    students = Student.objects.all()
    return render(request, 'students.html', {'students': students})

@login_required
@instructor_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.user.delete()  # This will also delete the student due to CASCADE
    messages.success(request, 'Student deleted successfully')
    return redirect('student_list')

@login_required
@instructor_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.full_name = request.POST.get('full_name')
        student.email = request.POST.get('email')
        student.save()
        messages.success(request, 'Student updated successfully')
        return redirect('student_list')
    return render(request, 'edit_student.html', {'student': student})

@login_required
def dashboard_view(request):
    try:
        # Check if user is student
        student = Student.objects.filter(user=request.user).first()
        if student:
            context = {
                'total_courses': Course.objects.filter(enrollment__student=student).count(),
                'recent_grades': Grade.objects.filter(student=student).select_related('course').order_by('-created_at')[:5],
                'recent_enrollments': Enrollment.objects.filter(student=student).order_by('-date_enrolled')[:5],
                'is_student': True
            }
        # Check if user is instructor
        else:
            context = {
                'total_students': Student.objects.count(),
                'total_courses': Course.objects.count(),
                'total_instructors': Instructor.objects.count(),
                'total_enrollments': Enrollment.objects.filter(status='ENROLLED').count(),
                'recent_grades': Grade.objects.select_related('student', 'course').order_by('-created_at')[:5],
                'recent_enrollments': Enrollment.objects.select_related('student', 'course').order_by('-date_enrolled')[:5],
                'is_instructor': True
            }
        return render(request, 'dashboard.html', context)
    except Exception as e:
        messages.error(request, f"Error loading dashboard: {str(e)}")
        return render(request, 'dashboard.html', {})

@login_required
@instructor_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})

@login_required
def student_grades(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    # Check if user is viewing their own grades or is an instructor
    if request.user == student.user or Instructor.objects.filter(user=request.user).exists():
        grades = Grade.objects.filter(student=student).select_related('course')
        return render(request, 'student_grades.html', {
            'student': student,
            'grades': grades,
            'gpa': student.get_gpa()
        })
    messages.error(request, "You can only view your own grades.")
    return redirect('dashboard')

@login_required
@role_required('add_grade')
def add_grade(request, student_id, course_id):
    if request.method == 'POST':
        grade = request.POST.get('grade')
        student = get_object_or_404(Student, id=student_id)
        course = get_object_or_404(Course, id=course_id)
        
        Grade.objects.create(
            student=student,
            course=course,
            grade=grade
        )
        messages.success(request, 'Grade added successfully')
        return redirect('student_grades', student_id=student_id)
    
    return redirect('student_list')

@login_required
@instructor_required
def add_course(request):
    if request.method == 'POST':
        course_code = request.POST.get('course_code')
        course_name = request.POST.get('course_name')
        description = request.POST.get('description')
        credits = request.POST.get('credits')
        
        Course.objects.create(
            course_code=course_code,
            course_name=course_name,
            description=description,
            credits=credits
        )
        messages.success(request, 'Course added successfully')
        return redirect('course_list')
    
    return render(request, 'add_course.html')

@login_required
def view_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrolled_students = course.get_enrolled_students()
    return render(request, 'view_course.html', {
        'course': course,
        'enrolled_students': enrolled_students
    })

@login_required
@instructor_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        course.course_name = request.POST.get('course_name')
        course.description = request.POST.get('description')
        course.credits = request.POST.get('credits')
        course.is_active = request.POST.get('is_active') == 'on'
        course.save()
        
        messages.success(request, 'Course updated successfully')
        return redirect('course_list')
    
    return render(request, 'edit_course.html', {'course': course})

@login_required
@instructor_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, 'Course deleted successfully')
    return redirect('course_list')

def register_choice(request):
    return render(request, 'registration/register_choice.html')

def register_student(request):
    """View for student registration"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(
                user=user,
                student_id=form.cleaned_data['student_id'],
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                date_of_birth=form.cleaned_data['date_of_birth']
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/register_student.html', {'form': form})

def register_instructor(request):
    if request.method == 'POST':
        form = InstructorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Instructor.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                department=form.cleaned_data['department']
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = InstructorRegistrationForm()
    return render(request, 'registration/register_instructor.html', {'form': form})