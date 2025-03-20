# pylint: disable=nb-use-fields-all
"""Table Views for DNS Models."""

import django_tables2 as tables
from nautobot.extras.tables import StatusTableMixin
from nautobot.apps.tables import BaseTable, ToggleColumn, ButtonsColumn

from nautobot_dns_records import models


class AddressRecordTable(StatusTableMixin, BaseTable):
    """Table for all record based models."""

    pk = ToggleColumn()
    label = tables.Column(linkify=True)
    address = tables.Column(linkify=True)
    actions = ButtonsColumn(models.AddressRecord, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        model = models.AddressRecord
        fields = ("pk", "label", "address")


class TxtRecordTable(StatusTableMixin, BaseTable):
    """Table for all record based models."""

    pk = ToggleColumn()
    label = tables.Column(linkify=True)
    device = tables.Column(linkify=True)
    actions = ButtonsColumn(models.TxtRecord, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        model = models.TxtRecord
        fields = ("pk", "label", "device", "value")


class LocRecordTable(StatusTableMixin, BaseTable):
    """Table for all record based models."""

    pk = ToggleColumn()
    label = tables.Column(linkify=True)
    device = tables.Column(linkify=True)
    actions = ButtonsColumn(models.LocRecord, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        model = models.LocRecord
        fields = ("pk", "label", "device")


class CNameRecordTable(StatusTableMixin, BaseTable):
    """Table for all record based models."""

    pk = ToggleColumn()
    label = tables.Column(linkify=True)
    device = tables.Column(linkify=True)
    actions = ButtonsColumn(models.CNameRecord, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        model = models.CNameRecord
        fields = ("pk", "label", "device")


class PtrRecordTable(StatusTableMixin, BaseTable):
    """Table for all record based models."""

    pk = ToggleColumn()
    label = tables.Column(linkify=True)
    address = tables.Column(linkify=True)
    actions = ButtonsColumn(models.PtrRecord, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        model = models.PtrRecord
        fields = ("pk", "label", "address")


class SshfpRecordTable(StatusTableMixin, BaseTable):
    """Table for all record based models."""

    pk = ToggleColumn()
    label = tables.Column(linkify=True)
    device = tables.Column(linkify=True)
    actions = ButtonsColumn(models.SshfpRecord, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        model = models.SshfpRecord
        fields = ("pk", "label", "device")


class SrvRecordTable(StatusTableMixin, BaseTable):
    """Table for srv record models."""

    pk = ToggleColumn()
    label = tables.Column(linkify=True)
    device = tables.Column(linkify=True)
    priority = tables.Column()
    weight = tables.Column()
    port = tables.Column()
    target = tables.Column()
    actions = ButtonsColumn(models.SrvRecord, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        model = models.SrvRecord
        fields = ("pk", "label", "device", "priority", "weight", "port", "target")
