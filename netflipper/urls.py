"""netflipper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from channel import views
from channel.models import Video, Channel



from rest_framework import routers

from django.contrib.auth.views import (
   password_reset,
   password_reset_done,
   password_reset_confirm,
   password_reset_complete
)


router = routers.DefaultRouter()
router.register(r'videos', views.VideoViewSet)





urlpatterns = [
    url(r'^accounts/password/reset/$',
        password_reset,
        {'template_name':
        'registration/password_reset_form.html'},
        name="password_reset"),
    url(r'^accounts/password/reset/done/$',
        password_reset_done,
        {'template_name':
        'registration/password_reset_done.html'},
        name="password_reset_done"),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        {'template_name':
        'registration/password_reset_confirm.html'},
        name="password_reset_confirm"),
    url(r'^accounts/password/done/$',
        password_reset_complete,
        {'template_name':
        'registration/password_reset_complete.html'},
        name="password_reset_complete"),
    url(r'^view_channel/(?P<channel_id>[0-9]+)/$',
        views.view_channel, name='view_channel'),
    url(r'^create_series/$', views.create_series, name='create_series'),
    url(r'^create_movie/$', views.create_movie, name='create_movie'),
    url(r'^create_channel/$', views.create_channel, name='create_channel'),
    url(r'^view_movie/(?P<video_id>[0-9]+)/$',
        views.view_movie, name='view_movie'),
    url(r'^view_season/(?P<series_id>[0-9]+)/(?P<season_id>[0-9]+)/$',
        views.view_season, name='view_season'),
    url(r'^view_series/(?P<series_id>[0-9]+)/$',
        views.view_series, name='view_series'),
    url(r'^user_home', views.user_home, name='user_home'),
    url(r'^browse/', views.browse, name='browse'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api/channels/$', views.ChannelList.as_view()),
    url(r'^api/channels/(?P<pk>[0-9]+)/$', views.ChannelDetail.as_view()),
    url(r'^api/users/$', views.UserList.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.index, name='home'),
]
