"""Views for nautobot_dns_records."""

from nautobot.core.views import generic

from nautobot_dns_records import models, forms
from nautobot_dns_records import tables
from nautobot_dns_records.filters import LocRecordFilterSet


class LocRecordsListView(generic.ObjectListView):
    """List all LOC Records."""

    queryset = models.LocRecord.objects.all()
    table = tables.LocRecordTable
    action_buttons = ("add",)
    filterset = LocRecordFilterSet
    filterset_form = forms.LocRecordFilterForm


class LocRecordView(generic.ObjectView):
    """Show a LOC Record."""

    queryset = models.LocRecord.objects.all()


class LocRecordEditView(generic.ObjectEditView):
    """Edit an LOC record."""

    queryset = models.LocRecord.objects.all()
    model_form = forms.LocRecordForm


class LocRecordDeleteView(generic.ObjectDeleteView):
    """Delete an LOC record."""

    queryset = models.LocRecord.objects.all()
