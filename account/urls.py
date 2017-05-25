from django.conf.urls import url

import views

urlpatterns = [
    url(r'^create/$', views.create_account, name='create'),
    url(r'^login/$', views.login_form, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
]
