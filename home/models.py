from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class grade(models.Model):
    name = models.IntegerField()

    def __str__(self):
        return ("class: "+str(self.name))


class student(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=20)
    grade = models.ForeignKey(grade, on_delete=models.CASCADE)
    age = models.IntegerField(null=True)
    father_name = models.CharField(max_length=20)
    mothers_name = models.CharField(max_length=20)
    joined_year = models.DateField(auto_now=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return str(self.full_name)


class submmitted_assigmet(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    assigment = models.OneToOneField('Assigment', on_delete=models.DO_NOTHING)
    submitted = models.FileField(
        upload_to='media/student_subbmit_assigment', max_length=100)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student} , | {self.assigment}'


class Subject(models.Model):
    name = models.CharField(max_length=100)
    grade = models.ForeignKey(grade, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " | " + str(self.grade.name)


class Teacher(models.Model):
    '''
    Teacher Model
    '''
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=20)
    age = models.IntegerField(null=True)
    joined_year = models.DateField(auto_now=True, null=True)
    email = models.EmailField()
    grade = models.ManyToManyField(grade)
    subject = models.ManyToManyField(Subject)

    def __str__(self):
        return str(self.full_name)


class Assigment(models.Model):
    name = models.FileField(upload_to='media/techer_give_assigment')
    topic = models.CharField(max_length=20)
    garde = models.ForeignKey(grade, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    due_date = models.DateTimeField()

    def __str__(self):
        return f'{self.name} | {self.garde} | {self.teacher} | {self.subject}'


class Announcement(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date_announced = models.DateTimeField(auto_now=True)
    an_type = (
        ('Custom', 'Custom'),
        ('Public', 'Public'),
    )
    announcement_type = models.CharField(max_length=10, choices=an_type)
    class_name = models.ForeignKey(
        grade, on_delete=models.CASCADE, blank=True, default="1")

    def __str__(self):
        return str(self.title)


class Discussion(models.Model):
    topic = models.CharField(max_length=50)
    content = models.TextField()
    student = models.ForeignKey('student', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey('grade', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.topic} | {self.student.full_name} | {self.subject}'


class Discussion_Answer(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    answer = models.TextField()
    student = models.ForeignKey('student', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.discussion.topic} | {self.student.full_name}'
