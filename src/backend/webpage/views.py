from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .serializers import *
from rest_framework import generics
import subprocess

# Route for opening the flask app and redirecting to the new tab
def open_flask(request, mcode, lecture_id, date, time, attendance, day):
    subprocess.Popen(["python3", "flask-app/app.py", mcode, lecture_id, date, time, attendance, day])
    return redirect('http://127.0.0.1:5000')

class APIUserViewSet(viewsets.ModelViewSet):
    queryset = APIUser.objects.all() #Route for interacting with the user details
    serializer_class = APIUserSerializer

class ModuleViewSet(viewsets.ModelViewSet):
	queryset = Module.objects.all() #Route for interacting with the module details
	serializer_class = ModuleSerializer

class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all() #Route for interacting with the lecture details
    serializer_class = LectureSerializer

class LectureRecordViewSet(viewsets.ModelViewSet):
    queryset = LectureRecord.objects.all() #Route for interacting with the lecture record details
    serializer_class = LectureRecordSerializer

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] #No login is needed to access this route
    queryset = APIUser.objects.all()

class AddLectureAPIView(generics.CreateAPIView):
    serializer_class = AddLectureSerializer
    permission_classes = [IsAuthenticated] #User needs to be logged in to access
    queryset = Lecture.objects.all()

class AddModuleAPIView(generics.CreateAPIView):
    serializer_class = AddModuleSerializer
    permission_classes = [IsAuthenticated] #User needs to be logged in to access
    queryset = Module.objects.all()

class AddLectureRecordAPIView(generics.CreateAPIView):
    serializer_class = AddLectureRecordSerializer
    permission_classes = [AllowAny] #No login is needed to access this route
    queryset = LectureRecord.objects.all()

class RemoveModuleAPIView(generics.CreateAPIView):
    serializer_class = RemoveModuleSerializer
    permission_classes = [IsAuthenticated] #User needs to be logged in to access
    queryset = Module.objects.all()

class RemoveLectureAPIView(generics.CreateAPIView):
    serializer_class = RemoveLectureSerializer
    permission_classes = [IsAuthenticated] #User needs to be logged in to access
    queryset = Lecture.objects.all()