from django.db import models
from django.conf import settings
from course.models import Course, Module
# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    enrolled_courses = models.ManyToManyField(
        Course, related_name='enrolled_students')
    completed_modules = models.ManyToManyField(
        Module, related_name='completed_by', blank=True)

    def add_completed_module(self, module):
        self.completed_modules.add(module)

    def __str__(self):
        completed_module_titles = ", ".join(
            [module.title for module in self.completed_modules.all()])
        return "{}. Completed modules: {}".format(self.user.email, completed_module_titles)
