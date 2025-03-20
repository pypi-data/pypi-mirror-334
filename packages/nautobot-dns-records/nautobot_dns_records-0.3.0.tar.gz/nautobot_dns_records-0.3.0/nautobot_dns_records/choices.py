"""Contains the choice values for nautobot dns records."""

from django.utils.translation import gettext_lazy as _

LATITUDE_DIRECTIONS = [("N", _("North")), ("S", _("South"))]

LONGITUDE_DIRECTIONS = [("E", _("East")), ("W", _("West"))]

SSHFP_ALGORITHMS = [
    (0, _("reserved")),
    (1, _("RSA")),
    (2, _("DSA")),
    (3, _("ECDSA")),
    (4, _("Ed25519")),
    (6, _("Ed488")),
]

SSHFP_HASH_TYPE = [(0, _("reserved")), (1, _("SHA-1")), (2, _("SHA-256"))]
