from django import template
from django.conf import settings

register=template.Library()


@register.simple_tag
def render_badge(badge, size):
    sizes = {0:92, 5:130, 10:256}
    assert size in sizes, "Cannot render badge at size %d. This size is not supported" % (size)
    picture_url = "%sstatus_awards/badge_%s_%d.png" % (settings.STATIC_URL, badge.slug, badge.level)
    return "<img src=\"%s\" width=\"%dpx\" height=\"%dpx\" alt=\"%s\" >" % (picture_url, sizes[size], sizes[size], badge.name)
