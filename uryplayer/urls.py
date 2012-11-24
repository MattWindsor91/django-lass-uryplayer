from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from uryplayer.views import podcast_channel_latest
from uryplayer.models import Podcast

urlpatterns = patterns(
    'uryplayer.views',
    url(r'^podcasts/$',
        ListView.as_view(model=Podcast),
        name='podcast_index'),
    url(r'^podcasts/channels/(?P<channel>\w+)/latest',
        podcast_channel_latest,
        name='podcast_channel_latest'),
    url(r'^podcasts/(?P<pk>\d+)/$',
        DetailView.as_view(model=Podcast),
        name='podcast_detail'),
)
