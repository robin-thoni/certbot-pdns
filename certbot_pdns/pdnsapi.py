#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import requests

_HTTP_VALID_METHODS = ('DELETE',
                       'GET',
                       'PATCH',
                       'POST',
                       'PUT')


class PdnsApi:
    api_key = None
    base_url = None
    http_auth = None                                # Standard-value of requests-library will be used
    verify_cert = None                              # Standard-value of requests-library will be used

    def set_api_key(self, api_key):
        self.api_key = api_key

    def set_base_url(self, base_url):
        self.base_url = base_url

    def set_verify_cert(self, verify_cert):
        if verify_cert in ("True", "true", True):         # convert from string to real bool if needed
            self.verify_cert = True
        elif verify_cert in ("False", "false", False):    # convert from string to real bool if needed
            self.verify_cert = False
        elif isinstance(verify_cert, str):          # alternative: path to local cert is given as string
            self.verify_cert = verify_cert          # see requests-documentation for more info
        
    def set_http_auth(self, http_auth):             # credentials should be given as list containing two string-elements
        if len(http_auth) == 2:                     # first: username, second: password for http-basic auth
            self.http_auth = (str(http_auth[0]), str(http_auth[1]))     # ensure right format of credentials
        
    def _query(self, uri, method, kwargs=None):
        headers = {
            'X-API-Key': self.api_key,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        data = None

        if method not in _HTTP_VALID_METHODS:
            raise ValueError("Invalid method '%s'" % method)

        if method[0] == 'P':
            data = json.dumps(kwargs)

        request = getattr(requests, method.lower())(self.base_url + uri,
                                                    auth=self.http_auth,
                                                    verify=self.verify_cert,
                                                    headers=headers,
                                                    data=data)

        return None if request.status_code == 204 else request.json()

    def list_zones(self):
        return self._query("/servers/localhost/zones", "GET")

    def get_zone(self, zone_name):
        return self._query("/servers/localhost/zones/%s" % zone_name, "GET")

    def update_zone(self, zone_name, data):
        return self._query("/servers/localhost/zones/%s" % zone_name, "PUT", data)

    def _patch_record(self, changetype, zone_name, name, type, ttl, content, disabled, set_ptr, records):
        if not records:
            records = [{"content": content,
                        "disabled": disabled,
                        "set-prt": set_ptr}]

        return self._query("/servers/localhost/zones/%s" % zone_name, "PATCH", {"rrsets": [
            {
                "name": name,
                "type": type,
                "ttl": ttl,
                "changetype": changetype,
                "records": records
            }
        ]})

    def replace_record(self, zone_name, name, type = 'TXT', ttl = 1, content = None, disabled = False, set_ptr = False, records = None):
        self._patch_record("REPLACE",
                           zone_name,
                           name,
                           type,
                           ttl,
                           content,
                           disabled,
                           set_ptr,
                           records)

    def delete_record(self, zone_name, name, type = 'TXT', ttl = 1, content = None, disabled = False, set_ptr = False, records = None):
        self._patch_record("DELETE",
                           zone_name,
                           name,
                           type,
                           ttl,
                           content,
                           disabled,
                           set_ptr,
                           records)

    def notify_zone(self, zone_name):
        return self._query("/servers/localhost/zones/%s/notify" % zone_name, "PUT")

    def flush_zone_cache(self, zone_name):
        return self._query("/servers/localhost/cache/flush?domain=%s" % zone_name, "PUT")
