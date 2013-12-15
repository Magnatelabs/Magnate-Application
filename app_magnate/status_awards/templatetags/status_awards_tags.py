from django import template
from django.conf import settings
from brabeion.models import BadgeAward

register=template.Library()


NO_STATUS_PIC_URL = 'status_awards/badge_no_status.png'

@register.simple_tag
def render_badge(badge, size):
    sizes = {"small" : "width=\"92px\" height=\"92px\"", 
            "medium" : "width=\"130px\" height=\"130px\"", 
             "large" : "width=\"256px\" height=\"256px\"",
       "status_icon" : "width=\"68px\" height=\"46px\"",
      "status_large" : "width=\"268px\" height=\"184px\"" }
    assert size in sizes, "Cannot render badge at size %d. This size is not supported" % (size)
    if isinstance(badge, BadgeAward):
        picture_url = "%sstatus_awards/badge_%s_%d.png" % (settings.STATIC_URL, badge.slug, badge.level)
        alt = badge.name
    else:
        picture_url=settings.STATIC_URL + settings.MAGNATE_NO_STATUS_PIC_URL
        alt="No status"
    return "<img src=\"%s\" %s alt=\"%s\" >" % (picture_url, sizes[size], alt)

@register.filter(name='no_metabadges')
def no_metabadges(list):
    return [badge for badge in list if not badge.is_metabadge()]
