from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from grades.models import Student, Course, Instructor, Enrollment, Grade
from datetime import date

class Command(BaseCommand):
    help = 'Creates test data for the grading system and test instructor account'

    def handle(self, *args, **kwargs):
        # Create test users
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        teacher_user = User.objects.create_user('teacher', 'teacher@example.com', 'teacher123')
        student_user = User.objects.create_user('student', 'student@example.com', 'student123')

        # Create instructor
        instructor = Instructor.objects.create(
            user=teacher_user,
            full_name='John Smith',
            email='teacher@example.com',
            department='Computer Science'
        )

        # Create test instructor
        instructor_user = User.objects.create_user(
            username='teacher1',
            password='teacher123',
            email='teacher1@example.com'
        )

        instructor = Instructor.objects.create(
            user=instructor_user,
            full_name='Teacher One',
            email='teacher1@example.com',
            department='Computer Science',
            phone='123-456-7890'
        )

        # Create students
        student1 = Student.objects.create(
            user=student_user,
            student_id='2024001',
            full_name='Jane Doe',
            email='student@example.com',
            date_of_birth=date(2000, 1, 1)
        )

        # Create courses
        course1 = Course.objects.create(
            course_code='CS101',
            course_name='Introduction to Programming',
            description='Basic programming concepts'
        )

        # Create enrollment
        enrollment = Enrollment.objects.create(
            student=student1,
            course=course1
        )

        # Create grade
        grade = Grade.objects.create(
            student=student1,
            course=course1,
            grade='A'
        )

        self.stdout.write(self.style.SUCCESS('Successfully created test data and instructor account:\nUsername: teacher1\nPassword: teacher123'))
