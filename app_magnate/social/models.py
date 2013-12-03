from django.db import models
from django.contrib.auth import get_user_model
from zinnia.models.entry import Entry

class Like(models.Model):
    user=models.ManyToManyField(get_user_model(), related_name='likes')
    entry=models.ForeignKey(Entry)
    date=models.DateTimeField(auto_now_add=True)
    total_likes=models.IntegerField(default=0)

    # returns (Boolean, Int) - whether the user likes the entry and the total number of likes(=liking users) the entry has

def total_entry_likes(entry):
    #    return Like.objects.filter(entry=entry).count()
    return sum([l.total_likes for l in Like.objects.filter(entry=entry)])

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


# If the user likes the entry, now it will be unliked, and vice versa.
# Returns (bool, int), i.e. liked = Like.objects.create(entry=entry)
def toggle_like_unlike(entry, user):
        liked = Like.objects.create(entry=entry)
        try:
            user_liked = Like.objects.get(entry=entry, user=user)
        except:
            user_liked=None
        if user_liked:  # If the "Like" object already existed. (We did not save the new one yet.)
            user_liked.total_likes -= 1
            user_liked.user.remove(user) 
            user_liked.save() # Decreased the number of likes by one. Second "Like" is interpreted as "Unlike"
            return (False, user_liked.total_likes)
        else: # It's a new "Like", not an "Unlike"
            liked.user.add(user)
            liked.total_likes += 1
            liked.save()
            return (True, liked.total_likes)
