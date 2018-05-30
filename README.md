DNSyncMyIP
==========
This is a Python 3 script to be run on a host with a dynamic IP address and a domain name that needs to be updated whenever the IP address changes. When run, the script discovers the actual IP address currently assigned, compares it with the IP address associated with the domain name, then updates the domain record if necessary using the DNS API of the nameserver provider. If there is no domain record, a new one will be created with the actual IP address.

Presently, it only supports the DigitalOcean DNS API.

Installation
------------
1. Clone this repository, e.g.:
```
git clone git@github.com:amanda-wee/dnsyncmyip.git dnsyncmyip
```
2. Create a configuration file named `.env` in the directory where the script will be run, or possibly a parent directory thereof. Sample configuration file where `randomtoken` is the DigitalOcean API token with write access:
```
DNSYNCMYIP_DIGITALOCEAN_TOKEN=randomtoken
```
Optionally, the domain name and host name may be specified in the configuration file, e.g., for `test.example.com`:
```
DNSYNCMYIP_DIGITALOCEAN_TOKEN=randomtoken
DNSYNCMYIP_DOMAIN_NAME=example.com
DNSYNCMYIP_HOST_NAME=test
```
3. Install the Python requirements:
```
pip3 install -r requirements.txt
```

Usage
-----
Set the script to be run regularly, e.g., with a cronjob:
```
0 * * * * python3 /path/to/dnsyncmyip.py
```
The domain name or host name may be provided as command line arguments, overriding the values in the configuration file:
```
0 * * * * python3 /path/to/dnsyncmyip.py --domain example.com --host test
```
