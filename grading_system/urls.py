from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from grades import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_choice, name='register_choice'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/instructor/', views.register_instructor, name='register_instructor'),
    path('students/', views.student_list, name='student_list'),
    path('student/<int:student_id>/grades/', views.student_grades, name='student_grades'),
    path('student/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('student/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/', views.view_course, name='view_course'),
    path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('grade/add/<int:student_id>/<int:course_id>/', views.add_grade, name='add_grade'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
