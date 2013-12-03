from django.test import TestCase

from django.contrib.auth import get_user_model
User=get_user_model()
from zinnia.models.entry import Entry
from . import models
from models import total_entry_likes, entry_is_liked, toggle_like_unlike

class SimpleTest(TestCase):
    def test_basic_addition(self):
        user = User.objects.create_user("Monica Schlicht", "m-schlicht@clearwaters.sky", "2380vh23v")
        entry = Entry.objects.create(title="Who owns Warhol portrait of Fawcett?")

        liked, total = entry_is_liked(entry, user)
        self.assertEqual(liked, False)
        self.assertEqual(total, 0)
        self.assertEqual(total_entry_likes(entry), 0)

        # Like and Unlike the entry several times in a row
        for i in range(5):
            liked, total = toggle_like_unlike(entry, user)
            # Now the user likes the entry
            self.assertEqual(liked, True)
            self.assertEqual(total, 1)
            self.assertEqual(total_entry_likes(entry), 1)

            liked, total = toggle_like_unlike(entry, user)
            # Now the user unliked the entry, back to where we were
            self.assertEqual(liked, False)
            self.assertEqual(total, 0)
            self.assertEqual(total_entry_likes(entry), 0)


        ### One user likes it, then the other, then the forer unlikes, then the latter unlikes

        u2 = User.objects.create_user("Schwarzenegger", "a-r@california.org", "32!!!@FJ#IOJV#E")
        # Now user u2 comes and likes the entry
        liked, total = toggle_like_unlike(entry, u2)
        self.assertEqual(liked, True)
        self.assertEqual(total, 1)
        liked, total = entry_is_liked(entry, user) # No, user doesn't like it
        self.assertEqual(liked, False)
        self.assertEqual(total, 1) # but we see the like of u2
        liked, total = entry_is_liked(entry, u2) # Yes, u2 likes it
        self.assertEqual(liked, True)
        self.assertEqual(total, 1)
        self.assertEqual(total_entry_likes(entry), 1)


        # Now user also likes the entry
        liked, total = toggle_like_unlike(entry, user)
        self.assertEqual(liked, True)
        self.assertEqual(total, 2)
        liked, total = entry_is_liked(entry, user) # Now both like it
        self.assertEqual(liked, True)
        self.assertEqual(total, 2)
        liked, total = entry_is_liked(entry, u2)
        self.assertEqual(liked, True)
        self.assertEqual(total, 2)
        self.assertEqual(total_entry_likes(entry), 2)

        # Now u2 unlikes the entry
        liked, total = toggle_like_unlike(entry, u2)
        self.assertEqual(liked, False)
        self.assertEqual(total, 1) # user still likes it
        liked, total = entry_is_liked(entry, user)
        self.assertEqual(liked, True)
        self.assertEqual(total, 1)
        liked, total = entry_is_liked(entry, u2)
        self.assertEqual(liked, False)
        self.assertEqual(total, 1)
        self.assertEqual(total_entry_likes(entry), 1)

        # Now user also unlikes the entry
        liked, total = toggle_like_unlike(entry, user)
        self.assertEqual(liked, False)
        self.assertEqual(total, 0)
        liked, total = entry_is_liked(entry, user)
        self.assertEqual(liked, False)
        self.assertEqual(total, 0)
        liked, total = entry_is_liked(entry, u2)
        self.assertEqual(liked, False)
        self.assertEqual(total, 0)
        self.assertEqual(total_entry_likes(entry), 0)
        
