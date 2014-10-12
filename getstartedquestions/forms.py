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
FUNDING_KNOWLEDGE_CHOICES = (('no_savings', 'Umm...I plead the fifth'), ('100_saved_whenever', "I add to my savings account whenever I can"), ('20percent', 'Roughly 10-20% of my yearly salary'), ('lotech_unknown_amount', 'I keep all of my savings in a jar'))
INCOME_CHOICES=(('0-31k', 'less than $32,000'), ('32-60k', 'between $32,000 and $60,000'), ('61-100k', 'between $60,000 and $100,000'), ('101-200k', 'between $100,000 and $200,000'), ('201k-infinity', 'greater than $200,000'))
FUNDING_PREFERENCE_CHOICES=(('accountant', 'No, but I have an accountant'), ('investment_app', 'I use an online investment app instead!'), ('no_advice', "I'll probably get one when I have more money"), ('wealth_manager', 'You mean my wealth manager, right?'))
INDUSTRY_PREFERENCE_CHOICES = (('finance_noob', "I'm a total financial noob"), ('stocks_bonds', "I know what stocks and bonds are. That's pretty much it"), ("mutual_index_funds", "I've got a portfolio of index funds with and a good asset allocation."), ('pro_status', 'Mutual funds are for the lemmings. I know where and when to invest my own money'))
SITE_REC_CHOICES = (('personal_referral', 'In person referral'), ('inapp_invite', 'Email invite fron a friend'), ('facebook', 'A post on my Facebook feed/timeline'), ('twitter', 'Saw a Magnate related tweet'), ('google', 'Searching on Google'), ('other', 'Other'))

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


