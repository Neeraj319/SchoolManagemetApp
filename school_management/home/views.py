from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView
from .models import student, Teacher, Assigment, submmitted_assigmet, Subject, Principal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.
# helloboi123@


def home_page(request):

    if request.user.is_authenticated:
        try:
            if request.user.student:
                return redirect('student/home')

        except:
            return redirect('teachers_home_page')
    return render(request, 'main_home.html')


@login_required(login_url='student/login')
def student_profile(request, pk):
    user_get = get_object_or_404(student, pk=pk)
    show_assigment = Assigment.objects.all()
    context = {
        'student': user_get

    }

    return render(request, 'students_profile.html', context)


@login_required(login_url='student/login')
def students_home_page(request):
    students = student.objects.get(user_name=request.user)
    context = {
        'students': students
    }
    return render(request, 'student_home.html', context)


def login_student(request):
    if request.method == 'POST':
        user_name = request.POST.get("user_name")
        password = request.POST.get('password')
        user = authenticate(username=user_name, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        print(user_name, password)

    return render(request, 'login.html')


@login_required(login_url='teacher/login')
def teachers_home_page(request):
    try:
        if request.user.student:
            return redirect('students_home_page')
    except:
        teacher = Teacher.objects.get(user_name=request.user)
        context = {
            'teacher': teacher,
        }

    return render(request, 'teachers_home.html', context)


def login_teacher(request):
    if request.method == 'POST':
        user_name = request.POST.get("user_name")
        password = request.POST.get('password')
        user = authenticate(username=user_name, password=password)
        if user is not None:
            login(request, user)
            return redirect('teachers_home_page')
        print(user_name, password)

    return render(request, 'teachers_login.html')


@login_required(login_url='login')
def teachers_profile(request, pk):
    user_get = Teacher.objects.get(pk=pk)
    context = {
        'teacher': user_get
    }

    return render(request, 'teachers_profile.html', context)


def logout_user(request):
    logout(request)
    return redirect('/')


# **kwargs(apple=123) *args(a, "apple")
def show_students_assigemnt(request, pk, *args):
    assigments = submmitted_assigmet.objects.all()
    if request.method == 'POST':
        imgage = request.FILES.get('file')
        assigment_s = Assigment.objects.get(id=pk)
        img, _ = submmitted_assigmet.objects.get_or_create(
            student=request.user.student, assigment=assigment_s)
        img.submitted = imgage
        img.save()

    students_asigment = Assigment.objects.filter(
        garde=request.user.student.grade)

    context = {
        'assigments': students_asigment,
        'submmit': assigments
    }

    return render(request, 'students_assigemnts.html', context)


def add_assigment(request, pk):
    try:
        give_assigment = Subject.objects.get(pk=pk)
        print(give_assigment)
    except:
        return redirect('home')
    if request.method == 'POST':
        file = request.FILES.get('file')

        name = request.POST.get('assigment')
        files, _ = Assigment.objects.get_or_create(
            topic=name, garde=give_assigment.grade, teacher=request.user.teacher, subject=give_assigment)
        files.name = file
        files.save()
    context = {
        'assigment': give_assigment
    }
    return render(request, 'teacher_submmit.html', context)
