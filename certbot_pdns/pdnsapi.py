import json

import requests


class PdnsApi:
    http_auth_user = None
    http_auth_pass = None
    api_key = None
    api_pass = None
    base_url = None

    def set_api_key(self, api_key):
        self.api_key = api_key

    def set_base_url(self, base_url):
        self.base_url = base_url

    def set_api_pass(self, api_pass):
        self.api_pass = api_pass
        
    def set_http_auth_user(self, http_auth_user):
        self.http_auth_user = http_auth_user
        
    def set_http_auth_pass(self, http_auth_pass):
        self.http_auth_pass = http_auth_pass
        
    def _query(self, uri, method, kwargs=None):
        headers = {
            'X-API-Key': self.api_key,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        data = json.dumps(kwargs)

        if method == "GET":
            request = requests.get(self.base_url + uri, headers=headers, auth=(self.http_auth_user, self.http_auth_pass))
        elif method == "POST":
            request = requests.post(self.base_url + uri, headers=headers, auth=(self.http_auth_user, self.http_auth_pass), data=data)
        elif method == "PUT":
            request = requests.put(self.base_url + uri, headers=headers, auth=(self.http_auth_user, self.http_auth_pass), data=data)
        elif method == "PATCH":
            request = requests.patch(self.base_url + uri, headers=headers, auth=(self.http_auth_user, self.http_auth_pass), data=data)
        elif method == "DELETE":
            request = requests.delete(self.base_url + uri, headers=headers, auth=(self.http_auth_user, self.http_auth_pass))
        else:
            raise ValueError("Invalid method '%s'" % method)

        return None if request.status_code == 204 else request.json()

    def list_zones(self):
        return self._query("/servers/localhost/zones", "GET")

    def get_zone(self, zone_name):
        return self._query("/servers/localhost/zones/%s" % zone_name, "GET")

    def update_zone(self, zone_name, data):
        return self._query("/servers/localhost/zones/%s" % zone_name, "PUT", data)

    def replace_record(self, zone_name, name, type, ttl, content, disabled, set_ptr):
        return self._query("/servers/localhost/zones/%s" % zone_name, "PATCH", {"rrsets": [
            {
                "name": name,
                "type": type,
                "ttl": ttl,
                "changetype": "REPLACE",
                "records": [
                    {
                        "content": content,
                        "disabled": disabled,
                        "set-prt": set_ptr
                    }
                ]
            }
        ]})

    def delete_record(self, zone_name, name, type, ttl, content, disabled, set_ptr):
        return self._query("/servers/localhost/zones/%s" % zone_name, "PATCH", {"rrsets": [
            {
                "name": name,
                "type": type,
                "ttl": ttl,
                "changetype": "DELETE",
                "records": [
                    {
                        "content": content,
                        "disabled": disabled,
                        "set-prt": set_ptr
                    }
                ]
            }
        ]})

    def notify_zone(self, zone_name):
        return self._query("/servers/localhost/zones/%s/notify" % zone_name, "PUT")

    def flush_zone_cache(self, zone_name):
        return self._query("/servers/localhost/cache/flush?domain=%s" % zone_name, "PUT")
