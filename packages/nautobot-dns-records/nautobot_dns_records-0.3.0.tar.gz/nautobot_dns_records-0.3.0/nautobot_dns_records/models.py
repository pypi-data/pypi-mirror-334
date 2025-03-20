# pylint: disable=too-many-ancestors
"""Model definition for nautobot_dns_records."""

import codecs

import nautobot.dcim.models
import nautobot.ipam.models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint

# from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from nautobot.core.models.generics import PrimaryModel
from nautobot.extras.models import StatusField
from nautobot.extras.utils import extras_features

from nautobot_dns_records.choices import LATITUDE_DIRECTIONS, LONGITUDE_DIRECTIONS, SSHFP_HASH_TYPE, SSHFP_ALGORITHMS
from nautobot_dns_records.validators import validate_dns_name


class Record(models.Model):
    """Abstract class that represents a base dns model.

    Attributes:
        label (CharField): Name of the dns node.
        ttl (IntegerField): TTL of the dns record. The minimal value is 1 and the maximum value is 604800
    """

    label = models.CharField(
        max_length=255,
        validators=[validate_dns_name],
        verbose_name=_("DNS Label"),
        help_text=_(
            "Label for the DNS entry, maximum length for individual segments is 63 characters, total length must not exceed 255 characters."
        ),
    )
    ttl = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(604800)],
        verbose_name=_("TTL"),
        help_text=_("Time to live for the dns entry in seconds, valid values are in the range 1 - 604800."),
        default=3600,
    )
    device = models.ForeignKey(
        nautobot.dcim.models.Device, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Device")
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Override the default django save method.

        Encodes the label field with the IDNA2003 rules
        """
        self.label = codecs.encode(self.label, encoding="idna").decode()
        super().save()

    def __str__(self):
        """Return the label field."""
        return self.label


@extras_features(
    "custom_fields",
    "graphql",
    "statuses",
)
class AddressRecord(PrimaryModel, Record):
    """Class that represents A and AAAA record.

    Attributes:
        address (nautobot.ipam.models.IPAddress)
    """

    address = models.ForeignKey(
        nautobot.ipam.models.IPAddress,
        on_delete=models.CASCADE,
        verbose_name=_("IP Address"),
        help_text=_("Related IP Address for the record."),
    )

    status = StatusField(on_delete=models.PROTECT, related_name="%(app_label)s_%(class)s_related")

    class Meta:
        constraints = [UniqueConstraint(fields=["label", "address"], name="arec_unique_label_address_combination")]


@extras_features(
    "custom_fields",
    "graphql",
    "statuses",
)
class CNameRecord(PrimaryModel, Record):
    """Class that represents a CNAME record.

    Attributes:
        target (CharField)
    """

    target = models.CharField(
        max_length=255,
        validators=[validate_dns_name],
        verbose_name=_("DNS Alias Target"),
        help_text=_("The target of the CNAME Record"),
    )

    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",
    )

    def save(self, *args, **kwargs):
        """Override the default django save method.

        Encodes the target field with the IDNA2003 rules
        """
        self.target = codecs.encode(self.target, encoding="idna").decode()
        super().save()

    class Meta:
        constraints = [UniqueConstraint(fields=["label"], name="unique_label")]


@extras_features(
    "custom_fields",
    "graphql",
    "statuses",
)
class TxtRecord(PrimaryModel, Record):
    """Class that represents a TXT record.

    Attributes:
        value (CharField)
    """

    value = models.CharField(max_length=255, verbose_name=_("Value"), help_text=_("The value of the TXT Record"))
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",
    )

    class Meta:
        constraints = [UniqueConstraint(fields=["label", "value"], name="txt_unique_label_value_combination")]


@extras_features(
    "custom_fields",
    "graphql",
    "statuses",
)
class LocRecord(PrimaryModel, Record):
    """Class that represents a LOC record.

    Attributes
        degLat (IntegerField): degrees latitude
        degLong (IntegerField): degrees longitude
        minLat (IntegerField): minutes latitude
        minLong (IntegerField): minutes longitude
        secLat (DecimalField): seconds latitude
        secLong (DecimalField): seconds longitude
        altitude (DecimalField): altitude
        precision (DecimalField): precision
        dirLat (CharField): direction for degrees latitude
        dirLong (CharField): direction for degrees longitude
    """

    degLat = models.IntegerField(
        verbose_name=_("degrees latitude"),
        help_text=_("The degree of latitude"),
        validators=[MinValueValidator(0), MaxValueValidator(90)],
    )
    degLong = models.IntegerField(
        verbose_name=_("degrees longitude"),
        help_text=_("The degree of longitude"),
        validators=[MinValueValidator(0), MaxValueValidator(180)],
    )
    minLat = models.IntegerField(
        verbose_name=_("minutes latitude"),
        help_text=_("The minutes of latitude"),
        validators=[MinValueValidator(0), MaxValueValidator(59)],
    )
    minLong = models.IntegerField(
        verbose_name=_("minutes longitude"),
        help_text=_("The minutes of longitude"),
        validators=[MinValueValidator(0), MaxValueValidator(59)],
    )
    secLat = models.DecimalField(
        verbose_name=_("seconds latitude"),
        help_text=_("The seconds of latitude"),
        validators=[MinValueValidator(0), MaxValueValidator(59.999)],
        decimal_places=3,
        max_digits=5,
    )
    secLong = models.DecimalField(
        verbose_name=_("seconds longitude"),
        help_text=_("The seconds of longitude"),
        validators=[MinValueValidator(0), MaxValueValidator(59.999)],
        decimal_places=3,
        max_digits=5,
    )
    altitude = models.DecimalField(
        verbose_name=_("altitude"),
        help_text=_("altitude of the point"),
        validators=[MinValueValidator(-100000), MaxValueValidator(42849672.95)],
        decimal_places=2,
        max_digits=10,
    )
    dirLat = models.CharField(
        verbose_name=_("latitude direction"),
        help_text=_("The alignment of the latitude"),
        choices=LATITUDE_DIRECTIONS,
        default="N",
        max_length=1,
    )
    dirLong = models.CharField(
        verbose_name=_("longitude direction"),
        help_text=_("The alignment of the longitude"),
        choices=LONGITUDE_DIRECTIONS,
        default="E",
        max_length=1,
    )
    precision = models.DecimalField(
        verbose_name=_("precision"),
        help_text=_("precision of the coordinate"),
        validators=[MinValueValidator(0), MaxValueValidator(90000000.00)],
        decimal_places=2,
        max_digits=10,
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",
    )

    class Meta:
        constraints = [UniqueConstraint(fields=["label"], name="loc_unique_label")]


@extras_features("custom_fields", "graphql", "statuses")
class PtrRecord(PrimaryModel, Record):
    """Class that represents a PTR record.

    Attributes:
        address (nautobot.ipam.models.IPAddress)
    """

    address = models.ForeignKey(
        nautobot.ipam.models.IPAddress,
        on_delete=models.CASCADE,
        verbose_name=_("IP Address"),
        help_text=_("Related IP Address for the record."),
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",
    )

    class Meta:
        constraints = [UniqueConstraint(fields=["label", "address"], name="ptr_unique_label_address")]


@extras_features(
    "custom_fields",
    "graphql",
    "statuses",
)
class SshfpRecord(PrimaryModel, Record):
    """Class that represents a SSHFP Record.

    see RFCs 4255,6594,7479,8709

    Attributes:
        algorithm (IntegerField)
        hashType (IntegerField)
        fingerprint (CharField)
    """

    algorithm = models.IntegerField(
        verbose_name=_("fingerprint algorithm"),
        help_text=_("Algorithm (0: reserved, 1: RSA, 2: DSA, 3: ECDSA, 4: Ed25519, 6:Ed448)"),
        choices=SSHFP_ALGORITHMS,
    )

    hashType = models.IntegerField(
        verbose_name=_("public key hash method"),
        help_text=_("Algorithm used to hash the public key (0: reserved, 1: SHA-1, 2: SHA-256)"),
        choices=SSHFP_HASH_TYPE,
    )

    fingerprint = models.CharField(
        verbose_name=_("fingerprint"),
        help_text=_("The ssh fingerprint"),
        max_length=255,
        validators=[RegexValidator("^[a-f0-9]*$", "Not a valid fingerprint in hex format")],
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",
    )

    class Meta:
        constraints = [UniqueConstraint(fields=["label", "fingerprint"], name="sshfp_unique_label_fingerprint")]


@extras_features("custom_fields", "graphql", "statuses")
class SrvRecord(PrimaryModel, Record):
    """Class that represents a SRV record.

    Attributes:
        priority (IntegerField)
        weight (IntegerField)
        port (IntegerField)
        target (CharField)
    """

    priority = models.IntegerField(
        verbose_name=_("Priority"),
        help_text=_("Priority of the record"),
        validators=[MinValueValidator(0), MaxValueValidator(65535)],
    )
    weight = models.IntegerField(
        verbose_name=_("Weight"),
        help_text=_("Relative weight for entries with the same priority"),
        validators=[MinValueValidator(0), MaxValueValidator(65535)],
        default=0,
    )
    port = models.IntegerField(
        verbose_name=_("Port"),
        help_text=_("TCP or UDP port of the service"),
        validators=[MinValueValidator(0), MaxValueValidator(65535)],
    )
    target = models.CharField(
        max_length=255,
        validators=[validate_dns_name],
        verbose_name=_("Target of the record"),
        help_text=_(
            "The domain name of the target host.  There MUST be one or more address records for this name, the name MUST NOT be an alias."
        ),
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",
    )

    class Meta:
        constraints = [UniqueConstraint(fields=["label", "target", "port"], name="srv_unique_label_target_port")]
