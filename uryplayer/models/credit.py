"""Models concerning credits on URY podcasts."""

# IF YOU'RE ADDING CLASSES TO THIS, DON'T FORGET TO ADD THEM TO
# __init__.py

from django.conf import settings
from django.db import models
from uryplayer.models import Podcast
from people.models import Credit


class PodcastCredit(Credit):
    """
    The intermediate model for the Podcast<->Person relationship.

    The rationale for the naming is that a PodcastCredit is a "credit"
    (in the "film credits" sense) for a person's role on a given
    podcast.

    """
    if hasattr(settings, 'PODCAST_CREDIT_DB_ID_COLUMN'):
        id = models.AutoField(
            primary_key=True,
            db_column=settings.PODCAST_CREDIT_DB_ID_COLUMN
        )
    podcast = Podcast.make_foreign_key()

    class Meta(Credit.Meta):
        if hasattr(settings, 'PODCAST_CREDIT_DB_TABLE'):
            db_table = settings.PODCAST_CREDIT_DB_TABLE
        app_label = 'uryplayer'
        ordering = ['credit_type__name']
