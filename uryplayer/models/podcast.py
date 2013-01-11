"""
This module contains the :class:`Podcast` model and support models.

"""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.conf import settings
from django.db import models
from metadata.models import TextMetadata, ImageMetadata
from metadata.models import PackageEntry
from metadata.mixins import MetadataSubjectMixin
from lass_utils.mixins import SubmittableMixin
from people.models import Person
from people.mixins import ApprovableMixin
from people.mixins import CreatableMixin
from people.mixins import CreditableMixin


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
        return u'{0} ({1})'.format(
            getattr(self, 'title', '((Untitled))'),
            self.id
        )

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
            'image': self.podcastimagemetadata_set
        }

    def packages(self):
        """
        Returns the set of package entries attached to a
        podcast.

        """
        return self.podcastpackageentry_set

    def credits_set(self):
        """
        Returns the related manager representing the podcast credits.

        """
        return self.podcastcredit_set

    ## ADDITIONAL METHODS ##

    @classmethod
    def make_foreign_key(cls):
        """
        Shortcut for creating a field that links to a podcast.

        """
        _FKEY_KWARGS = {}
        if hasattr(settings, 'PODCAST_DB_FKEY_COLUMN'):
            _FKEY_KWARGS['db_column'] = (
                settings.PODCAST_DB_FKEY_COLUMN
            )
        return models.ForeignKey(
            cls,
            help_text='The podcast associated with this item.',
            **_FKEY_KWARGS
        )

    ## METADATA ##

    class Meta:
        if hasattr(settings, 'PODCAST_DB_TABLE'):
            db_table = settings.PODCAST_DB_TABLE
        ordering = ['-date_submitted']
        get_latest_by = 'date_submitted'
        app_label = 'uryplayer'


# Automagic metadata models #

PodcastPackageEntry = PackageEntry.make_model(
    Podcast,
    'uryplayer',
    'PodcastPackageEntry',
    getattr(settings, 'PODCAST_PACKAGE_ENTRY_DB_TABLE', None),
    getattr(settings, 'PODCAST_PACKAGE_ENTRY_DB_ID_COLUMN', None),
    help_text='The podcast associated with this package entry.',
    fkey=Podcast.make_foreign_key()
)

PodcastTextMetadata = TextMetadata.make_model(
    Podcast,
    'uryplayer',
    'PodcastTextMetadata',
    getattr(settings, 'PODCAST_TEXT_METADATA_DB_TABLE', None),
    getattr(settings, 'PODCAST_TEXT_METADATA_DB_ID_COLUMN', None),
    help_text='The podcast associated with this textual metadata.',
    fkey=Podcast.make_foreign_key()
)

PodcastImageMetadata = ImageMetadata.make_model(
    Podcast,
    'uryplayer',
    'PodcastImageMetadata',
    getattr(settings, 'PODCAST_IMAGE_METADATA_DB_TABLE', None),
    getattr(settings, 'PODCAST_IMAGE_METADATA_DB_ID_COLUMN', None),
    getattr(settings, 'PODCAST_IMAGE_METADATA_DB_FKEY_COLUMN', None),
    help_text='The podcast associated with this image metadata.',
    fkey=Podcast.make_foreign_key()
)
