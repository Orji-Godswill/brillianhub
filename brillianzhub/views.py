from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView
from accounts.forms import ContactForm
from accounts.models import Contact
from django.core.mail import send_mail, BadHeaderError


def index_view(request):
    # objects_designs = Design.objects.all().published().filter(featured=True).reverse()[:20]
    # objects_plots  = Plot.objects.all().published().filter(featured=True).reverse()[:6]

    context = {
        # 'objects_designs': objects_designs,
        # 'objects_plots': objects_plots
    }
    return render(request, 'index.html', context)


def contact_view(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            sender = form.cleaned_data['sender']
            phone = form.cleaned_data['phone']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = ['brillianzhub@gmail.com']
            if cc_myself:
                recipients.append(sender)
            try:
                send_mail(name, phone, message,  recipients)
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
