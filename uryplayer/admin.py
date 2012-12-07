from django.contrib import admin
from metadata.admin_base import MetadataAdmin, MetadataInline
from uryplayer.models import Podcast
from uryplayer.models import PodcastTextMetadata, PodcastImageMetadata
from uryplayer.models import PodcastChannel
from uryplayer.models import PodcastChannelTextMetadata
from uryplayer.models import PodcastChannelTextMetadataRule


# METADATA


class PodcastMetadataInline(MetadataInline):
    model = PodcastTextMetadata


class PodcastImageMetadataInline(MetadataInline):
    model = PodcastImageMetadata


# PODCAST

class PodcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date_submitted', 'id')
    inlines = [
        PodcastMetadataInline,
        PodcastImageMetadataInline
    ]


# CHANNELS

class PodcastChannelTextMetadataInline(admin.TabularInline):
    model = PodcastChannelTextMetadata


class PodcastChannelTextMetadataRuleInline(admin.TabularInline):
    model = PodcastChannelTextMetadataRule


class PodcastChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [
        PodcastChannelTextMetadataInline,
        PodcastChannelTextMetadataRuleInline
    ]


def register(site):
    """
    Registers the uryplayer admin hooks with an admin site.

    """
    site.register(PodcastTextMetadata, MetadataAdmin)
    site.register(PodcastImageMetadata, MetadataAdmin)
    site.register(Podcast, PodcastAdmin)
    site.register(PodcastChannel, PodcastChannelAdmin)
