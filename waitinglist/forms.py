from django import forms

from .models import Cohort, SurveyAnswer, SurveyQuestion, WaitingListEntry
from .signals import answered_survey
from forum.models.user import User

class WaitingListEntryForm(forms.ModelForm):
    
    class Meta:
        model = WaitingListEntry
    
    def clean_email(self):
        value = self.cleaned_data["email"]

        try: 
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(
                "Unfortunately, the email address %s is already registered." % (value)
            )
        try:
            entry = WaitingListEntry.objects.get(email=value)
        except WaitingListEntry.DoesNotExist:
            return value
        else:
            raise forms.ValidationError(
                "Unfortunately, the email address %s is already registered." % (value)
            )
    
    def __init__(self, *args, **kwargs):
        super(WaitingListEntryForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "your@email.com"
        self.fields["email"].label = ""
        self.fields['email'].widget.attrs['id'] = 'super_email'


class CohortCreate(forms.ModelForm):
    
    class Meta:
        model = Cohort
        exclude = ["created"]


class SurveyForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.survey = kwargs.pop("survey")
        super(SurveyForm, self).__init__(*args, **kwargs)
        for question in self.survey.questions.all():
            self.fields[question.name] = question.form_field()
    
    def save(self, instance):
        for question in self.survey.questions.all():
            answer = SurveyAnswer.objects.create(instance=instance, question=question)
            value = self.cleaned_data[question.name]
            if question.kind == SurveyQuestion.RADIO_CHOICES:
                answer.value = value.label
            elif question.kind == SurveyQuestion.CHECKBOX_FIELD:
                answer.value = ", ".join([x.label for x in value])
            elif question.kind == SurveyQuestion.BOOLEAN_FIELD:
                answer.value_boolean = value
            else:
                answer.value = value
            answer.save()
        answered_survey.send(sender=self, instance=instance)
