"""
Tests for the URYPlayer system.

"""

from django.test import TestCase
from django.contrib import admin

from uryplayer.models import podcast, channel
from uryplayer import admin as ua


class AdminTest(TestCase):
    """
    Tests to make sure that the admin snap-ins validate correctly.

    """
    def setUp(self):
        self.site = admin.AdminSite()

    def test_admin_registration(self):
        """
        Tests that registering the admin hooks with an admin site
        yields no exceptions.

        """
        ua.register(self.site)
        self.assertTrue(
            isinstance(
                self.site._registry[podcast.Podcast],
                ua.PodcastAdmin
            )
        )
        self.assertTrue(
            isinstance(
                self.site._registry[channel.PodcastChannel],
                ua.PodcastChannelAdmin
            )
        )
