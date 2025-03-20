"""Content for the nautobot homepage."""

from nautobot.core.apps import HomePageItem, HomePagePanel
from .models import AddressRecord, TxtRecord, LocRecord, CNameRecord, PtrRecord, SshfpRecord, SrvRecord

layout = (
    HomePagePanel(
        name="DNS Records",
        weight=450,
        items=[
            HomePageItem(
                name="Address Records",
                model=AddressRecord,
                weight=10,
                link="plugins:nautobot_dns_records:addressrecord_list",
                description="DNS Records related to an IP address (A and AAAA)",
                permissions=["nautobot_dns_records.list_address_record"],
            ),
            HomePageItem(
                name="TXT Records",
                model=TxtRecord,
                weight=20,
                link="plugins:nautobot_dns_records:txtrecord_list",
                description="DNS Records for text",
                permissions=["nautobot_dns_records.list_txt_records"],
            ),
            HomePageItem(
                name="LOC Records",
                model=LocRecord,
                weight=30,
                link="plugins:nautobot_dns_records:locrecord_list",
                description="DNS Records related to an Location)",
                permissions=["nautobot_dns_records.list_loc_records"],
            ),
            HomePageItem(
                name="CNAME Records",
                model=CNameRecord,
                weight=40,
                link="plugins:nautobot_dns_records:cnamerecord_list",
                description="DNS Records related to an other record",
                permissions=["nautobot_dns_records.list_cname_records"],
            ),
            HomePageItem(
                name="PTR Records",
                model=PtrRecord,
                weight=50,
                link="plugins:nautobot_dns_records:ptrrecord_list",
                description="DNS records to resolve IP addresses backwards",
                permissions=["nautobot_dns_records.list_ptr_records"],
            ),
            HomePageItem(
                name="SSHFP Records",
                model=SshfpRecord,
                weight=60,
                link="plugins:nautobot_dns_records:sshfprecord_list",
                description="DNS records to store SSH fingerprints",
                permissions=["nautobot_dns_records.list_sshfprecord_records"],
            ),
            HomePageItem(
                name="SRV Records",
                model=SrvRecord,
                weight=70,
                link="plugins:nautobot_dns_records:srvrecord_list",
                description="DNS records for server resources",
                permissions=["nautobot_dns_records.list_srv_records"],
            ),
        ],
    ),
)
