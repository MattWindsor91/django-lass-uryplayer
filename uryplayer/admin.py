from django.contrib import admin
from metadata.admin_base import MetadataAdmin, MetadataInline
from uryplayer.models import Podcast
from uryplayer.models import PodcastMetadata, PodcastImageMetadata
from uryplayer.models import PodcastChannel
from uryplayer.models import PodcastChannelTextMetadata
from uryplayer.models import PodcastChannelTextMetadataRule


# METADATA
admin.site.register(PodcastMetadata, MetadataAdmin)
admin.site.register(PodcastImageMetadata, MetadataAdmin)


class PodcastMetadataInline(MetadataInline):
    model = PodcastMetadata


class PodcastImageMetadataInline(MetadataInline):
    model = PodcastImageMetadata


# PODCAST

class PodcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date_submitted', 'id')
    inlines = [
        PodcastMetadataInline,
        PodcastImageMetadataInline
    ]


admin.site.register(Podcast, PodcastAdmin)


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


admin.site.register(PodcastChannel, PodcastChannelAdmin)
