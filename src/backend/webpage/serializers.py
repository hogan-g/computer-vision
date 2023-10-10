from rest_framework import serializers
from .models import *

# The serializers for handling our basic models
class APIUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = APIUser
        fields = ['id','email','username']

class ModuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'code', 'name', 'lecturer', 'description', 'student_count']

class LectureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'module_id', 'date', 'day', 'time', 'attendance_count']

class LectureRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LectureRecord
        fields = ['id', 'lecture_id', 'report_data']

# The serializer for registering a new account
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}} # Makes sure password is hidden & secure when typing

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        passsword = validated_data['password'] # Extract the username, email and password from the serializer
        new_user = APIUser.objects.create_user(username=username, 
						email=email, password=passsword) # Create a new APIUser
        new_user.save() # Save the new user
        return new_user

# The serializer for adding a new lecture
class AddLectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'module_id', 'date', 'day', 'time', 'attendance_count']
    
    def create(self, validated_data):
        module_id = validated_data['module_id']
        date = validated_data['date']
        day = validated_data['day']
        time = validated_data['time']
        attendance_count = validated_data['attendance_count'] # Extracts the relevant data from the serializer
        new_lecture_item = Lecture.objects.create(module_id=module_id, date=date, day=day, time=time, attendance_count=attendance_count)
        return new_lecture_item # Creates and returns the new Lecture

# The serializer for adding a new module
class AddModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'code', 'name', 'lecturer', 'description', 'student_count']
    
    def create(self, validated_data):
        code = validated_data['code']
        name = validated_data['name']
        lecturer = validated_data['lecturer']
        description = validated_data['description']
        student_count = validated_data['student_count'] # Extracts the relevant data from the serializer
        new_module_item = Module.objects.create(code=code, name=name, lecturer=lecturer, description=description, student_count=student_count)
        return new_module_item # Creates and returns the new Module

# The serializer for adding a new lecture record from the flask app
class AddLectureRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureRecord
        fields = ['id', 'lecture_id', 'report_data']
    
    def create(self, validated_data):
        lecture_id = validated_data['lecture_id']
        report_data = validated_data['report_data'] # Extracts the relevant data from the serializer
        new_lecture_record_item = LectureRecord.objects.create(lecture_id=lecture_id, report_data=report_data)
        return new_lecture_record_item # Creates and returns the new Lecture Record

# The serializer for removing a module
class RemoveModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['code']

    def create(self, validated_data):
        code = validated_data['code'] # Extracts the relevant data from the serializer
        module = Module.objects.filter(code=code).first() # Finds the specified module
        if module: # If the module exists
            module.delete() # Delete the module
        return Module

# The serializer for removing a lecture
class RemoveLectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['module_id', 'date', 'time']

    def create(self, validated_data):
        module_id = validated_data['module_id']
        date = validated_data['date']
        time = validated_data['time'] # Extracts the relevant data from the serializer
        lecture = Lecture.objects.filter(module_id=module_id, date=date, time=time).first() # Finds the specified lecture
        if lecture: # If the lecture exists
            lecture.delete() # Delete the lecture
        return Lecture

