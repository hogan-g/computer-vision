from django.db import models
from django.contrib.auth.models import AbstractUser

class APIUser(AbstractUser):
    pass

class Module(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=5, null=False) # The module code
    name = models.CharField(max_length=100, null=False) # The name of the module
    lecturer = models.ForeignKey(APIUser, on_delete=models.CASCADE, default="1") # the ID of the lecturer it's assigned to
    description = models.CharField(max_length=500, default="There is currently no description for this module") # The module description
    student_count = models.IntegerField(default=1) # The module's number of students

class Lecture(models.Model):
    id = models.AutoField(primary_key=True)
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE, default="1") # The ID of the module it's assigned to
    date = models.DateField(default='2020-01-01') # The date the lecture takes place
    day = models.CharField(max_length=10, default="Monday") # The day the lecture takes place
    time = models.TimeField(default='11:00') # The time the lecture starts
    attendance_count = models.IntegerField(default=1) # How many students attended the lecture

class LectureRecord(models.Model):
    id = models.AutoField(primary_key=True)
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE, null = False) # The ID of the lecture it's assigned to
    report_data = models.TextField(null=False) # the text field for holding the JSON data, to be parsed in the frontend