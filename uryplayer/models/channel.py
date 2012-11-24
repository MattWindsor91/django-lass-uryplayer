"""Models for the podcast channel system.

Podcast channels are collections of podcasts selected by one or more
filtering schemes based on things such like podcast metadata.

"""

from django.db import models
from metadata.models import Type, Metadata, MetadataKey
from metadata.mixins import MetadataSubjectMixin
from uryplayer.models import PodcastMetadata, Podcast
from urysite import model_extensions as exts

# Match types for textual matching
#              exact?  case-sensitive?
MATCH_TYPES = {False: {False: 'icontains',
                       True: 'contains'},
               True: {False: 'iexact',
                      True:  'exact'}}


class PodcastChannel(Type, MetadataSubjectMixin):
    """A podcast channel definition."""

    class Meta:
        db_table = 'podcast_channel'
        app_label = 'uryplayer'

    id = exts.primary_key_from_meta(Meta)

    def metadata_strands(self):
        return {
            'text': self.podcastchanneltextmetadata_set
        }

    def match_ids(self):
        """Retrieves the IDs of all podcasts in this channel."""
        ids = []
        for rule in self.podcastchanneltextmetadatarule_set.all():
            ids.extend(rule.match_ids())
        return ids

    def latest(self):
        """Retrieves the latest podcast in this channel."""
        try:
            result = Podcast.objects.filter(
                pk__in=self.match_ids()).latest()
        except Podcast.DoesNotExist:
            result = None
        return result


class PodcastChannelTextMetadata(Metadata):
    """An item of text metadata associated with a channel."""

    class Meta(Metadata.Meta):
        db_table = 'podcast_channel_text_metadata'
        app_label = 'uryplayer'

    id = exts.primary_key_from_meta(Meta)

    element = models.ForeignKey(
        PodcastChannel,
        db_column='podcast_channel_id')


class PodcastChannelTextMetadataRule(models.Model):
    """A matching rule that matches any podcast whose textual
    metadata contains or is the given string.

    """

    class Meta:
        db_table = 'podcast_channel_text_metadata_rule'
        app_label = 'uryplayer'

    id = exts.primary_key_from_meta(Meta)

    channel = models.ForeignKey(
        PodcastChannel,
        db_column='podcast_channel_id')

    is_exact = models.BooleanField(
        default=False,
        help_text="""If True, the rule only matches a metadata value
            when the value is exactly that specified in the rule.
            If False, the value only needs to contain the rule value.

            """)

    is_case_sensitive = models.BooleanField(
        default=False,
        help_text="""Determines whether a match only succeeds if the
            matched part of a metadatum value is the same case as the
            rule value.

            """)

    key = models.ForeignKey(
        MetadataKey,
        db_column="metadata_key_id",
        help_text="The key to match against.")

    value = models.TextField(help_text="The value to match against.")

    def match_ids(self):
        """Returns a list of all podcast IDs matched by this rule."""
        filter_args = {
            'key__exact': self.key,
            'value__{0}'.format(
                MATCH_TYPES[self.is_exact][self.is_case_sensitive]):
                    self.value
            }
        return (PodcastMetadata.objects.filter(**filter_args)
                .values_list('element__id', flat=True))

    def matches(self):
        """Returns a queryset of all podcasts this rule matches."""
        return Podcast.objects.filter(pk__in=self.match_ids())
