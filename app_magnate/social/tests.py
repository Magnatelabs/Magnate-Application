from django.test import TestCase

from django.contrib.auth import get_user_model
User=get_user_model()
from zinnia.models.entry import Entry
from . import models
from models import total_entry_likes, entry_is_liked, toggle_like_unlike, total_likes_by_user
from .models import Like, StarRating
from .templatetags import social_tags
import status_awards

import random
from random import randrange
import datetime

from django.test.client import Client
from django.core.urlresolvers import reverse
import json

class SimpleTest(TestCase):
    def test_basic(self):
        # Make sure we are testing with sqlite3
        from django.db import settings
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')

        user = User.objects.create_user("Monica Schlicht", "m-schlicht@clearwaters.sky", "2380vh23v")
        entry = Entry.objects.create(title="Who owns Warhol portrait of Fawcett?")

        self.assertEqual(entry_is_liked(entry, user), 0)
        self.assertEqual(total_entry_likes(entry), 0)
        self.assertEqual(total_likes_by_user(user), 0)

        # Like and Unlike the entry several times in a row
        for i in range(5):
            count = toggle_like_unlike(entry, user)
            # Now the user likes the entry
            self.assertEqual(count, 1)
            self.assertEqual(total_entry_likes(entry), 1)
            self.assertEqual(total_likes_by_user(user), 1)

            count = toggle_like_unlike(entry, user)
            # Now the user unliked the entry, back to where we were
            self.assertEqual(count, 0)
            self.assertEqual(total_entry_likes(entry), 0)
            self.assertEqual(total_likes_by_user(user), 0)




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
     




    def setup_random(self):
        random.seed(834932784)
        self.users=[]
        for i in range(20):
            self.users.append(User.objects.create_user("User %d" % (i), "user-%d@people.biz" % (i), "12345678987654321"))
        self.entries=[]
        for i in range(20):
            self.entries.append(Entry.objects.create(title="Entry %d" % (i)))

    def tearDown(self):
        Like.objects.all().delete()

    # Start with n_user users and n_entries entries. Then, using pseudorandom generation, 
    # for n_repetition steps, randomly like/unlike entries. Maintain a two-dimensional array of booleans
    # and see if everything works as expected.
    def do_many(self, n_users, n_entries, n_repetitions):
        likes=[[False for e in self.entries] for u in self.users]

        for r in range(n_repetitions):
            u_ind=randrange(n_users)
            user=self.users[u_ind]
            e_ind=randrange(n_entries)
            entry=self.entries[e_ind]
            self.assertEqual(entry_is_liked(entry, user), likes[u_ind][e_ind])
            result=toggle_like_unlike(entry, user)
            likes[u_ind][e_ind] = not likes[u_ind][e_ind]
            self.assertEqual(entry_is_liked(entry, user), likes[u_ind][e_ind])
            self.assertEqual(result, int(likes[u_ind][e_ind]))
            self.assertEqual(total_entry_likes(entry), len([ui for ui in range(n_users) if likes[ui][e_ind]]))
            self.assertEqual(total_likes_by_user(user), len([ei for ei in range(n_entries) if likes[u_ind][ei]]))
        Like.objects.all().delete()

    def test_rand_1(self):
        self.setup_random()
        self.do_many(1, 1, 15)
        self.do_many(1, 2, 7)
        self.do_many(2, 1, 7)
        self.do_many(2, 2, 20)
        self.do_many(10, 10, 75)

    def test_templatetags(self):
        user = User.objects.create_user("Monica Schlicht", "m-schlicht@clearwaters.sky", "2380vh23v")
        entry = Entry.objects.create(title="Who owns Warhol portrait of Fawcett?")
        html = social_tags.like_entry_button(entry.pk, user)
        self.assertTrue(social_tags.get_div_dom_id(entry.pk) in html)
        self.assertTrue(social_tags.get_button_dom_id(entry.pk) in html)


    def test_ajax_like(self):
        client = Client()
        url=reverse('ajax_like_entry')
        # User not authenticated. Expected AJAX response HTTP 401.
        response401=client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest', )
        self.assertEqual(response401.status_code, 401)

        #Loggging in...
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        client.login(username='temporary', password='temporary')
        #Logged in

        # Now we are logged in and the request is ajax, but the data do not include entry_id
        response404=client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest', )
        self.assertEqual(response404.status_code, 404)


        
        # Now using nonexistent entry_id = 17
        data =  {'entry_id' : '17',}
        response404=client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')  
        self.assertEqual(response404.status_code, 404)

        
        # Create lots of users and entries...
        self.setup_random()
        # Now #17 exists. Just double-check; will raise DoesNotExist if anything.
        Entry.objects.get(pk=17)

        #try again
        response=client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')  

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._headers['content-type'], ('Content-Type', 'application/javascript'))
        resp_data = json.loads(response.content)

        # The user just liked an Entry
        self.assertEqual(resp_data['liked'], True)
        # Nobody else likes it so far
        self.assertEqual(resp_data['total_likes'], 1)
        # resp_data['update_html'] contains html to update the div
        self.assertTrue('update_html' in resp_data)
        # the html should send something about unliking, since the user has just liked it
        # We expect resp_data["update_html"] to be like {"div-like-17": "<div id=div-like-17><input type=\"Button\" id=\"like-17\" value=\"Unlike it (1)\" style=\"float: right\" onClick=\"on_click_like_entry(17, this.id)\" /> </div>"}
        self.assertTrue('unlike' in str(resp_data['update_html']).lower())



        # TODO: this is temporary check
        # Of course, the list of badges may change
        # But for now we know that there should be 1 badge awarded
        self.assertEquals(user.badges_earned.count(), 1)
        self.assertIsInstance(user.badges_earned.all()[0]._badge, status_awards.test_badges.TestLikesBadge_0)




        # Try an AJAX GET request
        response405=client.get(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response405.status_code, 405)


        # Try a POST request that is not AJAX.. Expected HTTP 400.
        response400=client.post(url, data)
        self.assertEqual(response400.status_code, 400)

        # Lastly, try a GET request that is not AJAX. Expected HTTP 400.
        response405=client.get(url, data)
        self.assertEqual(response405.status_code, 405)

        
    def test_ajax_star_rating(self):
        client = Client()
        url=reverse('ajax_star_rating')
        # User not authenticated. Expected AJAX response HTTP 401.
        response401=client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest', )
        self.assertEqual(response401.status_code, 401)

        #Loggging in...
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        client.login(username='temporary', password='temporary')
        #Logged in

        # Now we are logged in and the request is ajax, but the data do not include rating. Bad request...
        response400=client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest', )
        self.assertEqual(response400.status_code, 400)

        data = {'value': '5', }
        
        #try again
        response=client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')  
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._headers['content-type'], ('Content-Type', 'application/javascript'))
        resp_data = json.loads(response.content)

        # The user has just rated something (the website)

        self.assertTrue('message' in resp_data)
        self.assertEquals(resp_data['message'], "Thank you for your feedback!")

        # So far the user has rated once
        self.assertEquals(user.ratings.count(), 1)
        self.assertEqual(StarRating.objects.filter(user=user).count(), 1)

        self.assertEqual(user.badges_earned.count(), 1)
        self.assertIsInstance(user.badges_earned.all()[0]._badge, status_awards.test_badges.FearlessRaterBadge)


        # NOW try voting again!
        data = {'value': '2', }
        response=client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')   
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._headers['content-type'], ('Content-Type', 'application/javascript'))
        resp_data = json.loads(response.content)

        # The user has just tried to rate the same item again

        self.assertTrue('message' in resp_data)
        self.assertEquals(resp_data['message'], "You have already voted in the recent past.")
        # Still one rating
        self.assertEqual(user.ratings.count(), 1)
        # Namely, rating 5. The first one.
        self.assertEqual(user.ratings.all()[0].rating, 5)

        # Still one badge
        self.assertEqual(user.badges_earned.count(), 1)
       


        # NOW
        # Say, we can rate again after a day
        from django.db import settings
        settings.MAGNATE_CAN_STAR_RATE_EVERY = 'days=1'
        
        # Say, the user actually rated this item 23 hours ago
        r=user.ratings.all()[0]
        r.date = r.date - datetime.timedelta(hours=23)
        r.save()
        
        # He still shouldn't be able to rate again!
        response=client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')   
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._headers['content-type'], ('Content-Type', 'application/javascript'))
        resp_data = json.loads(response.content)
        self.assertTrue('message' in resp_data)
        self.assertEquals(resp_data['message'], "You have already voted in the recent past.")
        # Still one rating
        self.assertEqual(user.ratings.count(), 1)
        # Namely, rating 5. The first one.
        self.assertEqual(user.ratings.all()[0].rating, 5)
        # Still one badge
        self.assertEqual(user.badges_earned.count(), 1)



        # Now, say, the user actually rated this item 25 hours ago
        r=user.ratings.all()[0]
        r.date = r.date - datetime.timedelta(hours=2) # shift back two more hours
        r.save()


        # Now he should be able to rate again! (This is also a nice check for timezones, etc.)
        data = {'value': '1', }
        response=client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')   
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._headers['content-type'], ('Content-Type', 'application/javascript'))
        resp_data = json.loads(response.content)
        self.assertTrue('message' in resp_data)
        self.assertEquals(resp_data['message'], "Thank you for your feedback!")
        # Now two ratings
        self.assertEqual(user.ratings.count(), 2)
        self.assertEqual(sorted([r.rating for r in user.ratings.all()]), [1, 5])
        # Now two badges (same badge, but earned on two levels)
        self.assertEqual(user.badges_earned.count(), 2)
        self.assertEqual(sorted([(b.slug, b.level) for b in user.badges_earned.all()]), [('fearless-rater', 0), ('fearless-rater', 1)])



        # Try an AJAX GET request
        response405=client.get(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response405.status_code, 405)


        # Try a POST request that is not AJAX.. Expected HTTP 400.
        response400=client.post(url, data)
        self.assertEqual(response400.status_code, 400)

        # Lastly, try a GET request that is not AJAX. Expected HTTP 400.
        response405=client.get(url, data)
        self.assertEqual(response405.status_code, 405)
