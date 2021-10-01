
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_management.settings")
django.setup()
 
 # setting up

from home.models import grade
from home.models import Subject

grades = grade.objects.all()

subjects = ["science", "math", "english"]


for grade in grades:
    for subject in subjects:
        Subject.objects.create(name=subject, grade=grade)
