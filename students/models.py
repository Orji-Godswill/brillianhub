from django.db import models
from django.conf import settings
from course.models import Course, Topic
# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    enrolled_courses = models.ManyToManyField(
        Course, related_name='enrolled_students')
    completed_topics = models.ManyToManyField(
        Topic, related_name='completed_by', blank=True)

    def __str__(self):
        return self.user.email
