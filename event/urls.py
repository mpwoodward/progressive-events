from django.conf.urls import url

import views


urlpatterns = [
    url(r'^(\d+)/$', views.detail, name='detail'),
    url(r'^add/$', views.event_form, name='add'),
    url(r'^edit/(\d+)/$', views.event_form, name='edit'),
]
