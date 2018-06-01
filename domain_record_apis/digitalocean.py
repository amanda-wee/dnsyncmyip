"""
Python 3 API for accessing DigitalOcean API to synchronise the actual IP
address of a host with its domain name A record.

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

import requests

from .base import DomainRecordApi, DomainRecordError


class DigitalOceanApi:
    """
    Simple wrapper class for GET, POST, and PUT requests to be made to the
    DigitalOcean API.
    """
    BASE_URI = 'https://api.digitalocean.com/v2/'

    def __init__(self, token):
        self._authorization = 'Bearer {}'.format(token)

    def get(self, path):
        return requests.get(''.join([self.BASE_URI, path]),
                            headers={'Authorization': self._authorization})

    def post(self, path, json_data):
        return requests.post(''.join([self.BASE_URI, path]),
                             json=json_data,
                             headers={'Authorization': self._authorization,
                                      'Content-Type': 'application/json'})

    def put(self, path, json_data):
        return requests.put(''.join([self.BASE_URI, path]),
                            json=json_data,
                            headers={'Authorization': self._authorization,
                                     'Content-Type': 'application/json'})

    def follow_link(self, link):
        return requests.get(link,
                            headers={'Authorization': self._authorization})


@DomainRecordApi.register('digitalocean')
class DigitalOceanDomainRecordApi(DomainRecordApi):
    """
    Domain record API for synchronising the actual IP address of a host with
    its domain name A record on DigitalOcean.
    """
    def __init__(self, domain_name, token):
        if not domain_name:
            raise DomainRecordError('Error: domain name not specified')
        self._domain_name = domain_name

        if not token:
            raise DomainRecordError('Error: DigitalOcean API token not '
                                    'specified')
        self._api = DigitalOceanApi(token)

    def create(self, host_name, actual_ip):
        path = 'domains/{}/records'.format(self._domain_name)
        json_data = {'type': 'A', 'name': host_name, 'data': actual_ip}
        response = self._api.post(path, json_data)
        if not response.ok:
            raise DomainRecordError('Error: could not create domain record')

    def find(self, host_name):
        path = 'domains/{}/records?per_page=100'.format(self._domain_name)
        response = self._api.get(path)
        while True:
            if not response.ok:
                raise DomainRecordError(
                    'Error: failure when finding domain record'
                )

            result = response.json()
            for domain_record in result['domain_records']:
                if (domain_record['type'] == 'A' and
                        domain_record['name'] == host_name):
                    return {'id': domain_record['id'],
                            'ip': domain_record['data']}

            if result['links'] and 'next' in result['links']:
                response = self._api.follow_link(result['links']['next'])
            else:
                return None

    def update(self, domain_record, actual_ip):
        path = 'domains/{}/records/{}'.format(self._domain_name,
                                              domain_record['id'])
        json_data = {'data': actual_ip}
        response = self._api.put(path, json_data)
        if not response.ok:
            raise DomainRecordError('Error: could not update domain record')
