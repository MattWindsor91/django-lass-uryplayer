from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from uryplayer.models import Podcast

class LatestPodcastsFeed(Feed):
    title = "URY Player"
    link = "/uryplayer/podcasts/"
    description = "The ((ury player)) allows you to listen to hours of previous URY programming for free in the form of podcasts. Missed the last URY Speech production? You can find it in here. Couldn't listen to URY News's latest celebrity interview? It's on ((ury player)). And all of our coverage of campus events - from YUSU elections to Woodstock to Roses - is listenable on demand."

    def items(self):
        return Podcast.objects.all().order_by('-date_submitted')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('podcast', args=[item.pk])
