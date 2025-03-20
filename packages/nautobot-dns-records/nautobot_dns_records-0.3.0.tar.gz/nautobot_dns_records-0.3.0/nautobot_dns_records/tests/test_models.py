"""Tests for the nautobot_dns_records models."""

import django.db.models.fields
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from nautobot.apps.testing import TestCase
from nautobot.dcim.models import Device
from nautobot.extras.models import Status
from nautobot.ipam.models import IPAddress

from nautobot_dns_records.models import (
    Record,
    AddressRecord,
    CNameRecord,
    TxtRecord,
    LocRecord,
    PtrRecord,
    SshfpRecord,
    SrvRecord,
)
from nautobot_dns_records.tests.helpers import (
    random_valid_dns_ttl,
    random_valid_dns_name,
)
from nautobot_dns_records.tests.mixins import AbstractModelMixinTestCase


class RecordTestCase(AbstractModelMixinTestCase):
    """Test the Record model."""

    mixin = Record

    def setUp(self):
        self.device = Device(name="test-device")

    def test_record_is_abstract(self):
        with self.assertRaisesMessage(TypeError, "Abstract models cannot be instantiated."):
            Record(label=random_valid_dns_name(), ttl=random_valid_dns_ttl())

    def test_record_has_label(self):
        self.assertIsInstance(Record._meta.get_field("label"), django.db.models.fields.CharField)

    def test_record_single_label_to_long(self):
        label = "thisisaveryveryveryverylongdnslabelwhichisinvalid12345678942424"
        with self.assertRaisesMessage(ValidationError, f"The label {label} is longer than allowed (> 63)"):
            record = self.model(label=f"{label}.test", ttl=1)
            record.clean_fields()

    def test_record_to_long(self):
        label = "thisisaveryveryveryverylongdnslabelwhichisinvalid123456789424.thisisaveryveryveryverylongdnslabelwhichisinvalid123456789424.thisisaveryveryveryverylongdnslabelwhichisinvalid123456789424.thisisaveryveryveryverylongdnslabelwhichisinvalid123456789424.test1234"
        with self.assertRaisesMessage(ValidationError, "Ensure this value has at most 255 characters (it has 256)."):
            record = self.model(label=label, ttl=1)
            record.clean_fields()

    def test_record_has_ttl(self):
        self.assertIsInstance(Record._meta.get_field("ttl"), django.db.models.fields.IntegerField)

    def test_record_ttl_validation(self):
        with self.assertRaisesMessage(ValidationError, "Ensure this value is greater than or equal to 1."):
            record = self.model(label=random_valid_dns_name(), ttl=0)
            record.clean_fields()
        with self.assertRaisesMessage(ValidationError, "Ensure this value is less than or equal to 604800."):
            record.ttl = 604801
            record.clean_fields()
        record.ttl = 10
        record.clean_fields()

    def test_record_idna_encoding(self):
        record = self.model(label="💩.test", ttl=1)
        record.save()
        self.assertEqual(record.label, "xn--ls8h.test")

    def test_str(self):
        record = self.model(label=random_valid_dns_name(), ttl=1)
        record.save()
        self.assertEqual(str(record), record.label)

    def test_device_assignment(self):
        record = self.model(label=random_valid_dns_name(), ttl=1, device=self.device)
        self.assertEqual(record.device, self.device)


class AddressRecordTestCase(TestCase):
    """Test the AddressRecord Model"""

    def setUp(self):  # pylint: disable=invalid-name
        self.testIPv4 = IPAddress.objects.filter(ip_version="4").first()
        self.testIPv6 = IPAddress.objects.filter(ip_version="6").first()
        self.status = Status.objects.get(name="Active")

    def test_record_creation_ipv4(self):
        record_v4 = AddressRecord(
            label=random_valid_dns_name(), ttl=random_valid_dns_ttl(), address=self.testIPv4, status=self.status
        )
        record_v4.save()
        self.assertEqual(record_v4.address, self.testIPv4)

    def test_record_creation_ipv6(self):
        record_v6 = AddressRecord(
            label=random_valid_dns_name(), ttl=random_valid_dns_ttl(), address=self.testIPv6, status=self.status
        )
        record_v6.save()
        self.assertEqual(record_v6.address, self.testIPv6)

    def test_uniqueness(self):
        label = random_valid_dns_name()
        with self.assertRaisesRegex(IntegrityError, "duplicate key value violates unique constraint .*"):
            AddressRecord(label=label, ttl=random_valid_dns_ttl(), address=self.testIPv4, status=self.status).save()
            AddressRecord(label=label, ttl=random_valid_dns_ttl(), address=self.testIPv4, status=self.status).save()


class CNameRecordTestCase(TestCase):
    """Test the CNameRecord Model"""

    def setUp(self):  # pylint: disable=invalid-name
        self.status = Status.objects.get(name="Active")

    def test_record_creation(self):
        target = random_valid_dns_name()
        record = CNameRecord(
            label=random_valid_dns_name(), ttl=random_valid_dns_ttl(), target=target, status=self.status
        )
        record.save()
        self.assertEqual(record.target, target)

    def test_record_target_encoding(self):
        record = CNameRecord(
            label=random_valid_dns_name(), ttl=random_valid_dns_ttl(), target="💩.test", status=self.status
        )
        record.save()
        self.assertEqual(record.target, "xn--ls8h.test")

    def test_record_uniqueness(self):
        target = random_valid_dns_name()
        label = random_valid_dns_name()
        with self.assertRaisesRegex(IntegrityError, "duplicate key value violates unique constraint .*"):
            record1 = CNameRecord(label=label, ttl=random_valid_dns_ttl(), target=target, status=self.status)
            record1.save()
            record2 = CNameRecord(label=label, ttl=random_valid_dns_ttl(), target=target, status=self.status)
            record2.save()


class TxtRecordTestCase(TestCase):
    """Test the TxtRecord Model"""

    def setUp(self):  # pylint: disable=invalid-name
        self.status = Status.objects.get(name="Active")

    def test_txt_record_creation(self):
        value = "This is a test!"
        record = TxtRecord(label=random_valid_dns_name(), ttl=random_valid_dns_ttl(), value=value, status=self.status)
        record.save()
        self.assertEqual(record.value, value)

    def test_txt_record_uniqueness(self):
        value = "This is a test!"
        label = random_valid_dns_name()
        with self.assertRaisesRegex(IntegrityError, "duplicate key value violates unique constraint .*"):
            TxtRecord(label=label, ttl=random_valid_dns_ttl(), value=value, status=self.status).save()
            TxtRecord(label=label, ttl=random_valid_dns_ttl(), value=value, status=self.status).save()


class LocRecordTestCase(TestCase):
    """Test the LocRecord Model"""

    def setUp(self):  # pylint: disable=invalid-name
        self.status = Status.objects.get(name="Active")
        self.status.content_types.add(ContentType.objects.get_for_model(LocRecord))

    def test_loc_record_creation(self):
        record = LocRecord(
            label="big.ben.hm",
            ttl=random_valid_dns_ttl(),
            degLong=73,
            minLong=30,
            secLong=43,
            dirLong="E",
            degLat=53,
            minLat=6,
            secLat=1,
            dirLat="S",
            altitude=517,
            precision=0,
            status=self.status,
        )
        record.save()
        self.assertEqual(record.label, "big.ben.hm")

    def test_loc_record_field_validation_degLat(self):  # pylint: disable=C0103
        record = LocRecord(
            label="big.ben.hm",
            ttl=random_valid_dns_ttl(),
            degLong=73,
            minLong=30,
            secLong=43,
            dirLong="E",
            degLat=53,
            minLat=6,
            secLat=1,
            dirLat="S",
            altitude=517,
            precision=0,
            status=self.status,
        )
        record.save()
        with self.assertRaisesMessage(
            ValidationError, "{'degLat': ['Ensure this value is greater than or equal to 0.']}"
        ):
            record.degLat = -1
            record.clean_fields()
        with self.assertRaisesMessage(
            ValidationError, "{'degLat': ['Ensure this value is less than or equal to 90.']}"
        ):
            record.degLat = 91
            record.clean_fields()

    def test_loc_record_field_validation_degLong(self):  # pylint: disable=C0103
        record = LocRecord(
            label="big.ben.hm",
            ttl=random_valid_dns_ttl(),
            degLong=73,
            minLong=30,
            secLong=43,
            dirLong="E",
            degLat=53,
            minLat=6,
            secLat=1,
            dirLat="S",
            altitude=517,
            precision=0,
            status=self.status,
        )
        record.save()
        with self.assertRaisesMessage(
            ValidationError, "{'degLong': ['Ensure this value is greater than or equal to 0.']}"
        ):
            record.degLong = -1
            record.clean_fields()
        with self.assertRaisesMessage(
            ValidationError, "{'degLong': ['Ensure this value is less than or equal to 180.']}"
        ):
            record.degLong = 181
            record.clean_fields()

    def test_loc_record_field_validation_minLat(self):  # pylint: disable=C0103
        record = LocRecord(
            label="big.ben.hm",
            ttl=random_valid_dns_ttl(),
            degLong=73,
            minLong=30,
            secLong=43,
            dirLong="E",
            degLat=53,
            minLat=6,
            secLat=1,
            dirLat="S",
            altitude=517,
            precision=0,
            status=self.status,
        )
        record.save()
        with self.assertRaisesMessage(
            ValidationError, "{'minLat': ['Ensure this value is greater than or equal to 0.']}"
        ):
            record.minLat = -1
            record.clean_fields()
        with self.assertRaisesMessage(
            ValidationError, "{'minLat': ['Ensure this value is less than or equal to 59.']}"
        ):
            record.minLat = 60
            record.clean_fields()

    def test_loc_record_field_validation_minLong(self):  # pylint: disable=C0103
        record = LocRecord(
            label="big.ben.hm",
            ttl=random_valid_dns_ttl(),
            degLong=73,
            minLong=30,
            secLong=43,
            dirLong="E",
            degLat=53,
            minLat=6,
            secLat=1,
            dirLat="S",
            altitude=517,
            precision=0,
            status=self.status,
        )
        record.save()
        with self.assertRaisesMessage(
            ValidationError, "{'minLong': ['Ensure this value is greater than or equal to 0.']}"
        ):
            record.minLong = -1
            record.clean_fields()
        with self.assertRaisesMessage(
            ValidationError, "{'minLong': ['Ensure this value is less than or equal to 59.']}"
        ):
            record.minLong = 60
            record.clean_fields()

    def test_loc_record_field_validation_secLat(self):  # pylint: disable=C0103
        record = LocRecord(
            label="big.ben.hm",
            ttl=random_valid_dns_ttl(),
            degLong=73,
            minLong=30,
            secLong=43,
            dirLong="E",
            degLat=53,
            minLat=6,
            secLat=1,
            dirLat="S",
            altitude=517,
            precision=0,
            status=self.status,
        )
        record.save()
        with self.assertRaisesMessage(
            ValidationError, "{'secLat': ['Ensure this value is greater than or equal to 0.']}"
        ):
            record.secLat = -1
            record.clean_fields()
        with self.assertRaisesMessage(
            ValidationError, "{'secLat': ['Ensure this value is less than or equal to 59.999.']}"
        ):
            record.secLat = 60
            record.clean_fields()

    def test_loc_record_field_validation_secLong(self):  # pylint: disable=C0103
        record = LocRecord(
            label="big.ben.hm",
            ttl=random_valid_dns_ttl(),
            degLong=73,
            minLong=30,
            secLong=43,
            dirLong="E",
            degLat=53,
            minLat=6,
            secLat=1,
            dirLat="S",
            altitude=517,
            precision=0,
            status=self.status,
        )
        record.save()
        with self.assertRaisesMessage(
            ValidationError, "{'secLong': ['Ensure this value is greater than or equal to 0.']}"
        ):
            record.secLong = -1
            record.clean_fields()
        with self.assertRaisesMessage(
            ValidationError, "{'secLong': ['Ensure this value is less than or equal to 59.999.']}"
        ):
            record.secLong = 60
            record.clean_fields()

    def test_loc_record_field_validation_altitude(self):
        record = LocRecord(
            label="big.ben.hm",
            ttl=random_valid_dns_ttl(),
            degLong=73,
            minLong=30,
            secLong=43,
            dirLong="E",
            degLat=53,
            minLat=6,
            secLat=1,
            dirLat="S",
            altitude=517,
            precision=0,
            status=self.status,
        )
        record.save()
        with self.assertRaisesMessage(
            ValidationError, "{'altitude': ['Ensure this value is greater than or equal to -100000.']}"
        ):
            record.altitude = -100001
            record.clean_fields()
        with self.assertRaisesMessage(
            ValidationError, "{'altitude': ['Ensure this value is less than or equal to 42849672.95.']}"
        ):
            record.altitude = 42849672.96
            record.clean_fields()

    def test_loc_record_field_validation_precision(self):
        record = LocRecord(
            label="big.ben.hm",
            ttl=random_valid_dns_ttl(),
            degLong=73,
            minLong=30,
            secLong=43,
            dirLong="E",
            degLat=53,
            minLat=6,
            secLat=1,
            dirLat="S",
            altitude=517,
            precision=0,
            status=self.status,
        )
        record.save()
        with self.assertRaisesMessage(
            ValidationError, "{'precision': ['Ensure this value is greater than or equal to 0.']}"
        ):
            record.precision = -1
            record.clean_fields()
        with self.assertRaisesMessage(
            ValidationError, "{'precision': ['Ensure this value is less than or equal to 90000000.0.']}"
        ):
            record.precision = 90000000.01
            record.clean_fields()


class PtrRecordTestCase(TestCase):
    """Test the PtrRecord Model."""

    def setUp(self):  # pylint: disable=invalid-name
        self.testIPv4 = IPAddress.objects.filter(ip_version="4").first()
        self.testIPv6 = IPAddress.objects.filter(ip_version="6").first()
        self.status = Status.objects.get(name="Active")

    def test_ptr_record_creation_ipv4(self):
        record = PtrRecord(
            label=random_valid_dns_name(), ttl=random_valid_dns_ttl(), address=self.testIPv4, status=self.status
        )
        record.save()
        self.assertEqual(record.address, self.testIPv4)

    def test_ptr_record_creation_ipv6(self):
        record = PtrRecord(
            label=random_valid_dns_name(), ttl=random_valid_dns_ttl(), address=self.testIPv6, status=self.status
        )
        record.save()
        self.assertEqual(record.address, self.testIPv6)

    def test_ptr_record_uniqueness(self):
        label = random_valid_dns_name()
        with self.assertRaisesRegex(IntegrityError, "duplicate key value violates unique constraint .*"):
            PtrRecord(label=label, ttl=random_valid_dns_ttl(), address=self.testIPv4, status=self.status).save()
            PtrRecord(label=label, ttl=random_valid_dns_ttl(), address=self.testIPv4, status=self.status).save()


class SshfpRecordTestCase(TestCase):
    """Test the SSHFP Record Model."""

    def setUp(self):  # pylint: disable=invalid-name
        self.status = Status.objects.get(name="Active")
        self.status.content_types.add(ContentType.objects.get_for_model(SshfpRecord))

    def test_sshfp_record_creation(self):
        record = SshfpRecord(
            label=random_valid_dns_name(),
            ttl=random_valid_dns_ttl(),
            algorithm=1,
            hashType=1,
            fingerprint="81bc1331bcd5b1c605a142d36af7720afd6b38c9",
            status=self.status,
        )
        record.save()
        self.assertEqual(record.fingerprint, "81bc1331bcd5b1c605a142d36af7720afd6b38c9")

    def test_sshfp_record_validation(self):
        with self.assertRaisesMessage(ValidationError, "{'fingerprint': ['Not a valid fingerprint in hex format']}"):
            record = SshfpRecord(
                label=random_valid_dns_name(),
                ttl=random_valid_dns_ttl(),
                algorithm=1,
                hashType=1,
                fingerprint="81bc1331bcd5b1c605a142d36af7720afdx6b38c9",
                status=self.status,
            )
            record.save()
            record.clean_fields()


class SrvRecordTestCase(TestCase):
    """Test the SRV Record Model"""

    def setUp(self):  # pylint: disable=invalid-name
        self.status = Status.objects.get(name="Active")
        self.status.content_types.add(ContentType.objects.get_for_model(SrvRecord))

    def test_srv_record_creation(self):
        record = SrvRecord(
            label=random_valid_dns_name(),
            ttl=random_valid_dns_ttl(),
            priority=10,
            weight=10,
            port=80,
            target=random_valid_dns_name(),
            status=self.status,
        )
        record.save()
        record.clean_fields()

    def test_srv_record_validation(self):
        with self.assertRaisesMessage(
            ValidationError, "{'priority': ['Ensure this value is greater than or equal to 0.']}"
        ):
            record = SrvRecord(
                label=random_valid_dns_name(),
                ttl=random_valid_dns_ttl(),
                priority=-1,
                weight=10,
                port=80,
                target=random_valid_dns_name(),
                status=self.status,
            )
            record.save()
            record.clean_fields()
        with self.assertRaisesMessage(
            ValidationError, "{'priority': ['Ensure this value is less than or equal to 65535.']}"
        ):
            record = SrvRecord(
                label=random_valid_dns_name(),
                ttl=random_valid_dns_ttl(),
                priority=7000000,
                weight=10,
                port=80,
                target=random_valid_dns_name(),
                status=self.status,
            )
            record.save()
            record.clean_fields()
        with self.assertRaisesMessage(
            ValidationError, "{'weight': ['Ensure this value is greater than or equal to 0.']}"
        ):
            record = SrvRecord(
                label=random_valid_dns_name(),
                ttl=random_valid_dns_ttl(),
                priority=10,
                weight=-1,
                port=80,
                target=random_valid_dns_name(),
                status=self.status,
            )
            record.save()
            record.clean_fields()
        with self.assertRaisesMessage(
            ValidationError, "{'weight': ['Ensure this value is less than or equal to 65535.']}"
        ):
            record = SrvRecord(
                label=random_valid_dns_name(),
                ttl=random_valid_dns_ttl(),
                priority=10,
                weight=7000000,
                port=80,
                target=random_valid_dns_name(),
                status=self.status,
            )
            record.save()
            record.clean_fields()
        with self.assertRaisesMessage(
            ValidationError, "{'port': ['Ensure this value is greater than or equal to 0.']}"
        ):
            record = SrvRecord(
                label=random_valid_dns_name(),
                ttl=random_valid_dns_ttl(),
                priority=10,
                weight=10,
                port=-1,
                target=random_valid_dns_name(),
                status=self.status,
            )
            record.save()
            record.clean_fields()
        with self.assertRaisesMessage(
            ValidationError, "{'port': ['Ensure this value is less than or equal to 65535.']}"
        ):
            record = SrvRecord(
                label=random_valid_dns_name(),
                ttl=random_valid_dns_ttl(),
                priority=10,
                weight=10,
                port=7000000,
                target=random_valid_dns_name(),
                status=self.status,
            )
            record.save()
            record.clean_fields()
