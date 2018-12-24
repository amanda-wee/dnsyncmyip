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
2. Install the Python requirements:
```
pip3 install -r requirements.txt
```
3. Set the environment variables by creating a configuration file named `.env` in the directory where the script will be run, or possibly a parent directory thereof. Sample configuration file where `randomtoken` is the DigitalOcean API token with write access for `test.example.com`:
```
DNSYNCMYIP_DIGITALOCEAN_TOKEN=randomtoken
DNSYNCMYIP_DOMAIN_NAME=example.com
DNSYNCMYIP_HOST_NAME=test
```
The domain name and host name are optional as they can be supplied as command line arguments. To use this configuration file, install python-dotenv:
```
pip3 install python-dotenv
```
Or if using Docker, use the --env-file option:
```
docker run --rm --env-file /path/to/.env dnsyncmyip
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
If using Docker:
```
0 * * * * docker run --rm --env-file /path/to/.env dnsyncmyip
```
