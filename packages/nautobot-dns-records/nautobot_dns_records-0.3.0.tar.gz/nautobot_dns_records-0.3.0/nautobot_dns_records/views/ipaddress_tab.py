"""Add a tab to the device object view."""

from nautobot.core.views import generic
from nautobot.ipam.models import IPAddress

from nautobot_dns_records.models import (
    AddressRecord,
    PtrRecord,
)
from nautobot_dns_records.tables import (
    AddressRecordTable,
    PtrRecordTable,
)


class IpAddressRecordsTab(generic.ObjectView):
    """Display all dns records for a device."""

    queryset = IPAddress.objects.all()
    template_name = "nautobot_dns_records/tab_ipaddress_records.html"

    def get_extra_context(self, request, instance):  # pylint: disable-msg=too-many-locals
        """Returns all dns records related to a device."""
        extra_context = {}

        addressrecords = AddressRecord.objects.filter(address_id=instance.id).all()
        if addressrecords.count() > 0:
            addressrecords_table = AddressRecordTable(data=addressrecords, user=request.user, orderable=False)
            extra_context["addressrecords_table"] = addressrecords_table
        ptrrecords = PtrRecord.objects.filter(address_id=instance.id).all()
        if ptrrecords.count() > 0:
            ptrrecords_table = PtrRecordTable(data=ptrrecords, user=request.user, orderable=False)
            extra_context["ptrrecords_table"] = ptrrecords_table

        if len(extra_context.items()) == 0:
            extra_context["no_records"] = True

        return {
            **extra_context,
            **super().get_extra_context(request, instance),
        }
