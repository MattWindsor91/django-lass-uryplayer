"""Generic abstract class for podcast link through-models."""

from lass_utils.mixins import AttachableMixin

from uryplayer.models import Podcast


class PodcastLink(AttachableMixin):
    """
    A link from a model to a podcast, implemented as an
    attachable.

    """

    class Meta:
        abstract = True
        verbose_name = 'podcast link'
        verbose_name_plural = 'podcast links'

    podcast = Podcast.make_foreign_key()
