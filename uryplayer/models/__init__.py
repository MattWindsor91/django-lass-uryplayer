# Import all models, in an order such that models only depend on
# models further up the list
from uryplayer.models.podcast import Podcast
Podcast = Podcast

from uryplayer.models.podcast import PodcastPackageEntry
PodcastPackageEntry = PodcastPackageEntry

from uryplayer.models.podcast import PodcastTextMetadata
PodcastTextMetadata = PodcastTextMetadata

from uryplayer.models.podcast import PodcastImageMetadata
PodcastImageMetadata = PodcastImageMetadata

from uryplayer.models.podcast_link import PodcastLink
PodcastLink = PodcastLink

from uryplayer.models.credit import PodcastCredit
PodcastCredit = PodcastCredit

from uryplayer.models.channel import PodcastChannel
PodcastChannel = PodcastChannel

from uryplayer.models.channel import PodcastChannelTextMetadata
PodcastChannelTextMetadata = PodcastChannelTextMetadata

from uryplayer.models.channel import PodcastChannelTextMetadataRule
PodcastChannelTextMetadataRule = PodcastChannelTextMetadataRule
