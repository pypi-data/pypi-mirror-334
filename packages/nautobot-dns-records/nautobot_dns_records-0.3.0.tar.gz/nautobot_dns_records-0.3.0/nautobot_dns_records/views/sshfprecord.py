"""Views for the sshfp record model."""

from nautobot.core.views import generic

from nautobot_dns_records import models, forms
from nautobot_dns_records import tables
from nautobot_dns_records.filters import SshfpRecordFilterSet


class SshfpRecordsListView(generic.ObjectListView):
    """List all SSHFP Records."""

    queryset = models.SshfpRecord.objects.all()
    table = tables.SshfpRecordTable
    action_buttons = ("add",)
    filterset = SshfpRecordFilterSet
    filterset_form = forms.SshfpRecordFilterForm


class SshfpRecordView(generic.ObjectView):
    """Show a SSHFP Record."""

    queryset = models.SshfpRecord.objects.all()


class SshfpRecordEditView(generic.ObjectEditView):
    """Edit an SSHFP record."""

    queryset = models.SshfpRecord.objects.all()
    model_form = forms.SshfpRecordForm


class SshfpRecordDeleteView(generic.ObjectDeleteView):
    """Delete an SHFP record."""

    queryset = models.SshfpRecord.objects.all()
