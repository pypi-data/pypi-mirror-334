"""Views for the cname record model."""

from nautobot.core.views import generic

from nautobot_dns_records import models, forms
from nautobot_dns_records import tables
from nautobot_dns_records.filters import CNameRecordFilterSet


class CnameRecordsListView(generic.ObjectListView):
    """List all CName Records."""

    queryset = models.CNameRecord.objects.all()
    table = tables.CNameRecordTable
    action_buttons = ("add",)
    filterset = CNameRecordFilterSet
    filterset_form = forms.CNameRecordFilterForm


class CnameRecordView(generic.ObjectView):
    """Show a Address Record."""

    queryset = models.CNameRecord.objects.all()


class CnameRecordEditView(generic.ObjectEditView):
    """Edit an address record."""

    queryset = models.CNameRecord.objects.all()
    model_form = forms.CnameRecordForm


class CnameRecordDeleteView(generic.ObjectDeleteView):
    """Delete an address record."""

    queryset = models.CNameRecord.objects.all()
