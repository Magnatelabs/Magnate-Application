from django import template
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from ..models import Like, entry_is_liked, total_entry_likes, can_rate
from zinnia.models.entry import Entry

register=template.Library()

def get_button_dom_id(entry_id):
    return 'like-' + str(entry_id)

def get_div_dom_id(entry_id):
    return 'div-' + get_button_dom_id(entry_id)

@register.simple_tag
def like_entry_button(entry_id, user): # entry_id is an integer
    dom_id = get_button_dom_id(entry_id)
    div_dom_id = get_div_dom_id(entry_id)
    entry=get_object_or_404(Entry, pk=entry_id)
    user_likes_entry = entry_is_liked(entry, user)
    total_likes = total_entry_likes(entry) # total number of users who like it
    button_text=['Mark', 'Unmark'][user_likes_entry] + (' (%d)' % (total_likes))

    ctx = {'div_dom_id': div_dom_id, 'dom_id': dom_id, 'button_text': button_text, 'entry_id': entry_id, 'user': user}
    return render_to_string('social/_like_button.html', ctx)

# Need context to create csrf token
@register.simple_tag(takes_context = True)
def render_star_rating(context, user):
    if user.is_authenticated() and can_rate(user):
        return render_to_string('social/_star_rating.html', {}, context_instance=context)
    else:
        return ''
