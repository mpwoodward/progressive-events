from django.shortcuts import get_object_or_404, render

from .forms import EventForm, OrganizationForm, VenueForm
from .models import Event


def event_form(request, event_id=None):
    if event_id:
        event = get_object_or_404(Event, pk=event_id)
    else:
        event = None

    event_form = EventForm(request.POST or None, instance=event)
    organization_form = OrganizationForm()
    venue_form = VenueForm()

    return render(
        request,
        'event/event_form.html',
        {'event_form': event_form, 'organization_form': organization_form, 'venue_form': venue_form}
    )


def detail(request, event_id):
    pass
