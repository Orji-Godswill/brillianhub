from django.db import models
import random
from course.models import Course, Module


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    text = models.TextField()
    description = models.TextField(null=True, blank=True)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.course}: {self.module}"

    def get_next_question(self):
        next_question = Question.objects.filter(
            module=self.module, order__gt=self.order).order_by('order').first()
        return next_question


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    multiple_choice = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.multiple_choice
