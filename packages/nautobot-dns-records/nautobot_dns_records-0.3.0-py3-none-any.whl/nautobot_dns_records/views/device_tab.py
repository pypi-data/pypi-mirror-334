"""Add a tab to the device object view."""

from nautobot.core.views import generic
from nautobot.dcim.models import Device

from nautobot_dns_records.models import (
    AddressRecord,
    PtrRecord,
    TxtRecord,
    CNameRecord,
    LocRecord,
    SshfpRecord,
    SrvRecord,
)
from nautobot_dns_records.tables import (
    AddressRecordTable,
    PtrRecordTable,
    TxtRecordTable,
    CNameRecordTable,
    LocRecordTable,
    SshfpRecordTable,
    SrvRecordTable,
)


class DeviceRecordsTab(generic.ObjectView):
    """Display all dns records for a device."""

    queryset = Device.objects.all()
    template_name = "nautobot_dns_records/tab_device_records.html"

    def get_extra_context(self, request, instance):  # pylint: disable-msg=too-many-locals
        """Returns all dns records related to a device."""
        extra_context = {}

        addressrecords = AddressRecord.objects.filter(address__interfaces__device_id=instance.id).all()
        if addressrecords.count() > 0:
            addressrecords_table = AddressRecordTable(data=addressrecords, user=request.user, orderable=False)
            extra_context["addressrecords_table"] = addressrecords_table
        ptrrecords = PtrRecord.objects.filter(address__interfaces__device_id=instance.id).all()
        if ptrrecords.count() > 0:
            ptrrecords_table = PtrRecordTable(data=ptrrecords, user=request.user, orderable=False)
            extra_context["ptrrecords_table"] = ptrrecords_table
        txtrecords = TxtRecord.objects.filter(device=instance).all()
        if txtrecords.count() > 0:
            txtrecords_table = TxtRecordTable(data=txtrecords, user=request.user, orderable=False)
            extra_context["txtrecords_table"] = txtrecords_table
        cnamerecords = CNameRecord.objects.filter(device=instance).all()
        if cnamerecords.count() > 0:
            cnamerecords_table = CNameRecordTable(data=cnamerecords, user=request.user, orderable=False)
            extra_context["cnamerecords_table"] = cnamerecords_table
        locrecords = LocRecord.objects.filter(device=instance).all()
        if locrecords.count() > 0:
            locrecords_table = LocRecordTable(data=locrecords, user=request.user, orderable=False)
            extra_context["locrecords_table"] = locrecords_table
        sshfprecords = SshfpRecord.objects.filter(device=instance).all()
        if sshfprecords.count() > 0:
            sshfprecords_table = SshfpRecordTable(data=sshfprecords, user=request.user, orderable=False)
            extra_context["sshfprecords_table"] = sshfprecords_table
        srvrecords = SrvRecord.objects.filter(device=instance).all()
        if srvrecords.count() > 0:
            srvprecords_table = SrvRecordTable(data=srvrecords, user=request.user, orderable=False)
            extra_context["srvrecords_table"] = srvprecords_table

        if len(extra_context.items()) == 0:
            extra_context["no_records"] = True

        return {
            **extra_context,
            **super().get_extra_context(request, instance),
        }
