# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from metadata.models import Metadata, ImageMetadata
from urysite import settings
from urysite import model_extensions as exts
from people.models import Person
from metadata.mixins import MetadataSubjectMixin
from metadata.mixins import SubmittableMixin
from people.mixins import ApprovableMixin
from people.mixins import CreatableMixin
from people.mixins import CreditableMixin


class Podcast(MetadataSubjectMixin,
              SubmittableMixin,
              ApprovableMixin,
              CreatableMixin,
              CreditableMixin):
    """A podcast in the URY player."""

    class Meta:
        db_table = 'podcast'  # in schema "uryplayer"
        ordering = ['-date_submitted']
        get_latest_by = 'date_submitted'
        app_label = 'uryplayer'

    id = exts.primary_key_from_meta(Meta)

    people = models.ManyToManyField(
        Person,
        through='PodcastCredit')

    file = models.FileField(
        upload_to='podcasts',
        help_text="The file containing the podcast audio.")

    ## MAGIC METHODS ##

    def __unicode__(self):
        return u'{0} ({1})'.format(self.title(), self.id)

    ## OVERRIDES ##

    @models.permalink
    def get_absolute_url(self):
        return ('podcast_detail', [str(self.id)])

    def metadata_strands(self):
        return {
            'text': self.podcastmetadata_set,
            'images': self.podcastimagemetadata_set
        }

    def credits_set(self):
        return self.podcastcredit_set

    ## ADDITIONAL METHODS ##

    def embed_code(self):
        """Returns HTML code that can be used to embed this podcast
        in an arbitrary page.

        """
        return (u'<embed height="300"'
                u' width="400"'
                u' flashvars="autostart=false&file={0}&image={3}{1}'
                u'&displayheight=300&width=400&height=300"'
                u' allowfullscreen="false"'
                u' quality="high"'
                u' src="{3}{2}"'
                u' type="application/x-shockwave-flash">'
                .format(
                    self.file.url,
                    self.metadata()['images']['player_image'].url,
                    ''.join((settings.STATIC_URL, 'contrib/player.swf')),
                    'http://ury.org.uk'))

    @staticmethod
    def make_foreign_key(src_meta, db_column='podcast_id'):
        """Shortcut for creating a field that links to a podcast, given the
        source model's metadata class.

        """
        return exts.foreign_key(src_meta, Podcast, db_column, 'podcast')


class PodcastMetadata(Metadata):
    """An item of textual podcast metadata.

    """

    class Meta(Metadata.Meta):
        db_table = 'podcast_metadata'
        verbose_name = 'podcast metadatum'
        verbose_name_plural = 'podcast metadata'
        app_label = 'uryplayer'

    id = exts.primary_key_from_meta(Meta)

    element = Podcast.make_foreign_key(Meta)


class PodcastImageMetadata(ImageMetadata):
    """An item of textual podcast metadata.

    """

    class Meta(Metadata.Meta):
        db_table = 'podcast_image_metadata'
        verbose_name = 'podcast image metadatum'
        verbose_name_plural = 'podcast image metadata'
        app_label = 'uryplayer'

    id = exts.primary_key_from_meta(Meta)

    element = Podcast.make_foreign_key(Meta)
