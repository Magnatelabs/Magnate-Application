from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import get_object_or_404
from zinnia.models.entry import Entry

from .templatetags import social_tags
from django.http import HttpResponseBadRequest
from django.utils import simplejson
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import toggle_like_unlike, total_entry_likes, StarRating
import status_awards

#TODO! FIXME! Think about thread safety if multiple users like the same post at the same time!

# User clicked the "Like" button after a post.
def ajax_like_entry(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    if not request.user.is_authenticated():
        return HttpResponse(status=401)

    vars={}
    if request.method=='POST':
        user=request.user
        entry_id=request.POST.get('entry_id', None)
        entry=get_object_or_404(Entry, pk=entry_id)

        count = toggle_like_unlike(entry, user)
        status_awards.award_badges("user_liked_entry", user)


        vars['liked'] = (count > 0)
        vars['total_likes'] = total_entry_likes(entry)
        vars['update_html']={social_tags.get_div_dom_id(entry_id) : social_tags.like_entry_button(int(entry_id), user)}
        return HttpResponse(simplejson.dumps(vars), mimetype='application/javascript')
    else:
        return HttpResponseBadRequest()

@require_POST
@login_required
def ajax_star_rating(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    value = int(request.POST.get('value', None))
    if value is None:
        return HttpResponseBadRequest()

        

    # Save rating
    StarRating.objects.create(user=request.user, rating=value)
    # Award badges
    print "User %s rated %d..." % (request.user, value)

    return HttpResponse(simplejson.dumps({}), mimetype='application/javascript')
    
