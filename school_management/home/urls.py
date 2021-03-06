from django.urls import path
# from .views import student_profile, students_home_page, login_student, login_teacher, teachers_home_page, teachers_profile, home_page, logout_user, show_students_assigemnt
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', home_page, name='home'),
    path('student/<int:pk>', student_profile, name="student_profile"),
    path('student/login', login_student, name='student_login'),
    path('teacher/login', login_teacher, name='login_teacher'),
    path('teacher/<int:pk>', teachers_profile, name='teachers_profile'),
    path('student/home', students_home_page, name='students_home_page'),
    path('teacher/home', teachers_home_page, name='teachers_home_page'),
    path('logout', logout_user, name='logout_user'),
    path('assigments/<int:pk>', show_students_assigemnt, name='show_assigemnt'),
    path('add_assigment/<int:pk>', add_assigment, name="add_assigment"),
    path('announcemnet', aannouncemnet,  name='announcemnet'),
    path('discussion/<int:pk>', discussions, name='discussion'),
    path('discussuion/ans/<int:pk>',
         disscusiion_answers, name='disscussion_answers')
    # path('show_assigments', show_assigment_of_students, name='show_assigments'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
