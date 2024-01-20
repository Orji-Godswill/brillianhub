from .models import Student, Course, Module
from django.views.generic import ListView
from typing import Any
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from course.models import Course, Module, Topic, CompletedTopic
from .models import Student
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('course:course_detail', args=[self.course.id, self.course.slug])


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/enrolled_courses.html'

    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student = get_object_or_404(Student, user=self.request.user)

        my_courses = Course.objects.all().filter(
            students__in=[self.request.user])

        result_dict = {}

        for course in my_courses:
            total_topics = Topic.objects.filter(course_id=course.id).count()
            completed_topics = student.completed_topics.filter(course=course)

            num_completed_topics = completed_topics.count()

            percentage_completion = (
                num_completed_topics / total_topics) * 100 if total_topics > 0 else 0

            percentage_completion = round(percentage_completion, 2)

            if student.user not in result_dict:
                result_dict[student.user] = {course.title: {
                    'total_topics': total_topics,
                    'completed_topics': num_completed_topics,
                    'percentage_completion': percentage_completion
                }}
            else:
                result_dict[student.user][course.title] = {
                    'total_topics': total_topics,
                    'completed_topics': num_completed_topics,
                    'percentage_completion': percentage_completion
                }

        context['result'] = result_dict
        return context


# @login_required
# def confirm_completion(request, topic_id):
#     student = Student.objects.get(user=request.user)
#     topic = get_object_or_404(Topic, pk=topic_id)

#     if topic not in student.completed_topics.all():
#         student.completed_topics.add(topic)
#         student.save()

#     # You can return a JsonResponse or redirect to a different page as needed
#     return JsonResponse({'message': 'Completion confirmed'})


def percentage_completion(request, course_id):
    student = Student.objects.get(user=request.user)
    course = Course.objects.get(pk=course_id)
    topics = Topic.objects.filter(course=course)
    completed_topics = CompletedTopic.objects.filter(
        user=student, topic__course=course, completed=True)

    completed_topics = [
        topic for topic in topics if topic.is_completed_by(student)]
    completion_percentage = (len(completed_topics) /
                             len(topics)) * 100 if len(topics) > 0 else 0

    print(completion_percentage)
    context = {
        'course': course,
        'completion_percentage': completion_percentage
    }

    return render(request, 'students/percentage_completion.html', context)


def calculate_completion(request, student_id, pk):
    student_courses = Course.objects.filter(student_id=student_id)

    course = get_object_or_404(Course, pk=pk)
    completed_topics = CompletedTopic.objects.filter(
        user=request.user, topic__course=course, completed=True)

    total_topics = Topic.objects.count()
    completed_topics = student_courses.count()

    completion_percentage = (completed_topics / total_topics) * 100

    return JsonResponse({'completion_percentage': completion_percentage})
