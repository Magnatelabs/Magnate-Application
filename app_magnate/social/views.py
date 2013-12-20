from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from zinnia.models.entry import Entry

from .templatetags import social_tags
from django.http import HttpResponseBadRequest
from django.utils import simplejson
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

from .models import toggle_like_unlike, total_entry_likes, StarRating, can_rate
import status_awards

#TODO! FIXME! Think about thread safety if multiple users like the same post at the same time!

# User clicked the "Like" button after a post.
@require_POST
def ajax_like_entry(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    if not request.user.is_authenticated():
        return HttpResponse(status=401)

    vars={}

    user=request.user
    entry_id=request.POST.get('entry_id', None)
    entry=get_object_or_404(Entry, pk=entry_id)

    count = toggle_like_unlike(entry, user)
    status_awards.award_badges("user_liked_entry", user)


    vars['liked'] = (count > 0)
    vars['total_likes'] = total_entry_likes(entry)
    vars['update_html']={social_tags.get_div_dom_id(entry_id) : social_tags.like_entry_button(int(entry_id), user)}
    return HttpResponse(simplejson.dumps(vars), mimetype='application/javascript')

@require_POST
def ajax_star_rating(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    if not request.user.is_authenticated():
        return HttpResponse(status=401)

    value = request.POST.get('value', None)
    if value is None:
        return HttpResponseBadRequest()
    value = int(value)

    vars={}
    user = request.user

    if can_rate(user):
        # Save rating
        StarRating.objects.create(user=user, rating=value)
        # print "User %s rated %d..." % (request.user, value)
        vars['message'] = "Thank you for your feedback!"
    else:
        vars['message'] = "You have already voted in the recent past."

    # Award badges
    status_awards.award_badges("user_rated_something", user)

    return HttpResponse(simplejson.dumps(vars), mimetype='application/javascript')
    
def user_pages(request):
    try:
        id=request.GET.get('user_id', None)
        user=get_object_or_404(get_user_model(), pk=id)
    except ValueError:
        return HttpResponse(status=404)
    return render(request, 'social/users.html', {'user': user})
