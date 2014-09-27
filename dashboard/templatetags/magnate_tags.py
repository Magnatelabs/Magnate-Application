from django import template

register=template.Library()

@register.inclusion_tag('dashboard/_entry_feed.html')
def entry_feed(entries, pagination=True):
	return {
		'entries': entries,
		'pagination': pagination,
	}