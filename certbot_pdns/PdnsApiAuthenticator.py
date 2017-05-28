import json

import logging

import time
from certbot import errors

from certbot_pdns.pdnsapi import PdnsApi

logger = logging.getLogger(__name__)


class PdnsApiAuthenticator:
    api = None
    zones = None
    axfr_time = None

    def find_best_matching_zone(self, domain):
        if domain is None or domain == "":
            return None
        for zone in self.zones:
            if zone['name'] == domain + ".":
                return zone
        return self.find_best_matching_zone(domain[domain.index(".") + 1:]) if "." in domain else None

    def find_soa(self, zone):
        for rrset in zone["rrsets"]:
            if rrset["type"] == "SOA":
                return rrset, rrset["records"][0]
        return None

    def flush_zone(self, zone_name):
        res = self.api.flush_zone_cache(zone_name)
        if res is None or "result" not in res or res["result"] != "Flushed cache.":
            raise errors.PluginError("Bad return from PDNS API when flushing cache: %s" % res)

    def notify_zone(self, zone_name):
        res = self.api.notify_zone(zone_name)
        if res is None or "result" not in res or res["result"] != "Notification queued":
            raise errors.PluginError("Bad return from PDNS API when notifying: %s" % res)

    def update_soa(self, zone_name):
        zone = self.api.get_zone(zone_name)
        if zone is None or "error" in zone:
            raise errors.PluginError("Bad return from PDNS API when getting zone %s: %s" % (zone_name, zone))
        rrset, soa = self.find_soa(zone)
        split = soa["content"].split(" ")
        split[2] = str(int(split[2]) + 1)
        soa["content"] = ' '.join(split)
        res = self.api.replace_record(zone_name, zone_name, rrset["type"], rrset["ttl"], soa["content"],
                                      soa["disabled"], False)
        if res is not None:
            raise errors.PluginError("Bad return from PDNS API when updating SOA: %s" % res)

    def prepare(self, conf_path):
        self.api = PdnsApi()
        with open(conf_path) as f:
            config = json.load(f)
        self.api.set_api_key(config["api-key"])
        self.api.set_base_url(config["base-url"])
        self.axfr_time = config["axfr-time"]
        self.zones = self.api.list_zones()
        # print(self.zones)
        # raw_input('Press <ENTER> to continue')
        if self.zones is None or "error" in self.zones:
            raise errors.PluginError("Could not list zones %s" % self.zones)

    def perform_single(self, achall, response, validation):
        domain = achall.domain
        token = validation.encode()
        zone = self.find_best_matching_zone(domain)
        if zone is None:
            raise errors.PluginError("Could not find zone for %s" % domain)

        logger.debug("Found zone %s for domain %s" % (zone["name"], domain))

        res = self.api.replace_record(zone["name"], "_acme-challenge." + domain + ".", "TXT", 1, "\"" + token + "\"", False, False)
        if res is not None:
            raise errors.PluginError("Bad return from PDNS API when adding record: %s" % res)
        self.update_soa(zone["name"])
        self.flush_zone(zone["name"])
        self.notify_zone(zone["name"])

        # raw_input('Press <ENTER> to continue')
        logger.info("Waiting %i seconds..." % self.axfr_time)
        time.sleep(self.axfr_time)

        return response

    def cleanup(self, achall):
        domain = achall.domain
        zone = self.find_best_matching_zone(domain)
        if zone is None:
            return
        res = self.api.delete_record(zone["name"], "_acme-challenge." + domain + ".", "TXT", 1, None, False, False)
        if res is not None:
            raise errors.PluginError("Bad return from PDNS API when deleting record: %s" % res)
        self.update_soa(zone["name"])
        self.flush_zone(zone["name"])
        self.notify_zone(zone["name"])
