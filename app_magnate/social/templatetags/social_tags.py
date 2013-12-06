from django import template
from django.shortcuts import get_object_or_404
from ..models import Like, entry_is_liked
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
    user_likes_entry, total_likes = entry_is_liked(entry, user)
    button_text=['Like it', 'Unlike it'][user_likes_entry] + (' (%d)' % (total_likes))
    return '<div id=%s><input type="Button" id="%s" value="%s" style="float: right" onClick="on_click_like_entry(%d, this.id)" /> </div>' % (div_dom_id, dom_id, button_text, entry_id)

