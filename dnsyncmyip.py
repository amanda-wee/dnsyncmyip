"""
Python 3 utility and classes for synchronising the actual IP address of the
current host with its domain name A record.
Currently only supports DigitalOcean DNS API.

Idea of using resolver1.opendns.com and myip.opendns.com taken from Krinkle:
https://unix.stackexchange.com/questions/22615
Code for using dnspython adapted from koblas:
https://stackoverflow.com/questions/5235569

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
import socket
import sys

import dns.resolver
from dotenv import load_dotenv

from domain_record_apis import DomainRecordApi, DomainRecordError

DEFAULT_DOMAIN_RECORD_API = 'digitalocean'


class SyncError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'Error: ' + self.message


class SyncSession:
    DNS_RESOLVER_SERVER = 'resolver1.opendns.com'
    SELF_IP_HOST_NAME = 'myip.opendns.com'

    def __init__(self, domain_name, host_name, domain_record_api):
        if not domain_name:
            raise SyncError('domain name not specified')
        self._domain_name = domain_name

        if not host_name:
            raise SyncError('host name not specified')
        self._host_name = host_name

        if not domain_record_api:
            raise SyncError('domain record API not specified')
        self._domain_record_api = domain_record_api

    def find_my_ip(self):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [socket.gethostbyname(self.DNS_RESOLVER_SERVER)]
        results = resolver.query(self.SELF_IP_HOST_NAME, 'A')
        return results[0].address if results else None

    def sync_my_ip_with_dns(self):
        actual_ip = self.find_my_ip()
        if actual_ip is None:
            raise SyncError('could not determine actual IP address')

        domain_record = self._domain_record_api.find(self._host_name)
        if domain_record is None:
            self._domain_record_api.create(self._host_name, actual_ip)
        elif domain_record['ip'] != actual_ip:
            self._domain_record_api.update(domain_record, actual_ip)


def _create_command_line_arguments():
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


def _get_domain_record_api_kwargs(api_label, domain_name):
    return {
        'digitalocean': lambda: {
            'domain_name': domain_name,
            'token': os.getenv('DNSYNCMYIP_DIGITALOCEAN_TOKEN'),
        },
    }[api_label]()


def _main():
    domain_name = os.getenv('DNSYNCMYIP_DOMAIN_NAME')
    host_name = os.getenv('DNSYNCMYIP_HOST_NAME')

    args = _create_command_line_arguments()
    if args.domain_name:
        domain_name = args.domain_name
    if args.host_name:
        host_name = args.host_name

    api_label = args.domain_record_api
    try:
        api_kwargs = _get_domain_record_api_kwargs(api_label, domain_name)
    except KeyError:
        raise SyncError('unknown domain record API "{}"'.format(api_label))

    domain_record_api = DomainRecordApi.get_api(api_label, **api_kwargs)
    sync_session = SyncSession(domain_name, host_name, domain_record_api)
    sync_session.sync_my_ip_with_dns()


if __name__ == '__main__':
    load_dotenv()

    try:
        _main()
    except (DomainRecordError, SyncError) as e:
        print(e, file=sys.stderr)
        sys.exit(1)
