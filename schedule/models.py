from django.db import models


# Create your models here.
class Teacher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    priority = models.IntegerField()

    def __str__(self):
        return self.name


class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    hours_per_week = models.IntegerField()

    def __str__(self):
        return f"{self.teacher.name} - {self.subject.name} ({self.hours_per_week} hours/week)"


class Schedule(models.Model):
    day_of_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher_subject = models.ForeignKey(TeacherSubject, on_delete=models.CASCADE)
