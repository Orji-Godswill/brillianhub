from django.db import models
import random
from course.models import Course, Module


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    text = models.TextField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.course}: {self.module}"

    # def get_next_topic(self):
    #     next_question = Question.objects.filter(module=self.module).order_by('pk').first()
    #     return next_question

    def get_next_question(self):
        try:
            next_question = Question.objects.filter(
                course=self.course,
                module=self.module,
                pk__gt=self.pk
            ).order_by('pk').first()
            return next_question
        except Question.DoesNotExist:
            return None


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    multiple_choice = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.multiple_choice
