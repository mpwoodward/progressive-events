from __future__ import unicode_literals

from datetime import datetime, timedelta
import pytz

from localflavor.us.models import PhoneNumberField, USStateField, USZipCodeField

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.utils.timezone import now

from core.fields import MoneypatchedRecurrenceField
from core.utils import get_point


def round_hours(hours=1):
    return now().replace(minute=0).replace(second=0) + timedelta(hours=hours)


def round_two_hours():
    return round_hours(2)


class Venue(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = USStateField()
    zipcode = USZipCodeField(blank=True)
    slug = models.SlugField(blank=True, null=True, max_length=255)
    phone = PhoneNumberField(blank=True)
    url = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    keywords = models.CharField(blank=True, max_length=255)
    point = models.PointField(blank=True, null=True)
    objects = models.GeoManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            candidate_slug = slugify(self.title)[0:255]
            if self.__class__.objects.filter(slug=candidate_slug).exists():
                candidate_slug_counter = 1
                while True:
                    if not self.__class__.objects.filter(
                            slug="%s-%s" % (candidate_slug, candidate_slug_counter)).exists():
                        break
                    candidate_slug_counter += 1

            self.slug = candidate_slug
        if self.address and not self.point:
            self.point = Point(**get_point(', '.join([self.address, self.city, self.state, self.zipcode])))
        return super(Venue, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class Organization(models.Model):
    ORG_TYPE_CHOICES = (
        ('democratic', 'Democratic Party Organization'),
        ('governing-body', 'Governing Body'),
        ('progressive', 'Progressive Organization'),
        # ('advocacy', 'Advocacy Group'),
        # ('politician', 'Politician'),
        ('candidate', 'Political Candidate'),
    )
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    slug = models.SlugField(blank=True, null=True, max_length=255)
    organization_type = models.CharField(max_length=255, choices=ORG_TYPE_CHOICES, null=True, blank=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            candidate_slug = slugify(self.title)[0:255]
            if self.__class__.objects.filter(slug=candidate_slug).exists():
                candidate_slug_counter = 1
                while True:
                    if not self.__class__.objects.filter(
                            slug="%s-%s" % (candidate_slug, candidate_slug_counter)).exists():
                        break
                    candidate_slug_counter += 1

            self.slug = candidate_slug
        return super(Organization, self).save(*args, **kwargs)


class EventQueryset(models.query.GeoQuerySet):
    def filter_by_date(self, as_occurrences=False, **kwargs):

        midnight_hawaii = datetime.combine(datetime.now(pytz.timezone('US/Hawaii')), datetime.min.time())
        future_date = midnight_hawaii + timedelta(**kwargs)
        queryset = self.all()
        events = filter(lambda e: len(e.recurrences.between(midnight_hawaii, future_date, inc=True)) > 0, queryset)
        if as_occurrences:
            occurrences = []
            for e in events:
                occurrences += e.recurrences.between(midnight_hawaii, future_date, inc=True)
            return occurrences
        else:
            return self.filter(pk__in=map(lambda e: e.pk, events))


class Event(models.Model):
    EVENT_TYPE_CHOICES = (
        ('party-event', 'Party Event'),
        ('governing-body-event', 'Governing Body Event'),
        ('volunteer', 'Volunteering Event'),
        ('advocacy', 'Advocacy'),
        ('rally', 'Rally'),
        ('forum', 'Forum'),
        ('community', 'Community Meetup'),
        (None, 'Uncategorized Event'),
    )
    title = models.CharField(max_length=255)
    venue = models.ForeignKey(Venue, null=True, blank=True)
    url = models.URLField(blank=True)
    slug = models.SlugField(blank=True, null=True, max_length=255)
    description = models.TextField(blank=True)
    start = models.TimeField(default=round_hours)
    end = models.TimeField(default=round_two_hours)
    recurrences = MoneypatchedRecurrenceField(blank=True, null=True)
    event_type = models.CharField(max_length=255, choices=EVENT_TYPE_CHOICES, null=True, blank=True)
    host = models.ForeignKey(Organization, blank=True, null=True)
    objects = EventQueryset.as_manager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("event_detail", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            candidate_slug = slugify(self.title)[0:255]
            if self.__class__.objects.filter(slug=candidate_slug).exists():
                candidate_slug_counter = 1
                while True:
                    if not self.__class__.objects.filter(
                            slug="%s-%s" % (candidate_slug, candidate_slug_counter)).exists():
                        break
                    candidate_slug_counter += 1

            self.slug = candidate_slug
        return super(Event, self).save(*args, **kwargs)

    def dates(self, *args, **kwargs):
        if not kwargs:
            kwargs = {'days': 60}
        midnight_hawaii = datetime.combine(datetime.now(pytz.timezone('US/Hawaii')), datetime.min.time())
        future_date = midnight_hawaii + timedelta(**kwargs)
        return [i for i in self.recurrences.between(after=midnight_hawaii, before=future_date, inc=True)]

# from timezone_field import TimeZoneField
#
# from localflavor.us.models import PhoneNumberField, USStateField, USZipCodeField
#
# from ckeditor.fields import RichTextField
#
# class EventType(models.Model):
#     type = models.CharField(max_length=250, verbose_name='Type')
#     is_active = models.BooleanField(default=True, verbose_name='Active')
#     ordering = models.PositiveSmallIntegerField(verbose_name='Ordering')
#
#     def __str__(self):
#         return self.type
#
#     class Meta:
#         verbose_name = 'Event Type'
#         verbose_name_plural = 'Event Types'
#         ordering = ['ordering', ]
#
#
# class Event(models.Model):
#     EVENT_LENGTH_UNITS = (('minutes', 'minutes'), ('hours', 'hours'), ('days', 'days'), )
#
#     type = models.ForeignKey(EventType, verbose_name='Type')
#     title = models.CharField(max_length=250, verbose_name='Event Title')
#     description = RichTextField(verbose_name='Event Description')
#     receive_rsvp_emails = models.BooleanField(default=True, verbose_name='Receive RSVP Emails')
#     send_email_reminder_to_attendees = models.BooleanField(default=True, verbose_name='Send Email Reminders')
#     # num_hours_ahead_to_send_reminders = models.PositiveSmallIntegerField() -- JUST DO 24 HOURS
#     event_timezone = TimeZoneField(default='America/Los_Angeles', verbose_name='Event Timezone')
#     dt_event = models.DateTimeField(verbose_name='Event Date/Time')
#     event_length = models.PositiveSmallIntegerField(default=1, verbose_name='Event Length')
#     event_length_unit = models.CharField(max_length=20, choices=EVENT_LENGTH_UNITS, default='hours',
#                                          verbose_name='Event Length Unit')
#     all_day_event = models.BooleanField(default=False, verbose_name='All Day Event')
#     location_name = models.CharField(max_length=250, verbose_name='Location Name')
#     max_capacity = models.PositiveSmallIntegerField(default=0,
#                                                     verbose_name='Max Capacity (0 if unlimited)')
#     location_address1 = models.CharField(blank=True, null=True, max_length=250,
#                                          verbose_name='Location Address')
#     location_address2 = models.CharField(blank=True, null=True, max_length=250,
#                                          verbose_name='Location Address (cont.)')
#     location_city = models.CharField(max_length=250, verbose_name='Location City')
#     location_state = USStateField(verbose_name='Location State')
#     location_zip = USZipCodeField(verbose_name='Venue Zip Code')
#     directions = models.TextField(blank=True, null=True, verbose_name='Directions to Event')
#     contact_phone = PhoneNumberField(blank=True, null=True, verbose_name='Contact Phone')
#     display_phone_in_listing = models.BooleanField(default=False,
#                                                    verbose_name='Display Contact Phone in Event Listing')
#
#     def __str__(self):
#         pass
#
#     class Meta:
#         verbose_name = 'Event'
#         verbose_name_plural = 'Events'
#         ordering = ['-dt_event']
