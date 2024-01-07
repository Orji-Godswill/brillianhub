from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView
from accounts.forms import ContactForm
from accounts.models import Contact
from django.core.mail import send_mail, BadHeaderError
from course.models import Course


def index_view(request):
    course = Course.objects.all()

    context = {
        'course': course,
        # 'objects_plots': objects_plots
    }
    return render(request, 'index.html', context)


def contact_view(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email_address = form.cleaned_data['email_address']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipients = ['brillianzhub@gmail.com']

            try:
                send_mail(subject, message, email_address,  recipients)
                form.save()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('home')
        else:
            form = ContactForm(request.POST)
    return render(request, 'base/contact.html', {'form': form, })


def success(request):
    return HttpResponse('Success! Thank you for your message.')


def about_view(request):
    context = {
        'seo_title': 'brillianzhub is a training hub for investors',
    }
    return render(request, 'base/about.html', context)
