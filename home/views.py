from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView
from .models import student, Teacher, Assigment, submmitted_assigmet, Subject, grade, Discussion, Discussion_Answer
from .models import Announcement
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import datetime
from django.contrib import messages

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
    if request.user.student.grade == user_get.grade:
        sub = Subject.objects.filter(grade=request.user.student.grade)
        if request.method == 'POST':
            topic = request.POST.get('topic')
            subject_d = request.POST.get('subject')
            content = request.POST.get('content')
            subs = Subject.objects.get(pk=subject_d)
            print(subs)
            diss = Discussion(topic=topic, content=content,
                              grade=request.user.student.grade, student=request.user.student, subject=subs)
            diss.save()
            print('created')
    else:
        return redirect('students_home_page')
    context = {
        'student': user_get,
        'subject': sub

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
    # students can view their assigments from this view
    students_asigment = Assigment.objects.filter(
        garde=request.user.student.grade).order_by('-due_date')
    assigments = submmitted_assigmet.objects.all()
    if request.method == 'POST':
        # i used imagge cause i thought it was easy
        imgage = request.FILES.get('file')
        assigment_s = Assigment.objects.get(id=pk)
        img, _ = submmitted_assigmet.objects.get_or_create(
            student=request.user.student, assigment=assigment_s, subject=assigment_s.subject)
        img.submitted = imgage
        img.save()
        message = messages.success(request, 'assigment has been submitted')
    time = datetime.now()
    print(time)

    context = {
        'assigments': students_asigment,
        'submmit': assigments,
        'time': time
    }

    return render(request, 'students_assigemnts.html', context)


@login_required(login_url='login')
def add_assigment(request, pk):
    try:
        give_assigment = Subject.objects.get(pk=pk)
        Show_assigment = submmitted_assigmet.objects.filter(
            subject=give_assigment)

    except:
        return redirect('home')
    print(give_assigment, Show_assigment)
    if request.method == 'POST':
        file = request.FILES.get('file')

        name = request.POST.get('assigment')
        due_date = request.POST.get('date_s')
        files, _ = Assigment.objects.get_or_create(
            topic=name, garde=give_assigment.grade, teacher=request.user.teacher, subject=give_assigment, due_date=due_date)
        files.name = file
        files.save()
        message = messages.success(request, 'assigment created')
    print(Show_assigment)
    context = {
        'assigment': give_assigment,
        'student_ass': Show_assigment,
    }
    return render(request, 'teacher_submmit.html', context)


@login_required(login_url='login')
def aannouncemnet(request):
    try:
        if request.user.student:
            grade = request.user.student.grade
            announcement_list = Announcement.objects.filter(
                Q(announcement_type="Public") | Q(class_name=grade)).order_by('-date_announced')

    except:
        grade = request.user.teacher.grade
        announcement_list = Announcement.objects.all()

    context = {
        'announcement': announcement_list
    }
    return render(request, 'announcemnt.html', context)


@login_required(login_url='login')
def discussions(request, pk):
    diss = Discussion.objects.filter(grade__pk=pk)
    print(pk)
    if request.user.student.grade.pk != pk:
        return redirect('students_home_page')
    else:
        pass
    context = {
        'discusiion': diss,
    }
    return render(request, 'discussion.html', context)


@login_required(login_url='login')
def disscusiion_answers(request, pk):
    diss = Discussion.objects.get(pk=pk)
    if request.user.student.grade == diss.grade:
        if request.method == 'POST':
            answer = request.POST.get('answer')
            if answer == '':
                return redirect('discussion')
            question = request.POST.get('question_id')
            question_obj = Discussion.objects.get(pk=pk)
            diss_ans = Discussion_Answer(
                discussion=question_obj, answer=answer, student=request.user.student)
            diss_ans.save()
        diss_ans = Discussion_Answer.objects.filter(discussion=diss)
    else:
        return redirect('students_home_page')
    context = {
        'discussion': diss,
        'discussion_answer': diss_ans
    }
    return render(request, 'disscusiion_answer.html', context)
