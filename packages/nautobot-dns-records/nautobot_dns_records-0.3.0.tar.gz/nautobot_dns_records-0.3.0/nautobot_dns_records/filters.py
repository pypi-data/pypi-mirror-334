"""Nautobot DNS-Records filters."""

from nautobot.apps.filters import BaseFilterSet

from nautobot_dns_records.models import (
    AddressRecord,
    CNameRecord,
    TxtRecord,
    LocRecord,
    PtrRecord,
    SshfpRecord,
    SrvRecord,
)


class AddressRecordFilterSet(BaseFilterSet):
    """FilterSet for filtering a set of Address records."""

    class Meta:
        model = AddressRecord
        fields = ["label", "address", "device"]


class CNameRecordFilterSet(BaseFilterSet):
    """FilterSet for filtering a set of CName records."""

    class Meta:
        model = CNameRecord
        fields = ["label", "target"]


class TxtRecordFilterSet(BaseFilterSet):
    """FilterSet for filtering a set of Txt records."""

    class Meta:
        model = TxtRecord
        fields = [
            "label",
        ]


class LocRecordFilterSet(BaseFilterSet):
    """FilterSet for filtering a set of Location records."""

    class Meta:
        model = LocRecord
        fields = [
            "label",
        ]


class PtrRecordFilterSet(BaseFilterSet):
    """FilterSet for filtering a set of Ptr records."""

    class Meta:
        model = PtrRecord
        fields = ["label", "address"]


class SshfpRecordFilterSet(BaseFilterSet):
    """FilterSet for filtering a set of Sshfp records."""

    class Meta:
        model = SshfpRecord
        fields = ["label", "fingerprint"]


class SrvRecordFilterSet(BaseFilterSet):
    """FilterSet for filtering a set of Srv records."""

    class Meta:
        model = SrvRecord
        fields = [
            "label",
        ]
