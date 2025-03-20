# pylint: disable=too-many-ancestors
"""API views for nautobot_dns_records."""
from nautobot.apps.api import NautobotModelViewSet

from nautobot_dns_records.models import (
    AddressRecord,
    CNameRecord,
    TxtRecord,
    LocRecord,
    PtrRecord,
    SshfpRecord,
    SrvRecord,
)
from nautobot_dns_records.api.serializers import (
    AddressRecordSerializer,
    CNameRecordSerializer,
    TxtRecordSerializer,
    LocRecordSerializer,
    PtrRecordSerializer,
    SshfpRecordSerializer,
    SrvRecordSerializer,
)


class AddressRecordViewSet(NautobotModelViewSet):
    """API viewset for interacting with AddressRecord objects."""

    queryset = AddressRecord.objects.all()
    serializer_class = AddressRecordSerializer


class CNameRecordViewSet(NautobotModelViewSet):
    """API viewset for interacting with CNameRecord objects."""

    queryset = CNameRecord.objects.all()
    serializer_class = CNameRecordSerializer


class TxtRecordViewSet(NautobotModelViewSet):
    """API viewset for interacting with TxtRecord objects."""

    queryset = TxtRecord.objects.all()
    serializer_class = TxtRecordSerializer


class LocRecordViewSet(NautobotModelViewSet):
    """API viewset for interacting with LocRecord objects."""

    queryset = LocRecord.objects.all()
    serializer_class = LocRecordSerializer


class PtrRecordViewSet(NautobotModelViewSet):
    """API viewset for interacting with PtrRecord objects."""

    queryset = PtrRecord.objects.all()
    serializer_class = PtrRecordSerializer


class SshfpRecordViewSet(NautobotModelViewSet):
    """API viewset for interacting with SshfpRecord objects."""

    queryset = SshfpRecord.objects.all()
    serializer_class = SshfpRecordSerializer


class SrvRecordViewSet(NautobotModelViewSet):
    """API viewset for interacting with SrvRecord objects."""

    queryset = SrvRecord.objects.all()
    serializer_class = SrvRecordSerializer
