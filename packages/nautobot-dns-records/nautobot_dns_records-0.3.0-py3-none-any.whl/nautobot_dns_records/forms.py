"""Forms for the nautobot dns records plugin."""

import nautobot.dcim.models
import nautobot.ipam.models
from django import forms
from django.utils.translation import gettext_lazy as _
from nautobot.apps.forms import BootstrapMixin, DynamicModelChoiceField
from nautobot.extras.forms import RelationshipModelFormMixin, NautobotFilterForm, StatusModelFilterFormMixin

from nautobot_dns_records import models


class AddressRecordForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """Address Record create/edit form."""

    device = DynamicModelChoiceField(queryset=nautobot.dcim.models.Device.objects.all(), required=False)
    address = DynamicModelChoiceField(
        queryset=nautobot.ipam.models.IPAddress.objects.all(), query_params={"device_id": "$device"}
    )
    create_reverse = forms.BooleanField(label=_("Create reverse record"), required=False)

    class Meta:
        model = models.AddressRecord
        fields = ["label", "ttl", "device", "address", "status", "tags"]


class AddressRecordFilterForm(NautobotFilterForm, StatusModelFilterFormMixin):
    """Filters for the Address Record list view."""

    model = models.AddressRecord
    field_order = ["q", "label__ic", "device", "address", "status"]
    q = forms.CharField(required=False, label=_("Search"))
    label__ic = forms.CharField(required=False, label=_("Label"))
    device = DynamicModelChoiceField(
        queryset=nautobot.dcim.models.Device.objects.all(),
        required=False,
    )
    address = DynamicModelChoiceField(
        queryset=nautobot.ipam.models.IPAddress.objects.all(),
        required=False,
    )


class CnameRecordForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """CName Record create/edit form."""

    device = DynamicModelChoiceField(queryset=nautobot.dcim.models.Device.objects.all(), required=False)

    class Meta:
        model = models.CNameRecord
        fields = ["label", "ttl", "target", "device", "status", "tags"]


class CNameRecordFilterForm(NautobotFilterForm, StatusModelFilterFormMixin):
    """Filters for the CName Record list view."""

    model = models.CNameRecord
    field_order = ["q", "label__ic", "target", "device", "status"]
    q = forms.CharField(required=False, label=_("Search"))
    label__ic = forms.CharField(required=False, label=_("Label"))
    target = forms.CharField(required=False, label=_("Target"))
    device = DynamicModelChoiceField(
        queryset=nautobot.dcim.models.Device.objects.all(),
        required=False,
    )


class LocRecordForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """LOC Record create/edit form."""

    device = DynamicModelChoiceField(queryset=nautobot.dcim.models.Device.objects.all(), required=False)

    class Meta:
        model = models.LocRecord
        fields = [
            "label",
            "ttl",
            "degLat",
            "minLat",
            "secLat",
            "degLong",
            "minLong",
            "secLong",
            "precision",
            "altitude",
            "device",
            "status",
            "tags",
        ]


class LocRecordFilterForm(NautobotFilterForm, StatusModelFilterFormMixin):
    """Filters for the LOC Record list view."""

    model = models.LocRecord
    field_order = ["q", "label__ic", "device", "status"]
    q = forms.CharField(required=False, label=_("Search"))
    label__ic = forms.CharField(required=False, label=_("Label"))
    device = DynamicModelChoiceField(
        queryset=nautobot.dcim.models.Device.objects.all(),
        required=False,
    )


class PtrRecordForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """PTR Record create/edit form."""

    device = DynamicModelChoiceField(queryset=nautobot.dcim.models.Device.objects.all(), required=False)
    address = DynamicModelChoiceField(
        queryset=nautobot.ipam.models.IPAddress.objects.all(), query_params={"device_id": "$device"}
    )

    class Meta:
        model = models.PtrRecord
        fields = ["label", "ttl", "device", "address", "status", "tags"]


class PtrRecordFilterForm(NautobotFilterForm, StatusModelFilterFormMixin):
    """Filters for the PTR Record list view."""

    model = models.PtrRecord
    field_order = ["q", "label__ic", "device", "address", "status"]
    q = forms.CharField(required=False, label=_("Search"))
    label__ic = forms.CharField(required=False, label=_("Label"))
    device = DynamicModelChoiceField(
        queryset=nautobot.dcim.models.Device.objects.all(),
        required=False,
    )
    address = DynamicModelChoiceField(
        queryset=nautobot.ipam.models.IPAddress.objects.all(),
        required=False,
    )


class SshfpRecordForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """SSHFP Record create/edit form."""

    device = DynamicModelChoiceField(queryset=nautobot.dcim.models.Device.objects.all(), required=False)

    class Meta:
        model = models.SshfpRecord
        fields = ["label", "ttl", "algorithm", "hashType", "fingerprint", "device", "status", "tags"]


class SshfpRecordFilterForm(NautobotFilterForm, StatusModelFilterFormMixin):
    """Filters for the SSHFP Record."""

    model = models.SshfpRecord
    field_order = ["q", "label__ic", "device", "fingerprint", "status"]
    q = forms.CharField(required=False, label=_("Search"))
    label__ic = forms.CharField(required=False, label=_("Label"))
    device = DynamicModelChoiceField(
        queryset=nautobot.dcim.models.Device.objects.all(),
        required=False,
    )
    fingerprint = forms.CharField(required=False, label=_("Fingerprint"))


class TxtRecordForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """TXT Record create/edit form."""

    device = DynamicModelChoiceField(queryset=nautobot.dcim.models.Device.objects.all(), required=False)

    class Meta:
        model = models.TxtRecord
        fields = ["label", "ttl", "value", "device", "status", "tags"]


class TxtRecordFilterForm(NautobotFilterForm, StatusModelFilterFormMixin):
    """Filters for the TXT Record list view."""

    model = models.TxtRecord
    field_order = ["q", "label__ic", "device", "value", "status"]
    q = forms.CharField(required=False, label=_("Search"))
    label__ic = forms.CharField(required=False, label=_("Label"))
    device = DynamicModelChoiceField(
        queryset=nautobot.dcim.models.Device.objects.all(),
        required=False,
    )
    value = forms.CharField(required=False, label=_("Value"))


class SrvRecordForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """SRV Record create/edit form."""

    device = DynamicModelChoiceField(queryset=nautobot.dcim.models.Device.objects.all(), required=False)

    class Meta:
        model = models.SrvRecord
        fields = ["label", "ttl", "device", "priority", "weight", "port", "target", "status", "tags"]


class SrvRecordFilterForm(NautobotFilterForm, StatusModelFilterFormMixin):
    """Filters for the SRV Record list view."""

    model = models.SrvRecord
    field_order = ["q", "label__ic", "device", "port", "target", "status"]
    q = forms.CharField(required=False, label=_("Search"))
    label__ic = forms.CharField(required=False, label=_("Label"))
    device = DynamicModelChoiceField(
        queryset=nautobot.dcim.models.Device.objects.all(),
        required=False,
    )
    port = forms.IntegerField(required=False, label=_("Port"))
    target = forms.CharField(required=False, label=_("Target"))
