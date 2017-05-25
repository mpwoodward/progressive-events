from django.shortcuts import render


def create_event(request):
    return render(request, 'event/event_form.html')
