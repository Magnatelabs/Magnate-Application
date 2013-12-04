from django.db import models
from django.contrib.auth import get_user_model
from zinnia.models.entry import Entry

# Every instance will represent one Like of one entry by one user
class Like(models.Model):
    user=models.ForeignKey(get_user_model(), related_name='likes')
    entry=models.ForeignKey(Entry)
    date=models.DateTimeField(auto_now_add=True)
    count=models.IntegerField(default=0) # This is typically 0/1

    # returns (Boolean, Int) - whether the user likes the entry and the total number of likes(=liking users) the entry has

def total_entry_likes(entry):
    #    return Like.objects.filter(entry=entry).count()
    return sum([l.count for l in Like.objects.filter(entry=entry)])


    

def entry_liked_count(entry, user):
    try:
        like = Like.objects.get(entry=entry, user=user)
        return like.count
    except:
        return 0

def entry_is_liked(entry, user):
    return entry_liked_count(entry, user) > 0



# If the user likes the entry, now it will be unliked, and vice versa.
# Returns (bool, int), i.e. liked = Like.objects.create(entry=entry)
def toggle_like_unlike(entry, user):
        try:
            like = Like.objects.get(entry=entry, user=user)
        except:
            like=None
        if like: 
            if (like.count == 0):
                like.count = 1
            else:
                like.count = 0
        else: # It's a new "Like", not an "Unlike"
            like = Like.objects.create(entry=entry, user=user)
            like.count = 1
        like.save()
        return like.count
