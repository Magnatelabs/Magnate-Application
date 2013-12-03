from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import get_object_or_404
from zinnia.models.entry import Entry
from .models import Like
from .templatetags import social_tags

#TODO! FIXME! Think about thread safety if multiple users like the same post at the same time!

# User clicked the "Like" button after a post.
def ajax_like_entry(request):
    vars={}
    if request.method=='POST':
        user=request.user
        entry_id=request.POST.get('entry_id', None)
        entry=get_object_or_404(Entry, pk=entry_id)
        liked = Like.objects.create(entry=entry)
        try:
            user_liked = Like.objects.get(entry=entry, user=user)
        except:
            user_liked=None
        if user_liked: # If the "Like" object already existed. (We did not save the new one yet.)
            user_liked.total_likes -= 1
            user_liked.user.remove(request.user) 
            user_liked.save() # Decreased the number of likes by one. Second "Like" is interpreted as "Unlike"
#            print "Unliked!"
            vars['liked']=False
            vars['total_likes']=user_liked.total_likes
            vars['message']="Thank you for unliking! Now %d likes" % (user_liked.total_likes)
        else: # It's a new "Like", not an "Unlike"
            liked.user.add(request.user)
            liked.total_likes += 1
            liked.save()
#            print "Liked!"
            vars['liked']=True
            vars['total_likes']=liked.total_likes
            vars['message']="Thank you for liking! Now %d likes" % (liked.total_likes)
  
        vars['update_html']={social_tags.get_div_dom_id(entry_id) : social_tags.like_entry_button(int(entry_id), user)}
    return HttpResponse(simplejson.dumps(vars), mimetype='application/javascript')
