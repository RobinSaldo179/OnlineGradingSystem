from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from .models import Student, Instructor

def role_required(permission=None):
    """Decorator that checks if user has specific permission"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            # Check if user is instructor
            if Instructor.objects.filter(user=request.user).exists():
                instructor_permissions = [
                    'add_grade',
                    'edit_grade',
                    'view_all_courses',
                    'add_course',
                    'edit_course',
                    'delete_course',
                    'view_all_students'
                ]
                if not permission or permission in instructor_permissions:
                    return view_func(request, *args, **kwargs)

            # Check if user is student
            if Student.objects.filter(user=request.user).exists():
                student_permissions = [
                    'view_own_grades',
                    'view_own_courses'
                ]
                if permission in student_permissions:
                    return view_func(request, *args, **kwargs)

            messages.error(request, "You don't have permission to access this page.")
            return redirect('dashboard')
        return _wrapped_view
    return decorator

def instructor_required(view_func):
    """Decorator that checks if user is an instructor"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if Instructor.objects.filter(user=request.user).exists():
            # Add instructor to request for easy access in templates
            request.instructor = Instructor.objects.get(user=request.user)
            return view_func(request, *args, **kwargs)
        
        messages.error(request, "Only instructors can access this page.")
        return redirect('dashboard')
    return _wrapped_view
