from django.utils.feedgenerator import Rss201rev2Feed
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site
from django.db.models import permalink
from uryplayer.models import Podcast
import datetime

class iTunesPodcastsFeedGenerator(Rss201rev2Feed):

  def rss_attributes(self):
    return {u"version": self._version, u"xmlns:atom": u"http://www.w3.org/2005/Atom", u'xmlns:itunes': u'http://www.itunes.com/dtds/podcast-1.0.dtd'}

  def add_root_elements(self, handler):
    super(iTunesPodcastsFeedGenerator, self).add_root_elements(handler)
    handler.addQuickElement(u'itunes:subtitle', self.feed['subtitle'])
    handler.addQuickElement(u'itunes:author', self.feed['author_name'])
    handler.addQuickElement(u'itunes:summary', self.feed['description'])
    handler.addQuickElement(u'itunes:explicit', self.feed['iTunes_explicit'])
    handler.startElement(u"itunes:owner", {})
    handler.addQuickElement(u'itunes:name', self.feed['iTunes_name'])
    handler.addQuickElement(u'itunes:email', self.feed['iTunes_email'])
    handler.endElement(u"itunes:owner")
    handler.addQuickElement(u'itunes:image', self.feed['iTunes_image_url'])

  def add_item_elements(self,  handler, item):
    super(iTunesPodcastsFeedGenerator, self).add_item_elements(handler, item)
    handler.addQuickElement(u'itunes:summary',item['summary'])
    handler.addQuickElement(u'itunes:duration',item['duration'])
    handler.addQuickElement(u'itunes:explicit',item['explicit'])
    handler.addQuickElement(u'itunes:image', item['iTunes_image_url'])

class iTunesPodcastPost():
  def __init__(self, podcast):
    self.id = podcast.id
    self.date_submitted = podcast.date_submitted
    self.title = podcast.title
    self.summary = podcast.description
    self.enclosure_url = insecure_url(podcast.file.url)
    self.enclosure_length = podcast.file.size
    self.enclosure_mime_type = u'audio/mpeg'
    self.duration = podcast.duration
    self.explicit = u'no'
    self.url = podcast.get_absolute_url
    self.iTunes_image_url = insecure_url(podcast.thumbnail_image)
  
  def __unicode__(self):
    return "Podcast: %s" % self.title
  
  @permalink
  def get_absolute_url(self):
    return self.url


class iTunesPodcastsFeed(Feed):
  """
  A feed of podcasts for iTunes and other compatible podcatchers.
  """
  title = "URY Player"
  link = "/uryplayer/podcasts/"
  description = "The ((ury player)) allows you to listen to hours of previous URY programming for free in the form of podcasts. Missed the last URY Speech production? You can find it in here. Couldn't listen to URY News's latest celebrity interview? It's on ((ury player)). And all of our coverage of campus events - from YUSU elections to Woodstock to Roses - is listenable on demand."
  author_name = 'University Radio York'
  subtitle = "The latest On Demand content from Your Student Radio Station"
  summary = "The latest on demand content from University Radio York, your student radio station."
  iTunes_name = u'University Radio York'
  iTunes_email = u'computing@ury.org.uk'
  iTunes_image_url = u'http://ury.org.uk/static/img/logo.png'
  iTunes_explicit = u'no'
  feed_type = iTunesPodcastsFeedGenerator
  feed_copyright = "Copyright 1967-%s University Radio York" % datetime.date.today().year
  
  def items(self):
    """
    Returns a list of items to publish in this feed.
    """
    posts = Podcast.objects.all().order_by('-date_submitted')[:10]
    posts = [iTunesPodcastPost(item) for item in posts]
    return posts

  def feed_extra_kwargs(self, item):
    extra = {}
    extra['iTunes_name'] = self.iTunes_name
    extra['iTunes_email'] = self.iTunes_email
    extra['iTunes_image_url'] = self.iTunes_image_url
    extra['iTunes_explicit'] = self.iTunes_explicit
    return extra

  def item_extra_kwargs(self, item):
    return {'summary':item.summary, 'duration':item.duration, 'explicit':item.explicit, 'iTunes_image_url':item.iTunes_image_url}

  def item_pubdate(self, item):
    return item.date_submitted

  def item_enclosure_url(self, item):
    return item.enclosure_url
    
  def item_enclosure_length(self, item):
    return item.enclosure_length
    
  def item_enclosure_mime_type(self, item):
    return item.enclosure_mime_type

  def item_description(self, item):
    return item.summary



current_site = Site.objects.get_current()

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
        return 'http://' + current_site.domain + item.file.url

    def item_enclosure_length(self, item):
        return item.file.size

    item_enclosure_mime_type = "audio/mpeg"

    def item_pubdate(self, item):
        return item.date_submitted
