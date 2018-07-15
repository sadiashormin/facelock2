from django.conf.urls import url
from home.views import HomeView
from . import views

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^post/(?P<operation>.+)/(?P<pk>\d+)/$', views.action_post, name='change_post'),
    # url(r'^tag/(?P<operation>.+)/(?P<pk>\d+)/(?P<area>.+)/$', views.action_area, name='change_area'),
    url(r'^tag/(?P<operation>.+)/(?P<pk>\d+)/(?P<area>.+)/$', views.action_tag, name='change_area'),
    url(r'^tag/(?P<operation>.+)/(?P<pk>\d+)/$', views.action_tag, name='change_tag'),

    
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends')
]
