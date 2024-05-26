from django.urls import path
from .views import TeacherList, SubjectList, TeacherSubjectList, ScheduleList, GenerateSchedule

urlpatterns = [
    path('teachers/', TeacherList.as_view()),
    path('subjects/', SubjectList.as_view()),
    path('teacher-subjects/', TeacherSubjectList.as_view()),
    path('schedules/', ScheduleList.as_view()),
    path('generate-schedule/', GenerateSchedule.as_view())
]