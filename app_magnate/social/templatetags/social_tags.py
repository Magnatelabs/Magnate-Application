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
    button_text=['Like it', 'Unlike it'][user_likes_entry] + (' (%d)' % (total_likes))

    if user.is_authenticated():
        on_click='on_click_like_entry(%d, this.id)' % (entry_id)
    else:
        on_click='alert(\'Please, log in to like or unlike posts\')'
    return '<div id=%s><input type="Button" id="%s" value="%s" style="float: right" onClick="%s" /> </div>' % (div_dom_id, dom_id, button_text, on_click)


# Need context to create csrf token
@register.simple_tag(takes_context = True)
def render_star_rating(context, user):
    if can_rate(user):
        return render_to_string('social/_star_rating.html', {}, context_instance=context)
    else:
        return ''
