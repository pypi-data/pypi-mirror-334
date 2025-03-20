"""Views for the loc record model."""

from nautobot.core.views import generic

from nautobot_dns_records import models, forms
from nautobot_dns_records import tables
from nautobot_dns_records.filters import TxtRecordFilterSet


class TxtRecordsListView(generic.ObjectListView):
    """List all TXT Records."""

    queryset = models.TxtRecord.objects.all()
    table = tables.TxtRecordTable
    action_buttons = ("add",)
    filterset = TxtRecordFilterSet
    filterset_form = forms.TxtRecordForm


class TxtRecordView(generic.ObjectView):
    """Show a TXT Record."""

    queryset = models.TxtRecord.objects.all()


class TxtRecordEditView(generic.ObjectEditView):
    """Edit an TXT record."""

    queryset = models.TxtRecord.objects.all()
    model_form = forms.TxtRecordForm


class TxtRecordDeleteView(generic.ObjectDeleteView):
    """Delete an TXT record."""

    queryset = models.TxtRecord.objects.all()
