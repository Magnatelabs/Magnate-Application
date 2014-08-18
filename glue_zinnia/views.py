import zinnia
from .mixins import HiddenEntryProtectionMixin, AddRelatedQuestionsMixin

class HiddenEntryDetail(HiddenEntryProtectionMixin, AddRelatedQuestionsMixin, zinnia.views.entries.EntryDateDetail):
    pass
