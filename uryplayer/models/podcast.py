"""
This module contains the :class:`Podcast` model and support models.

"""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.conf import settings
from django.db import models
from metadata.models import TextMetadata, ImageMetadata
from metadata.mixins import MetadataSubjectMixin
from lass_utils.mixins import SubmittableMixin
from people.models import Person
from people.mixins import ApprovableMixin
from people.mixins import CreatableMixin
from people.mixins import CreditableMixin


# Make sure the database column is correctly set up for the
# podcast foreign key.
POD_KW = {}
if hasattr(settings, 'PODCAST_CREDIT_DB_PODCAST_COLUMN'):
    POD_KW['db_column'] = settings.PODCAST_CREDIT_DB_PODCAST_COLUMN
elif hasattr(settings, 'PODCAST_CREDIT_DB_ID_COLUMN'):
    POD_KW['db_column'] = settings.PODCAST_CREDIT_DB_ID_COLUMN


class Podcast(MetadataSubjectMixin,
              SubmittableMixin,
              ApprovableMixin,
              CreatableMixin,
              CreditableMixin):
    """
    A podcast in the URY player.

    This model's primary key and database table are changeable by
    supplying settings for ``PODCAST_DB_ID_COLUMN`` and
    ``PODCAST_DB_TABLE`` respectively.

    """
    if hasattr(settings, 'PODCAST_DB_ID_COLUMN'):
        id = models.AutoField(
            primary_key=True,
            db_column=settings.PODCAST_DB_ID_COLUMN
        )
    people = models.ManyToManyField(
        Person,
        through='PodcastCredit'
    )
    file = models.FileField(
        upload_to='podcasts',
        help_text="The file containing the podcast audio."
    )

    ## MAGIC METHODS ##

    def __unicode__(self):
        return u'{0} ({1})'.format(self.title(), self.id)

    ## OVERRIDES ##

    @models.permalink
    def get_absolute_url(self):
        return ('podcast_detail', [str(self.id)])

    def metadata_strands(self):
        """
        Returns the set of metadata strands that this podcast model
        attaches to.

        """
        return {
            'text': self.podcasttextmetadata_set,
            'images': self.podcastimagemetadata_set
        }

    def credits_set(self):
        """
        Returns the related manager representing the podcast credits.

        """
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

    @classmethod
    def make_foreign_key(cls):
        """
        Returns a model field that will create a foreign key link
        to this model.

        """
        return models.ForeignKey(
            cls,
            help_text='The podcast this item relates to.',
            **POD_KW
        )

    ## METADATA ##

    class Meta:
        if hasattr(settings, 'PODCAST_DB_TABLE'):
            db_table = settings.PODCAST_DB_TABLE
        ordering = ['-date_submitted']
        get_latest_by = 'date_submitted'
        app_label = 'uryplayer'


# Automagic metadata models #

PodcastTextMetadata = TextMetadata.make_model(
    Podcast,
    'uryplayer',
    'PodcastTextMetadata',
    getattr(settings, 'PODCAST_TEXT_METADATA_DB_TABLE', None),
    getattr(settings, 'PODCAST_TEXT_METADATA_DB_ID_COLUMN', None),
    getattr(settings, 'PODCAST_TEXT_METADATA_DB_FKEY_COLUMN', None),
    'The podcast associated with this textual metadata.',
)


PodcastImageMetadata = ImageMetadata.make_model(
    Podcast,
    'uryplayer',
    'PodcastImageMetadata',
    getattr(settings, 'PODCAST_IMAGE_METADATA_DB_TABLE', None),
    getattr(settings, 'PODCAST_IMAGE_METADATA_DB_ID_COLUMN', None),
    getattr(settings, 'PODCAST_IMAGE_METADATA_DB_FKEY_COLUMN', None),
    'The podcast associated with this image metadata.',
)
