from django.contrib import admin
from .models import Student, Course, Instructor, Grade, Enrollment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'email', 'date_of_birth')
    search_fields = ('student_id', 'full_name', 'email')
    list_filter = ('date_of_birth',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'credits', 'is_active')
    search_fields = ('course_code', 'course_name')
    list_filter = ('is_active',)

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'department')
    search_fields = ('full_name', 'email', 'department')
    list_filter = ('department',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'grade', 'created_at')
    search_fields = ('student__full_name', 'course__course_name')
    list_filter = ('grade',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'date_enrolled')
    search_fields = ('student__full_name', 'course__course_name')
    list_filter = ('status',)
