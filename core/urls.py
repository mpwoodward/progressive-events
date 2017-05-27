from django.conf.urls import include, url

import api
import views


urlpatterns = [
    url(r'^$', views.MapView.as_view(), name='index'),
    url(r'^why$', views.WhyView.as_view(), name='why'),
    url(r'^add$', views.AddView.as_view(), name='add'),

    # experimental embed view
    url(r'^embed$', views.EmbedView.as_view(), name='embed'),
    url(r'^embed-demo$', views.EmbedDemoView.as_view(), name='embed-demo'),

    url(r'^api/1/events', api.EventList.as_view()),
    url(r'^api/1/orgs', api.OrganizationList.as_view()),
    url(r'^api/1/venues', api.VenueList.as_view()),

    url(r'^events/(?P<slug>[\w\-]+)$', views.EventDetailView.as_view(), name='event_detail'),
]
