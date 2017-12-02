"""DNS plugin."""
import collections
import logging

import zope.interface
from acme import challenges
from certbot import interfaces
from certbot.plugins import common

from certbot_pdns.PdnsApiAuthenticator import PdnsApiAuthenticator

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(common.Plugin):
    """PDNS Authenticator."""

    description = "Place challenges in DNS records"

    MORE_INFO = """\
Authenticator plugin that performs dns-01 challenge by saving
necessary validation resources to appropriate records in a PowerDNS server."""

    backend = None

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return self.MORE_INFO

    @classmethod
    def add_parser_arguments(cls, add):
        add("certbot-pdns-config", default="/etc/letsencrypt/certbot-pdns.json",
            help="Path to certbot-pdns configuration file")

    def get_chall_pref(self, domain):  # pragma: no cover
        # pylint: disable=missing-docstring,no-self-use,unused-argument
        return [challenges.DNS01]

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.full_roots = {}
        self.performed = collections.defaultdict(set)

    def prepare(self):  # pylint: disable=missing-docstring
        self.backend = PdnsApiAuthenticator()
        conf_path = self.conf("certbot-pdns-config")
        self.backend.prepare(conf_path)
        pass

    def perform(self, achalls):  # pylint: disable=missing-docstring
        responses = []
        zones = []
        for achall in achalls:
            response, validation = achall.response_and_validation()
            resp = self.backend.perform_single(achall, response, validation)
            responses.append(resp)

            domain = achall.domain
            zone = self.backend.find_best_matching_zone(domain)
            if zone not in zones:
                zones.append(zone)

        for zone in zones:
            self.backend.perform_notify(zone)

        self.backend.wait_for_propagation(achalls)
        return responses

    def cleanup(self, achalls):  # pylint: disable=missing-docstring
        for achall in achalls:
            self.backend.cleanup(achall)
