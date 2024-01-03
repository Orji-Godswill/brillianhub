from django.shortcuts import render, redirect
from .forms import AppointmentForm
from django.contrib import messages

# Create your views here.


def appointment_view(request):
    appointment_form = AppointmentForm(request.POST)

    if request.method == 'POST':
        if appointment_form.is_valid():
            appointment_form.save()
            messages.success(
                request, "We have received your message. we would rech you on email. Thank you.")
            return redirect("{% url 'home' %}")
    else:
        appointment_form = AppointmentForm()

    context = {
        'appointment_form': appointment_form
    }
    return render(request, 'consult/book_appointment.html', context)
