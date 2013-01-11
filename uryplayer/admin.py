from django.contrib import admin
from metadata.admin_base import TextMetadataInline
from metadata.admin_base import ImageMetadataInline
from metadata.admin_base import PackageEntryInline
from metadata.admin_base import MetadataAdmin
from uryplayer.models import Podcast
from uryplayer.models import PodcastTextMetadata, PodcastImageMetadata
from uryplayer.models import PodcastPackageEntry
from uryplayer.models import PodcastChannel
from uryplayer.models import PodcastChannelTextMetadata
from uryplayer.models import PodcastChannelTextMetadataRule


# METADATA


class PodcastTextMetadataInline(TextMetadataInline):
    model = PodcastTextMetadata


class PodcastImageMetadataInline(ImageMetadataInline):
    model = PodcastImageMetadata


class PodcastPackageEntryInline(PackageEntryInline):
    model = PodcastPackageEntry

# PODCAST

class PodcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date_submitted', 'id')
    inlines = [
        PodcastPackageEntryInline,
        PodcastTextMetadataInline,
        PodcastImageMetadataInline,
    ]

    # These are needed because title and description are pseudo
    # attributes exported through the metadata system.

    def title(self, obj):
        return obj.title

    def description(self, obj):
        return obj.description


# CHANNELS

class PodcastChannelTextMetadataInline(TextMetadataInline):
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
