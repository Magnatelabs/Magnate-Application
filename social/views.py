from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from zinnia.models.entry import Entry

from .templatetags import social_tags
from django.http import HttpResponseBadRequest
from django.utils import simplejson
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

from .models import toggle_like_unlike, total_entry_likes, StarRating, can_rate
import status_awards

#Added for feedback_entry
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
import datetime 
from social.models import FeedbackModel
from social.forms import FeedbackModelForm

#imports to recognize django messages
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

#import to recognize class based view
from django.views.generic.edit import FormView



#TODO! FIXME! Think about thread safety if multiple users like the same post at the same time!

# User clicked the "Like" button after a post.
@require_POST
def ajax_like_entry(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    if not request.user.is_authenticated():
        return HttpResponse(status=401)

    vars={}

    user=request.user
    entry_id=request.POST.get('entry_id', None)
    entry=get_object_or_404(Entry, pk=entry_id)
    question="How would you rate your overall experience with Magnate?"

    count = toggle_like_unlike(entry, user)
    status_awards.award_badges("user_liked_entry", user)


    vars['liked'] = (count > 0)
    vars['total_likes'] = total_entry_likes(entry)
    vars['update_html']={social_tags.get_div_dom_id(entry_id) : social_tags.like_entry_button(int(entry_id), user)}
    return HttpResponse(simplejson.dumps(vars), mimetype='application/javascript')

@require_POST
def ajax_star_rating(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    if not request.user.is_authenticated():
        return HttpResponse(status=401)

    value = request.POST.get('value', None)
    if value is None:
        return HttpResponseBadRequest()
    value = int(value)

    vars={}
    user = request.user
    question="How would you rate your overall experience with Magnate?"

    if can_rate(user):
        # Save rating
        StarRating.objects.create(user=user, rating=value, question=question,)
        # print "User %s rated %d..." % (request.user, value)
        vars['message'] = "Thank you for your feedback!"
    else:
        vars['message'] = "You have already voted in the recent past."

    # Award badges
    status_awards.award_badges("user_rated_something", user)

    return HttpResponse(simplejson.dumps(vars), mimetype='application/javascript')
    
def user_pages(request):
    try:
        id=request.GET.get('user_id', None)
        user=get_object_or_404(get_user_model(), pk=id)
    except ValueError:
        return HttpResponse(status=404)
    return render(request, 'social/users.html', {'user': user})

#def platform_index(request):
#    return render(request, 'social/platform_main.html')


class feedback_entry(FormView):
#    import pdb #(test for checking each process)
#    pdb.set_trace()
     
    template_name = 'social/platform_main.html'
    form_class = FeedbackModelForm
    redirect_field_name = "next"
    messages = {
        "survey_added": {
            "level": messages.SUCCESS,
            "text": _(u"Thanks, your feedback was successfully submitted.")
        },
        "input_error": {
            "level": messages.ERROR,
            "text": _(u"Your information was not entered correctly. Please try again.")
        }
    }

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            entry = FeedbackModel()
            entry.feedback_paragraph = form.data['feedback_paragraph']
            entry.created = datetime.datetime.now()
            entry.save()
            
            messages.add_message(
                self.request,
                self.messages["survey_added"]["level"],
                self.messages["survey_added"]["text"]
            )
    
            return redirect('confirm_questions') # Redirect after POST
        else:
            messages.add_message(
                self.request,
                self.messages["input_error"]["level"],
                self.messages["input_error"]["text"]
            )
            print 'DEBUG: form is not valid!!!', form.errors



