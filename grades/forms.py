from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Instructor

class StudentRegistrationForm(UserCreationForm):
    student_id = forms.CharField(max_length=10)
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('username', 'student_id', 'full_name', 'email', 'date_of_birth', 'password1', 'password2')

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if Student.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("This Student ID is already taken. Please use a different one.")
        return student_id

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please use a different email.")
        return email

class InstructorRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15, required=False)
    department = forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'phone', 'department', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please use a different email.")
        return email
