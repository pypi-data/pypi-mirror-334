"""Modifies build in nautobot templates."""

from django.urls import reverse
from nautobot.extras.plugins import PluginTemplateExtension


class DeviceExtensions(PluginTemplateExtension):
    """Extend the device detail view."""

    model = "dcim.device"

    def detail_tabs(self):
        """Add tabs to the device detail view."""
        return [
            {
                "title": "DNS Records",
                "url": reverse(
                    "plugins:nautobot_dns_records:device_records_tab", kwargs={"pk": self.context["object"].pk}
                ),
            },
        ]

    def buttons(self):
        """Add additional buttons to the device detail view."""
        addressrecord_url = f"{reverse('plugins:nautobot_dns_records:addressrecord_add')}?device={self.context['object'].pk}&return_url={reverse('plugins:nautobot_dns_records:device_records_tab', kwargs={'pk': self.context['object'].pk})}?tab=nautobot_dns_records:1"
        txtrecord_url = f"{reverse('plugins:nautobot_dns_records:txtrecord_add')}?device={self.context['object'].pk}&return_url={reverse('plugins:nautobot_dns_records:device_records_tab', kwargs={'pk': self.context['object'].pk})}?tab=nautobot_dns_records:1"
        locrecord_url = f"{reverse('plugins:nautobot_dns_records:locrecord_add')}?device={self.context['object'].pk}&return_url={reverse('plugins:nautobot_dns_records:device_records_tab', kwargs={'pk': self.context['object'].pk})}?tab=nautobot_dns_records:1"
        cnamerecord_url = f"{reverse('plugins:nautobot_dns_records:cnamerecord_add')}?device={self.context['object'].pk}&return_url={reverse('plugins:nautobot_dns_records:device_records_tab', kwargs={'pk': self.context['object'].pk})}?tab=nautobot_dns_records:1"
        ptrrecord_url = f"{reverse('plugins:nautobot_dns_records:ptrrecord_add')}?device={self.context['object'].pk}&return_url={reverse('plugins:nautobot_dns_records:device_records_tab', kwargs={'pk': self.context['object'].pk})}?tab=nautobot_dns_records:1"
        sshfprecord_url = f"{reverse('plugins:nautobot_dns_records:sshfprecord_add')}?device={self.context['object'].pk}&return_url={reverse('plugins:nautobot_dns_records:device_records_tab', kwargs={'pk': self.context['object'].pk})}?tab=nautobot_dns_records:1"
        srvrecord_url = f"{reverse('plugins:nautobot_dns_records:srvrecord_add')}?device={self.context['object'].pk}&return_url={reverse('plugins:nautobot_dns_records:device_records_tab', kwargs={'pk': self.context['object'].pk})}?tab=nautobot_dns_records:1"
        add_dns_records = (
            '<div class="btn-group">'
            '<button type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
            '<span class="mdi mdi-plus-thick" aria-hidden="true"></span> Add DNS Records <span class="caret"></span>'
            "</button>"
            '<ul class="dropdown-menu">'
            f'<li><a href="{addressrecord_url}">Address Record</a></li>'
            f'<li><a href="{txtrecord_url}">TXT Record</a></li>'
            f'<li><a href="{locrecord_url}">LOC Record</a></li>'
            f'<li><a href="{cnamerecord_url}">CNAME Record</a></li>'
            f'<li><a href="{ptrrecord_url}">PTR Record</a></li>'
            f'<li><a href="{sshfprecord_url}">SSHFP Record</a></li>'
            f'<li><a href="{srvrecord_url}">SRV Record</a></li>'
            "</ul>"
            "</div>"
        )
        return add_dns_records

    def full_width_page(self):
        """Add additional full width content to the device detail view."""
        return ""

    def left_page(self):
        """Add additional content to the left page of the device detail view."""
        return ""

    def right_page(self):
        """Add additional content to the left page of the device detail view."""
        return ""

    def list_buttons(self):
        """Add additional buttons to the buttons of the device detail view."""
        return ""


class IPAddressExtensions(PluginTemplateExtension):
    """Extend the IP address detail view."""

    model = "ipam.ipaddress"

    def detail_tabs(self):
        """Add tabs to the IP address detail view."""
        return [
            {
                "title": "DNS Records",
                "url": reverse(
                    "plugins:nautobot_dns_records:address_records_tab", kwargs={"pk": self.context["object"].pk}
                ),
            },
        ]

    def buttons(self):
        """Add additional buttons to the IP address detail view."""
        addressrecord_url = f"{reverse('plugins:nautobot_dns_records:addressrecord_add')}?address={self.context['object'].pk}&return_url={reverse('plugins:nautobot_dns_records:address_records_tab', kwargs={'pk': self.context['object'].pk})}?tab=nautobot_dns_records:1"
        ptrrecord_url = f"{reverse('plugins:nautobot_dns_records:ptrrecord_add')}?address={self.context['object'].pk}&return_url={reverse('plugins:nautobot_dns_records:address_records_tab', kwargs={'pk': self.context['object'].pk})}?tab=nautobot_dns_records:1"
        add_dns_records = (
            '<div class="btn-group">'
            '<button type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
            '<span class="mdi mdi-plus-thick" aria-hidden="true"></span> Add DNS Records <span class="caret"></span>'
            "</button>"
            '<ul class="dropdown-menu">'
            f'<li><a href="{addressrecord_url}">Address Record</a></li>'
            f'<li><a href="{ptrrecord_url}">PTR Record</a></li>'
            "</ul>"
            "</div>"
        )
        return add_dns_records

    def full_width_page(self):
        """Add additional full width content to the IP address detail view."""
        return ""

    def left_page(self):
        """Add additional content to the left page of the IP address detail view."""
        return ""

    def right_page(self):
        """Add additional content to the left page of the IP address detail view."""
        return ""

    def list_buttons(self):
        """Add additional buttons to the buttons of the IP address detail view."""
        return ""


template_extensions = [
    DeviceExtensions,
    IPAddressExtensions,
]
