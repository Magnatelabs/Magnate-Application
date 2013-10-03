from django import forms
from getstartedquestions.models import QuestionList
from django.utils.safestring import mark_safe


# django knows to look for each input field, 
# as long the form subclass defines the fields
# in the same order as the model.


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class QuestionListForm(forms.Form):

    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    waitinglistemail = forms.EmailField()
    sex = forms.CharField(max_length=200)
    dob = forms.DateField(input_formats=['%m/%d/%Y',], required=False, widget=forms.DateInput(format = '%m/%d/%Y') )

#    funding_knowledge = forms.CharField(max_length=200, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer, choices=(('yes','YES'),('no','NO'))))
# Above is an attempt to horizontally place radials (didn't work)

    funding_knowledge = forms.CharField(max_length=200) 
    income = forms.IntegerField()
#    income = forms.CharField(max_length=200) !Need to make this a charfield during production!!
    funding_preference = forms.CharField(max_length=200)
    industry_preference = forms.CharField(max_length=200)
    site_rec = forms.CharField(max_length=200)


    def __init__(self, *args, **kwargs):
        super(QuestionListForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['id'] = 'super_first'


