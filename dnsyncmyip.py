"""
Python 3 utility for synchronising the actual IP address of the current host
with its domain name A record. Currently only supports DigitalOcean DNS API.

License Notice
--------------
Copyright 2018 Amanda Wee

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import argparse
import os
import sys

from dotenv import load_dotenv

from domain_record_apis import DomainRecordApi, DomainRecordError
from sync_session import SyncSession, SyncError

DEFAULT_DOMAIN_RECORD_API = 'digitalocean'


def parse_command_line_arguments():
    """
    Parses the command line arguments and returns them.
    """
    arg_parser = argparse.ArgumentParser(
        description='Synchronise the actual (usually dynamic) IP address of '
                    'the current host with its domain name A record'
    )
    api_help = 'Domain record API (default: {}) [{}]'.format(
        DEFAULT_DOMAIN_RECORD_API,
        ' | '.join(DomainRecordApi.get_api_labels())
    )
    arg_parser.add_argument('--api',
                            '-A',
                            dest='domain_record_api',
                            default=DEFAULT_DOMAIN_RECORD_API,
                            help=api_help)
    arg_parser.add_argument('--domain',
                            '-D',
                            dest='domain_name',
                            help='Domain name')
    arg_parser.add_argument('--host',
                            '-H',
                            dest='host_name',
                            help='Host name (format depends on DNS API)')
    return arg_parser.parse_args()


def get_domain_record_api_kwargs(api_label, domain_name):
    """
    Returns the keyword arguments to initialise the domain name record API with
    the given api_label.
    """
    return {
        'digitalocean': lambda: {
            'domain_name': domain_name,
            'token': os.getenv('DNSYNCMYIP_DIGITALOCEAN_TOKEN'),
        },
    }[api_label]()


def main():
    """
    Synchronises the actual IP address of the current host with its domain name
    A record.
    """
    domain_name = os.getenv('DNSYNCMYIP_DOMAIN_NAME')
    host_name = os.getenv('DNSYNCMYIP_HOST_NAME')

    args = parse_command_line_arguments()
    if args.domain_name:
        domain_name = args.domain_name
    if args.host_name:
        host_name = args.host_name

    api_label = args.domain_record_api
    try:
        api_kwargs = get_domain_record_api_kwargs(api_label, domain_name)
    except KeyError:
        raise SyncError('unknown domain record API "{}"'.format(api_label))

    domain_record_api = DomainRecordApi.get_api(api_label, **api_kwargs)
    sync_session = SyncSession(domain_record_api)
    sync_session.sync_my_ip_with_dns(host_name)


if __name__ == '__main__':
    load_dotenv()

    try:
        main()
    except (DomainRecordError, SyncError) as e:
        sys.exit(e)
