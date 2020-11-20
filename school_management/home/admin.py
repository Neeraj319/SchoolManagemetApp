from django.contrib import admin
from .models import student, Teacher, Assigment, grade, submmitted_assigmet, Subject, Announcemnt
# Register your models here.

admin.site.register(student)
admin.site.register(Teacher)
admin.site.register(Assigment)
admin.site.register(grade)
admin.site.register(submmitted_assigmet)
admin.site.register(Subject)
admin.site.register(Announcemnt)
