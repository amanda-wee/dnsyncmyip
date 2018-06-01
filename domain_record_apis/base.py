"""
Python 3 API for accessing DNS host APIs to synchronise the actual IP
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


class DomainRecordError(Exception):
    """
    Exception to be raised on domain record API errors detected by
    DomainRecordApi or its subclasses.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'Error: ' + self.message


class DomainRecordApi:
    """
    Models a domain record API for synchronising the actual IP address of a
    host with its domain name A record.
    """
    _api_classes = {}

    @classmethod
    def get_api(cls, api_label, *args, **kwargs):
        """
        Returns a new instance of the DomainRecordApi subclass instantiated
        with the given arguments.
        """
        try:
            return cls._api_classes[api_label](*args, **kwargs)
        except KeyError:
            raise DomainRecordError('domain record API with the label "{}" '
                                    'does not exist'.format(api_label))

    @classmethod
    def get_api_labels(cls):
        """
        Returns iterable of strings corresponding to the available
        DomainRecordApi subclass labels.
        """
        return cls._api_classes.keys()

    @classmethod
    def register(cls, api_label):
        """
        Returns a class decorator to decorate a class as being a
        DomainRecordApi subclass with the given label.
        """
        def decorator(api_class):
            cls._api_classes[api_label] = api_class
            return api_class
        return decorator

    def create(self, host_name, actual_ip):
        """
        Creates the domain name A record given the hostname and the actual IP
        address. Returns None on success.
        """
        raise NotImplementedError

    def find(self, host_name):
        """
        Returns the domain name A record corresponding to the given hostname,
        or None if there is no domain name record with the given hostname.
        The domain name record returned shall be a dictionary with at least
        'ip' as one of the keys; the remaining layout of the dictionary depends
        on the DomainRecordApi subclass.
        """
        raise NotImplementedError

    def update(self, domain_record, actual_ip):
        """
        Updates the domain name record with the actual IP address. Returns None
        on success.
        """
        raise NotImplementedError
