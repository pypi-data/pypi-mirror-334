"""Views for the ptr record model."""

from nautobot.core.views import generic

from nautobot_dns_records import models, forms
from nautobot_dns_records import tables
from nautobot_dns_records.filters import PtrRecordFilterSet


class PtrRecordsListView(generic.ObjectListView):
    """List all PTR Records."""

    queryset = models.PtrRecord.objects.all()
    table = tables.PtrRecordTable
    action_buttons = ("add",)
    filterset = PtrRecordFilterSet
    filterset_form = forms.PtrRecordFilterForm


class PtrRecordView(generic.ObjectView):
    """Show a PTR Record."""

    queryset = models.PtrRecord.objects.all()


class PtrRecordEditView(generic.ObjectEditView):
    """Edit an PTR record."""

    queryset = models.PtrRecord.objects.all()
    model_form = forms.PtrRecordForm


class PtrRecordDeleteView(generic.ObjectDeleteView):
    """Delete an PTR record."""

    queryset = models.PtrRecord.objects.all()
