"""Navigation Items to add to Nautobot for nautobot_dns_records."""

from nautobot.apps.ui import NavMenuTab, NavMenuGroup, NavMenuItem

menu_items = (
    NavMenuTab(
        name="DNS",
        weight=350,
        groups=[
            NavMenuGroup(
                name="Records",
                weight=100,
                items=[
                    NavMenuItem(
                        link="plugins:nautobot_dns_records:addressrecord_list",
                        name="Address Records",
                        permissions=["nautobot_dns_records.list_address_record"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_dns_records:txtrecord_list",
                        name="TXT Records",
                        permissions=["nautobot_dns_records.list_txt_records"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_dns_records:locrecord_list",
                        name="LOC Records",
                        permissions=["nautobot_dns_records.list_loc_records"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_dns_records:cnamerecord_list",
                        name="CNAME Records",
                        permissions=["nautobot_dns_records.list_cname_records"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_dns_records:ptrrecord_list",
                        name="PTR Records",
                        permissions=["nautobot_dns_records.list_ptr_records"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_dns_records:sshfprecord_list",
                        name="SSHFP Records",
                        permissions=["nautobot_dns_records.list_sshfprecord_records"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_dns_records:srvrecord_list",
                        name="SRV Records",
                        permissions=["nautobot_dns_records.list_srv_records"],
                    ),
                ],
            ),
        ],
    ),
)
