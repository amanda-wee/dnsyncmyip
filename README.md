DNSyncMyIP
==========
This is a Python 3 script to be run on a host with a dynamic IP address and a domain name that needs to be updated whenever the IP address changes. When run, the script discovers the actual IP address currently assigned, compares it with the IP address associated with the domain name, then updates the domain record if necessary using the DNS API of the nameserver provider. If there is no domain record, a new one will be created with the actual IP address.

Presently, it only supports the DigitalOcean DNS API.

Installation
------------
For running the script directly:
1. Clone this repository, e.g.:
```
git clone https://github.com/amanda-wee/dnsyncmyip.git dnsyncmyip
```
2. Install the Python requirements:
```
pip3 install -r requirements.txt
pip3 install python-dotenv
```

For running the script in a Docker container:
1. Pull from Docker Hub:
```
docker pull aranel/dnsyncmyip
```

For running the script in a Docker container on a Synology NAS:
1. Install the Docker package.
2. From the Docker package's Registry, find and download `aranel/dnsyncmyip`

Configuration
-------------
Set the environment variables by creating a configuration file named `.env` in the directory where the script will be run, or possibly a parent directory thereof. Sample configuration file where `randomtoken` is the DigitalOcean API token with write access for `test.example.com`:
```
DNSYNCMYIP_DIGITALOCEAN_TOKEN=randomtoken
DNSYNCMYIP_DOMAIN_NAME=example.com
DNSYNCMYIP_HOST_NAME=test
```
The domain name and host name are optional as they can be supplied as command line arguments.

For running the script in a Docker container on a Synology NAS:
1. Create a `dnsyncmyip` subfolder in the user's home folder. The folder permissions should be changed to ensure that no other users have access to it.
2. Upload the `.env` file to this `dnsyncmyip` subfolder.

Usage
-----
* Set the script to be run regularly, e.g., with a cronjob:
```
0 * * * * python3 /path/to/dnsyncmyip.py
```
* The domain name or host name may be provided as command line arguments, overriding the values in the configuration file:
```
0 * * * * python3 /path/to/dnsyncmyip.py --domain example.com --host test
```
* For running the script in a Docker container, use the Docker host's version of cron:
```
0 * * * * docker run --rm --env-file /path/to/.env aranel/dnsyncmyip
```
* For running the script in a Docker container on a Synology NAS, use the Task Scheduler with a user-defined script owned by root, replacing `username` with the username of the user:
```
docker run --rm --env-file /var/services/homes/username/dnsyncmyip/.env aranel/dnsyncmyip
```
