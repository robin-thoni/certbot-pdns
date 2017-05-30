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

`pip2 install -U certbot`

Install certbot-pdns:

```
#Install from pip
pip2 install certbot-pdns
#Install from sources
python2 setup.py install
```

Check that `certbot-pdns:auth` is listed when executing `certbot --text plugins`

Configuration
-------------

An example file is provided in `/usr/local/etc/letsencrypt/certbot-pdns.json`:
```
{
  "api-key": "change_it",
  "base-url": "http://127.0.0.1:34022/api/v1",
  "axfr-time": 5
}
```

Configuration file must be placed in `/etc/letsencrypt/certbot-pdns.json` or be specified with argument `certbot-pdns-config`.

Configuration keys:

 - api-key: Your PowerDNS API Key as specified in property `api-key` in file `/etc/powerdns/pdns.conf`
 - base-url: The base URL for PowerDNS API. Require `api=yes` and `api-readonly=no` in file `/etc/powerdns/pdns.conf`
 - axfr-time: The time in seconds to wait for AXFR in slaves. Can be set to 0 if there is only one authoritative server for the zone.

Usage
-----

Use certbot as usual but specify `--authenticator certbot-pdns:auth`:

`certbot --agree-tos --text --renew-by-default --authenticator certbot-pdns:auth certonly -d example.com -d www.example.com`
