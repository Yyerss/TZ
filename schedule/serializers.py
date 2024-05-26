from rest_framework import serializers
from .models import *


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class TeacherSubjectSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = TeacherSubject
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    teacher_subject = TeacherSubjectSerializer()

    class Meta:
        model = Schedule
        fields = '__all__'

