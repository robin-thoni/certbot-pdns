certbot-pdns
============

Authenticator plugin for certbot (https://certbot.eff.org/).

Perform a DNS-01 challenge using TXT record in a PowerDNS (https://doc.powerdns.com/md/)

The advantages are:
 - No need to configure your web server to serve challenges
 - Web server not even needed
 - Can generate certificate for internal hosts that are not exposed to the Internet
 - A or CNAME record not even needed. Only the TXT record added by certbot-pdns matters.

Installation
------------

Install or upgrade certbot:

`pip install -U certbot`

Install certbot-pdns from sources:

`python setup.py install`

Check that `certbot-pdns:auth` is listed when executing `certbot --text plugins`

Configuration
-------------

Configuration file: `/etc/letsencrypt/certbot-pdns.json`:
 - api-key: Your PowerDNS API Key as specified in property `api-key` in file `/etc/powerdns/pdns.conf`
 - base-url: The base URL for PowerDNS API. Require `api=yes` and `api-readonly=no` in file `/etc/powerdns/pdns.conf`
 - axfr-time: The time in seconds to wait for zone replication in slaves. Can be set to 0 if there is only one authoritative server for the zone.

Usage
-----

Use certbot as usual but specify `--authenticator certbot-pdns:auth certonly`:

`certbot --agree-tos --text --renew-by-default --authenticator certbot-pdns:auth certonly -d example.com -d www.example.com`
