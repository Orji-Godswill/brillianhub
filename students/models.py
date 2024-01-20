from django.db import models
from django.conf import settings
from course.models import Course, Module
# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    enrolled_courses = models.ManyToManyField(
        Course, related_name='enrolled_students')
    completed_topics = models.ManyToManyField(
        Module, related_name='completed_by', blank=True)

    def add_completed_topic(self, module):
        self.completed_modules.add(module)

    def __str__(self):
        completed_topic_title = ", ".join(
            [topic.title for topic in self.completed_topics.all()])
        return "{}. Completed topics: {}".format(self.user.email, completed_topic_title)
