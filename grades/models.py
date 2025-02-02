from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    def get_current_courses(self):
        return Course.objects.filter(enrollment__student=self)

    def get_gpa(self):
        grades = self.grade_set.all()
        if not grades:
            return 0.0
        return sum(float(grade.numeric_grade()) for grade in grades) / len(grades)

class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=100)
    description = models.TextField()
    credits = models.IntegerField(default=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course_name

    def get_enrolled_students(self):
        return Student.objects.filter(enrollment__course=self)

    def get_average_grade(self):
        grades = self.grade_set.all()
        if not grades:
            return 0.0
        return sum(float(grade.numeric_grade()) for grade in grades) / len(grades)

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    def get_courses(self):
        return Course.objects.filter(instructor=self)

    def get_total_students(self):
        return Student.objects.filter(enrollment__course__instructor=self).distinct().count()

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('ENROLLED', 'Enrolled'),
        ('DROPPED', 'Dropped'),
        ('COMPLETED', 'Completed')
    ], default='ENROLLED')

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"

    def clean(self):
        existing = Enrollment.objects.filter(
            student=self.student,
            course=self.course,
            status='ENROLLED'
        ).exists()
        if existing and self.status == 'ENROLLED':
            raise ValidationError("Student is already enrolled in this course.")

class Grade(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+'),
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('D+', 'D+'),
        ('D', 'D'),
        ('F', 'F'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student} - {self.course}: {self.grade}"

    def numeric_grade(self):
        grade_values = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'F': 0.0,
        }
        return grade_values.get(self.grade, 0.0)

    def clean(self):
        if self.student not in self.course.get_enrolled_students():
            raise ValidationError("Student must be enrolled in the course to receive a grade.")
