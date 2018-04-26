from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),  
    #url(r'join/(?P<id>[0-9a-zA-Z% ]+)?/?$', views.join), 
    url(r'join/?$', views.joining),
    # url(r'new/?$', views.new), 
    url(r'create/?$', views.create), 
    url(r'group/(?P<id>[0-9a-zA-Z% ]+)?/?$', views.group), 
    url(r'upgrade_user/(?P<user_id>[0-9]+)/(?P<group_id>[0-9]+)/?$', views.upgrade_user),
    url(r'admin/users/?$', views.users),
    url(r'downgrade_user/(?P<user_id>[0-9]+)/(?P<group_id>[0-9]+)/?$', views.downgrade_user),
    url(r'remove/(?P<user_id>[0-9]+)/(?P<group_id>[0-9]+)/?$', views.remove_user),
]
