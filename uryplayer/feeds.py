from django.contrib.syndication.views import Feed
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

    def item_url(self, item):
        return item.get_absolute_url

    def item_enclosure_url(self, item):
        return website.root + item.file.url

    def item_enclosure_length(self, item):
        return item.file.size

    item_enclosure_mime_type = "audio/mpeg"

    def item_pubDate(self, item):
        return item.date_submitted
