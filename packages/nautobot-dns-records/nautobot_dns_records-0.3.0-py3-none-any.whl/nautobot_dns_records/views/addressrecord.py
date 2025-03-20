"""Views for the address record model."""

from nautobot.core.views import generic

from nautobot_dns_records import models, tables, forms
from nautobot_dns_records.filters import AddressRecordFilterSet


class AddressRecordsListView(generic.ObjectListView):
    """List all Address Records."""

    queryset = models.AddressRecord.objects.all()
    table = tables.AddressRecordTable
    action_buttons = ("add",)
    filterset = AddressRecordFilterSet
    filterset_form = forms.AddressRecordFilterForm


class AddressRecordView(generic.ObjectView):
    """Show a Address Record."""

    queryset = models.AddressRecord.objects.all()


class AddressRecordEditView(generic.ObjectEditView):
    """Edit an address record."""

    queryset = models.AddressRecord.objects.all()
    model_form = forms.AddressRecordForm
    template_name = "nautobot_dns_records/addressrecord_edit.html"

    def post(self, request, *args, **kwargs):
        """Extend build in post method with a ptr record creation."""
        if request.POST.get("create_reverse") == "on":
            form = self.model_form(data=request.POST, files=request.FILES)
            if form.is_valid():
                ptr = models.PtrRecord(
                    label=form.cleaned_data["label"],
                    address=form.cleaned_data["address"],
                    ttl=form.cleaned_data["ttl"],
                    status=form.cleaned_data["status"],
                )
                if form.cleaned_data["device"]:
                    ptr.device = form.cleaned_data["device"]
                ptr.save()
        return super().post(request, *args, **kwargs)


class AddressRecordDeleteView(generic.ObjectDeleteView):
    """Delete an address record."""

    queryset = models.AddressRecord.objects.all()
