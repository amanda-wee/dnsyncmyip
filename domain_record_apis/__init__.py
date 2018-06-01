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

from .base import DomainRecordApi, DomainRecordError # noqa
from .digitalocean import DigitalOceanDomainRecordApi # noqa
