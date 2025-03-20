"""Helpers for test execution."""

from faker import Faker

faker = Faker()


def random_valid_dns_name() -> str:
    """Returns a random valid dns name."""
    return faker.domain_word()


def random_valid_dns_ttl() -> int:
    """Returns a random valid dns ttl."""
    return faker.random_int(min=1, max=604800)


def random_ipv4_address() -> str:
    """Returns a random IPv4."""
    return faker.ipv4(True)


def random_ipv6_address() -> str:
    """Returns a random IPv6."""
    return faker.ipv6(True)
