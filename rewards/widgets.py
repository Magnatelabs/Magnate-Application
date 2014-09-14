from django import forms
from django.template import loader, Context

class ExtraWidget(forms.Widget):
	def render(self, name, value, attrs=None):
		t = loader.get_template("rewards/_admin_extra_widget.html")
		# Value None means there is no extra data.
		# Value False means it is a new model and has to be saved first.
		# Otherwise we expect a dictionary.
		c = Context({ 'keyvalue': value.items() if type(value)==dict else value })
		return t.render(c)

	# We have prefixed all text input names with _aew_.
	# Let's hope that nothing else has thing kind of name. 
	# So just collect those values and output. 
	# No need to store any information in the widget; no need
	# to access the form or the model, nothing at all.
	def value_from_datadict(self, data, files, name):
		return { key[5:] : data[key] for key in data if key.startswith('_aew_') }