from django import forms
from string import Template
from django.utils.safestring import mark_safe

class ExtraWidget(forms.Widget):
	def render(self, name, value, attrs=None):
#		value = {'current-amount': 1000, 'target-amount' : 5000}
		return mark_safe("<br/>PRE<pre>%s </pre>" %(value))
#		tpl = Template(u"""<h1>There would be a colour widget here, for value $colour</h1>""")
#		return mark_safe(tpl.substitute(colour=value))

	def value_from_datadict(self, data, files, name):
		return {'a':'b'}