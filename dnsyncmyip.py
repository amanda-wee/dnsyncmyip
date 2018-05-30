"""
Python 3 utility and classes for synchronising the actual IP address of the
current host with its domain name A record.
Currently only supports DigitalOcean DNS API.

Configuration:
Create a file named .env in the current directory or a parent thereof.
Sample .env file content:
DNSYNCMYIP_DOMAIN_NAME=example.com
DNSYNCMYIP_HOST_NAME=test
DNSYNCMYIP_DIGITALOCEAN_TOKEN=randomtoken

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

import os
import socket
import sys

import dns.resolver
from dotenv import load_dotenv

from domain_record_apis import DomainRecordApi, DomainRecordError


DOMAIN_RECORD_API = 'digitalocean'


class SyncError(Exception):
    def __init__(self, message):
        self.message = message


class SyncSession:
    DNS_RESOLVER_SERVER = 'resolver1.opendns.com'
    SELF_IP_HOST_NAME = 'myip.opendns.com'

    def __init__(self, domain_name, host_name, domain_record_api):
        if not domain_name:
            raise SyncError('Error: domain name not specified')
        self._domain_name = domain_name

        if not host_name:
            raise SyncError('Error: host name not specified')
        self._host_name = host_name

        if not domain_record_api:
            raise SyncError('Error: domain record API not specified')
        self._domain_record_api = domain_record_api

    def find_my_ip(self):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [socket.gethostbyname(self.DNS_RESOLVER_SERVER)]
        results = resolver.query(self.SELF_IP_HOST_NAME, 'A')
        return results[0].address if results else None

    def sync_my_ip_with_dns(self):
        actual_ip = self.find_my_ip()
        if actual_ip is None:
            raise SyncError('Error: could not determine actual IP address')

        domain_record = self._domain_record_api.find(self._host_name)
        if domain_record is None:
            self._domain_record_api.create(self._host_name, actual_ip)
        elif domain_record['ip'] != actual_ip:
            self._domain_record_api.update(domain_record, actual_ip)


if __name__ == '__main__':
    load_dotenv()

    domain_name = os.getenv('DNSYNCMYIP_DOMAIN_NAME')
    host_name = os.getenv('DNSYNCMYIP_HOST_NAME')
    token = os.getenv('DNSYNCMYIP_DIGITALOCEAN_TOKEN')

    try:
        domain_record_api = DomainRecordApi.get_api(DOMAIN_RECORD_API,
                                                    domain_name,
                                                    token)
        sync_session = SyncSession(domain_name, host_name, domain_record_api)
        sync_session.sync_my_ip_with_dns()
    except (DomainRecordError, SyncError) as e:
        print(e.message, file=sys.stderr)
