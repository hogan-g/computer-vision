from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
admin.site.register(APIUser, UserAdmin)
admin.site.register(Module)
admin.site.register(Lecture)
admin.site.register(LectureRecord)
