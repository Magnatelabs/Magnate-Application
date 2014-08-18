from django.http import Http404
from zinnia.views.mixins.entry_protection import EntryProtectionMixin
from zinnia.managers import HIDDEN


class HiddenEntryProtectionMixin(EntryProtectionMixin):

    def get(self, request, *args, **kwargs):
        # Have to get response first to populate self.object
        response = super(EntryProtectionMixin, self).get(
            request, *args, **kwargs)
        if self.object.status==HIDDEN:
            if (not request.user.is_authenticated()) or (not self.object.authorized_users.filter(username=request.user).exists()):
                raise Http404   # User is not authorized to view this hidden entry
        return response


    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

class AddRelatedQuestionsMixin(object):
    def get_context_data(self, **kwargs):
        context = super(AddRelatedQuestionsMixin, self).get_context_data(**kwargs)

        entry_pk = context['object'].pk # Zinnia entry
        from forum.models.question import Question
        initial=Question.objects.all()
        questions = initial.filter_state(deleted=False)
        questions = questions.filter(about_entries__entry__pk=entry_pk)
        context['related_questions']=questions.order_by('-added_at')
        return context