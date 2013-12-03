from django.test import TestCase

from django.contrib.auth import get_user_model
User=get_user_model()
from zinnia.models.entry import Entry
from . import models
from models import total_entry_likes

class SimpleTest(TestCase):
    def test_basic_addition(self):
        user = User.objects.create_user("Monica Schlicht", "m-schlicht@clearwaters.sky", "2380vh23v")
        entry = Entry.objects.create(title="Who owns Warhol portrait of Fawcett?")

        liked, total = models.entry_is_liked(entry, user)
        self.assertEqual(liked, False)
        self.assertEqual(total, 0)
        self.assertEqual(total_entry_likes(entry), 0)

        # Like and Unlike the entry several times in a row
        for i in range(5):
            liked, total = models.toggle_like_unlike(entry, user)
            # Now the user likes the entry
            self.assertEqual(liked, True)
            self.assertEqual(total, 1)
            self.assertEqual(total_entry_likes(entry), 1)

            liked, total = models.toggle_like_unlike(entry, user)
            # Now the user unliked the entry, back to where we were
            self.assertEqual(liked, False)
            self.assertEqual(total, 0)
            self.assertEqual(total_entry_likes(entry), 0)
