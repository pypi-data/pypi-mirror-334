# Nautobot DNS Records

## Overview
This plugin allows managing DNS record in Nautobot.
The following record types are actually supported:
* A / AAAA Records
* CNAME Records
* PTR Records
* LOC Records
* SSHFP Records
* SRV Records

## Development

The Development Environment uses docker for the auxiliary containers and a virtual environment for the python dependencies.

The following requirements are needed for a setup:
* docker
* docker-compose
* poetry
* python 3.7

* Setup steps:
1. `poetry install`
2. `docker-compose up -f development/docker-compose.yml`
3. `poetry shell`
4. `python development/manage.py -c development/nautobot_config.py migrate`
5. `python development/manage.py -c development/nautobot_config.py runserver`

## Setup

1. Install the `nautobot-dns-records` package to your nautobot virtual environment
2. Run `nautobot-server migrate`

## License

This code is licensed under the [Apache License 2.0](LICENSE)

Copyright 2022, Copyright Owner: Karlsruhe Institute of Technology (KIT)

Author: Daniel Bacher

Contact: daniel.bacher@kit.edu, Institute of Software Development
