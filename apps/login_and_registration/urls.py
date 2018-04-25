from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^login_form$', views.login_form),
    url(r'^register_form$', views.register_form),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
]