from django.db import models
from django.contrib.auth import get_user_model
from zinnia.models.entry import Entry

class Like(models.Model):
    user=models.ManyToManyField(get_user_model(), related_name='likes')
    entry=models.ForeignKey(Entry)
    date=models.DateTimeField(auto_now_add=True)
    total_likes=models.IntegerField(default=0)

    # returns (Boolean, Int) - whether the user likes the entry and the total number of likes(=liking users) the entry has

def entry_is_liked(entry, user):
    liked = Like.objects.create(entry=entry)
    try:
        user_liked = Like.objects.get(entry=entry, user=user)
    except:
        user_liked=None
    if user_liked:
        return (True, user_liked.total_likes)
    else:
        return (False, liked.total_likes)
