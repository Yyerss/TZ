from django.contrib import admin
from .models import Teacher, Subject, TeacherSubject, Schedule


class TeacherSubjectInline(admin.TabularInline):
    model = TeacherSubject
    extra = 1


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)
    inlines = [TeacherSubjectInline]


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'priority')
    search_fields = ('name',)
    ordering = ('priority', 'name')
    inlines = [TeacherSubjectInline]


@admin.register(TeacherSubject)
class TeacherSubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'subject', 'hours_per_week')
    list_filter = ('teacher', 'subject')
    search_fields = ('teacher__name', 'subject__name')
    ordering = ('teacher', 'subject')
    inlines = [ScheduleInline]


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'day_of_week', 'start_time', 'end_time', 'teacher_subject')
    list_filter = ('day_of_week', 'teacher_subject__teacher', 'teacher_subject__subject')
    search_fields = ('teacher_subject__teacher__name', 'teacher_subject__subject__name')
    ordering = ('day_of_week', 'start_time')
