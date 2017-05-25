from django.conf.urls import url

import views

urlpatterns = [
    url(r'^create/$', views.create_event, name='create'),
]
