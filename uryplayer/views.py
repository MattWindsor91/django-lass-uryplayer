"""Views for the URY Player system."""

from django.shortcuts import render, redirect
from django.http import Http404
from uryplayer.models import Podcast, PodcastChannel


def home_podcasts(request, amount=5, block_id=None):
    """Snap-in view for the URY Player box on the front page."""
    return render(
        request,
        'uryplayer/home_podcasts.html',
        {
            'podcasts':
            Podcast.objects.all().order_by('-date_submitted')[:amount]
        })


def podcast_channel_latest(request, channel):
    """Redirects to the latest podcast in a given channel.

    The channel can be specified by name, ID or object.

    """

    match = PodcastChannel.get(channel).latest()
    if not match:
        raise Http404
    return redirect(match)
