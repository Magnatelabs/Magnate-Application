import zinnia
from .mixins import HiddenEntryProtectionMixin

class HiddenEntryDetail(HiddenEntryProtectionMixin, zinnia.views.entries.EntryDateDetail):
    pass
