"""Models concerning credits on the URY schedule."""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.db import models
from urysite import model_extensions as exts
from uryplayer.models import Podcast
from people.models import Credit


class PodcastCredit(Credit):
    """The intermediate model for the Podcast<->Person relationship.

    The rationale for the naming is that a PodcastCredit is a "credit"
    (in the "film credits" sense) for a person's role on a given
    podcast.

    """

    class Meta(Credit.Meta):
        db_table = 'podcast_credit'  # In schema "uryplayer"
        app_label = 'uryplayer'
        ordering = ['credit_type__name']

    id = exts.primary_key_from_meta(Meta)

    podcast = models.ForeignKey(
        Podcast,
        db_column='podcast_id',
        help_text='The podcast that the person is being credited for.')
