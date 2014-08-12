from django import forms
from getstartedquestions.models import QuestionList
from django.utils.safestring import mark_safe


# django knows to look for each input field, 
# as long the form subclass defines the fields
# in the same order as the model.


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

SEX_CHOICES=(('F', 'Female',), ('M', 'Male',),)
FUNDING_KNOWLEDGE_CHOICES = (('noob', 'serious noob'), ('amateur', 'skeptical amateur'), ('expert', 'seasoned expert'), ('what?', 'wait, what?'))
INCOME_CHOICES=(('0-31k', 'less than $32,000'), ('32-60k', 'between $32,000 and $60,000'), ('61-100k', 'between $60,000 and $100,000'), ('101-200k', 'between $100,000 and $200,000'), ('201k-infinity', 'greater than $200,000'))
FUNDING_PREFERENCE_CHOICES=(('non-profits', 'to help non-profits'), ('rewards', 'for the rewards'), ('ideas', 'just to help out great ideas'), ('money', 'to save money, or to make extra money'))
INDUSTRY_PREFERENCE_CHOICES = (('film-tv', 'Film & TV'), ('music', 'Music'), ('technology', 'Technology'), ('games', 'Games'), ('social-causes', 'Social Causes'))
SITE_REC_CHOICES = (('other', 'Other'), ('friends', 'Friends'), ('facebook', 'Facebook'), ('twitter', 'Twitter'), ('pinterest', 'Pinterest'), ('blogs', 'Blogs'), ('google', 'Google'))

class QuestionListForm(forms.Form):

    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    waitinglistemail = forms.EmailField()
    sex = forms.ChoiceField(widget=forms.Select, choices=SEX_CHOICES) #forms.CharField(max_length=200, label='Gender')
    dob = forms.DateField(required=False, input_formats=['%m/%d/%Y'],
        widget=forms.DateInput(format = '%m/%d/%Y') )

#    funding_knowledge = forms.CharField(max_length=200, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer, choices=(('yes','YES'),('no','NO'))))
# Above is an attempt to horizontally place radials (didn't work)

    funding_knowledge = forms.ChoiceField(widget=forms.RadioSelect, choices=FUNDING_KNOWLEDGE_CHOICES)#CharField(max_length=200) 
#    income = forms.IntegerField()
    income = forms.ChoiceField(widget=forms.Select, choices=INCOME_CHOICES)#forms.CharField(max_length=200)
    funding_preference = forms.ChoiceField(widget=forms.Select, choices=FUNDING_PREFERENCE_CHOICES)#forms.CharField(max_length=200)
    industry_preference = forms.ChoiceField(widget=forms.Select, choices=INDUSTRY_PREFERENCE_CHOICES)#forms.CharField(max_length=200)
    site_rec = forms.ChoiceField(widget=forms.Select, choices=SITE_REC_CHOICES)#forms.CharField(max_length=200)


    def __init__(self, *args, **kwargs):
        super(QuestionListForm, self).__init__(*args, **kwargs)


