from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from rest_framework.response import Response
from .serializers import *
import datetime


# Create your views here.
class TeacherList(APIView):
    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubjectList(APIView):
    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherSubjectList(APIView):
    def get(self, request):
        teacher_subjects = TeacherSubject.objects.all()
        serializer = TeacherSubjectSerializer(teacher_subjects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeacherSubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleList(APIView):
    def get(self, request):
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)


class GenerateSchedule(APIView):
    def post(self, request):
        Schedule.objects.all().delete()
        teacher_subjects = TeacherSubject.objects.all().order_by('subject__priority')

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        times = [
            (datetime.time(8, 30), datetime.time(9, 15)),
            (datetime.time(9, 20), datetime.time(10, 5)),
            (datetime.time(10, 20), datetime.time(11, 5)),
            (datetime.time(11, 10), datetime.time(11, 45)),
            (datetime.time(11, 50), datetime.time(12, 35)),
        ]

        schedule = []
        day_index = 0
        time_index = 0
        teacher_schedule = {teacher.id: {day: [] for day in days} for teacher in Teacher.objects.all()}

        for ts in teacher_subjects:
            for _ in range(ts.hours_per_week):
                assigned = False
                while not assigned:
                    if day_index >= len(days):
                        day_index = 0
                    day = days[day_index]

                    if time_index >= len(times):
                        time_index = 0
                        day_index += 1
                        continue

                    start_time, end_time = times[time_index]

                    if not any(s.start_time == start_time for s in teacher_schedule[ts.teacher.id][day]) and not any(
                            s.teacher_subject.subject == ts.subject for s in teacher_schedule[ts.teacher.id][day]):
                        new_schedule = Schedule(
                            day_of_week=day,
                            start_time=start_time,
                            end_time=end_time,
                            teacher_subject=ts
                        )
                        schedule.append(new_schedule)
                        teacher_schedule[ts.teacher.id][day].append(new_schedule)
                        assigned = True
                        time_index += 1
                        if time_index >= len(times):
                            time_index = 0
                            day_index += 1
                    else:
                        time_index += 1
                        if time_index >= len(times):
                            time_index = 0
                            day_index += 1

        Schedule.objects.bulk_create(schedule)
        return Response({'status': 'Schedule generated successfully'}, status=status.HTTP_201_CREATED)