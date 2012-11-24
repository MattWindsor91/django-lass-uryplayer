"""Generic abstract class for podcast link through-models."""

from django.db import models
from uryplayer.models import Podcast


class PodcastLink(models.Model):
    """A link from a model to a URY podcast.

    Implementors must provide the foreign key to the linked item,
    as well as the primary key.

    """

    class Meta:
        abstract = True
        verbose_name = 'podcast link'
        verbose_name_plural = 'podcast links'

    podcast = Podcast.make_foreign_key(Meta)
