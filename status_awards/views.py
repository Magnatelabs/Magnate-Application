from django.db import models
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required(login_url='/account/login')
def status_index(request):
#    if not request.user.is_authenticated():
#        return redirect('/donations/user/?next=%s' % request.path)

    return render(request, 'status_awards/status_home.html')

@login_required(login_url='/account/login')
def award_detail(request):
#    if not request.user.is_authenticated():
#        return redirect('/donations/user/?next=%s' % request.path)
#    import pdb; pdb.set_trace()
    try:
        award_pk = int(request.GET['award'])
        badge = request.user.badges_earned.get(pk=award_pk)
    except:
        return status_index(request)
#    import pdb; pdb.set_trace()
#    request.user.badges_earned.get(r

    return render(request, 'status_awards/status_award_detail.html', {'badge': badge})

# This can be moved somewhere, merged with magnate_user_info in dashboard/contexts.py, etc.
# For now just putting it here for the sake of simplicity.
def user_stats(request):
	user=request.user
	from forum.models.question import Question
	from social.models import FeedbackModel
	questions_asked = Question.objects.filter(author=user).count()
	feedback_given = FeedbackModel.objects.filter(user=user).count()
	knowledge_ranking = user.reputation
	news_spread = 0
	startups_sourced = 0
	return {'questions_asked': questions_asked,
		    'feedback_given': feedback_given,
		    'knowledge_ranking': knowledge_ranking,
		    'news_spread': news_spread,
		    'startups_sourced': startups_sourced}

@login_required(login_url='/account/login')
def newstatus_index(request):
#    if not request.user.is_authenticated():                                                             #        return redirect('/donations/user/?next=%s' % request.path)                                       
    return render(request, 'status_awards/newstatus_home.html', {'stats': user_stats(request) })
