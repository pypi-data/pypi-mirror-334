"""nautobot_dns_records Plugin Initilization."""

from nautobot.apps import NautobotAppConfig


class NautobotDnsRecordsConfig(NautobotAppConfig):
    """Plugin configuration for the nautobot_dns_records plugin."""

    name = "nautobot_dns_records"  # Raw plugin name; same as the plugin's source directory.
    verbose_name = "DNS Records"  # Human-friendly name for the plugin.
    base_url = "dns"  # (Optional) Base path to use for plugin URLs. Defaulting to app_name.
    required_settings = []  # A list of any configuration parameters that must be defined by the user.
    min_version = "2.0.0"  # Minimum version of Nautobot with which the plugin is compatible.
    # max_version = "1.4.0"  # Maximum version of Nautobot with which the plugin is compatible.
    default_settings = {}  # A dictionary of configuration parameters and their default values.
    caching_config = {}  # Plugin-specific cache configuration.
    author = "Daniel Bacher"
    author_email = "bacher@kit.edu"
    version = "0.2.0"
    description = "This plugin allows to manage DNS records in Nautobot"

    searchable_models = [
        "addressrecord",
        "txtrecord",
        "locrecord",
        "cnamerecord",
        "ptrrecord",
        "sshfprecord",
        "srvrecord",
    ]


config = NautobotDnsRecordsConfig  # pylint:disable=invalid-name
