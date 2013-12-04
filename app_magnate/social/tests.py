from django.test import TestCase

from django.contrib.auth import get_user_model
User=get_user_model()
from zinnia.models.entry import Entry
from . import models
from models import total_entry_likes, entry_is_liked, toggle_like_unlike

import random
random.seed(2746833)
from random import randrange

class SimpleTest(TestCase):
    def test_basic_addition(self):
        user = User.objects.create_user("Monica Schlicht", "m-schlicht@clearwaters.sky", "2380vh23v")
        entry = Entry.objects.create(title="Who owns Warhol portrait of Fawcett?")

        self.assertEqual(entry_is_liked(entry, user), 0)
        self.assertEqual(total_entry_likes(entry), 0)

        # Like and Unlike the entry several times in a row
        for i in range(5):
            count = toggle_like_unlike(entry, user)
            # Now the user likes the entry
            self.assertEqual(count, 1)
            self.assertEqual(total_entry_likes(entry), 1)

            count = toggle_like_unlike(entry, user)
            # Now the user unliked the entry, back to where we were
            self.assertEqual(count, 0)
            self.assertEqual(total_entry_likes(entry), 0)


        ### One user likes it, then the other, then the forer unlikes, then the latter unlikes

        u2 = User.objects.create_user("Schwarzenegger", "a-r@california.org", "32!!!@FJ#IOJV#E")
        # Now user u2 comes and likes the entry
        count = toggle_like_unlike(entry, u2)
        self.assertEqual(count, 1)
        count = entry_is_liked(entry, user) # No, user doesn't like it
        self.assertEqual(count, 0) 
        self.assertEqual(total_entry_likes(entry), 1) # but we see the like of u2
        count = entry_is_liked(entry, u2) # Yes, u2 likes it
        self.assertEqual(count, 1)


        # Now user also likes the entry
        count = toggle_like_unlike(entry, user)
        self.assertEqual(count, 1)
        count = entry_is_liked(entry, user) # Now both like it
        self.assertEqual(count, 1)
        count = entry_is_liked(entry, u2)
        self.assertEqual(count, 1)
        self.assertEqual(total_entry_likes(entry), 2)

        # Now u2 unlikes the entry
        count = toggle_like_unlike(entry, u2)
        self.assertEqual(count, 0) # user still likes it
        count = entry_is_liked(entry, user)
        self.assertEqual(count, 1)
        count = entry_is_liked(entry, u2)
        self.assertEqual(count, 0)
        self.assertEqual(total_entry_likes(entry), 1)

        # Now user also unlikes the entry
        count = toggle_like_unlike(entry, user)
        self.assertEqual(count, 0)
        count = entry_is_liked(entry, user)
        self.assertEqual(count, 0)
        count = entry_is_liked(entry, u2)
        self.assertEqual(count, 0)
        self.assertEqual(total_entry_likes(entry), 0)
     
 
    def do_many(self, n_users, n_entries, n_repetitions):
        users=[]
        for i in range(n_users):
            users.append(User.objects.create_user("User %d" % (i), "user-%d@people.biz" % (i), "12345678987654321"))
        entries=[]
        for i in range(n_entries):
            entries.append(Entry.objects.create(title="Entry %d" % (i)))
        likes=[[False for e in entries] for u in users]

        for r in range(n_repetitions):
            u_ind=randrange(n_users)
            user=users[u_ind]
            e_ind=randrange(n_entries)
            entry=entries[e_ind]
            self.assertEqual(entry_is_liked(entry, user), int(likes[u_ind][e_ind]))
            result=toggle_like_unlike(entry, user)
            likes[u_ind][e_ind] = not likes[u_ind][e_ind]
            self.assertEqual(entry_is_liked(entry, user), int(likes[u_ind][e_ind]))
            self.assertEqual(result, int(likes[u_ind][e_ind]))
            self.assertEqual(total_entry_likes(entry), len([ui for ui in range(n_users) if likes[ui][e_ind]]))

    def test_random(self):
        self.do_many(1, 1, 100)
