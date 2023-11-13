from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from course.models import Course, Topic
from .models import Student
from django.http import JsonResponse


@login_required
def enrolled_courses(request):
    student = Student.objects.get(user=request.user)

    courses = student.enrolled_courses.all()

    context = {
        'courses': courses,
        'student': student
    }

    return render(request, 'students/enrolled_courses.html', context)


@login_required
def percentage_completion(request, course_id):
    student = Student.objects.get(user=request.user)
    course = Course.objects.get(pk=course_id)
    topics = Topic.objects.filter(course=course)

    completed_topics = [
        topic for topic in topics if topic.is_completed_by(student)]
    completion_percentage = (len(completed_topics) /
                             len(topics)) * 100 if len(topics) > 0 else 0

    context = {
        'course': course,
        'completion_percentage': completion_percentage
    }

    return render(request, 'students/percentage_completion.html', context)


def calculate_completion(request, student_id):
    student_courses = Course.objects.filter(student_id=student_id)

    total_courses = Course.objects.count()
    completed_courses = student_courses.count()

    completion_percentage = (completed_courses / total_courses) * 100

    return JsonResponse({'completion_percentage': completion_percentage})


@login_required
def confirm_completion(request, topic_id):
    student = Student.objects.get(user=request.user)
    topic = get_object_or_404(Topic, pk=topic_id)

    if topic not in student.completed_topics.all():
        student.completed_topics.add(topic)
        student.save()

    # You can return a JsonResponse or redirect to a different page as needed
    return JsonResponse({'message': 'Completion confirmed'})
