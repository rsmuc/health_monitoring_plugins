"""
Module for check_snmp_service.py
"""

#    Copyright (C) 2016-2019 rsmuc <rsmuc@sec-dev.de>

#    This file is part of "Health Monitoring Plugins".

#    "Health Monitoring Plugins" is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    "Health Monitoring Plugins" is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with "Health Monitoring Plugins".  If not, see <https://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function
from pynag.Plugins import critical, ok

# that is the base oid
BASE_OID = ".1.3.6.1.4.1.77.1.2.3.1.1"


def convert_in_oid(service_name):
    """
    calculate the correct OID for the service name
    """
    # convert the service_name to ascci
    service_ascii = [ord(c) for c in service_name]
    # we need the length of the service name
    length = str(len(service_name))
    # make the oid
    oid = BASE_OID + "." + length + "." + ".".join(str(x) for x in service_ascii)
    return oid


class Windowsservice(object):
    """Class for check_snmp_service"""

    def __init__(self, session):
        self.sess = session

    @staticmethod
    def run_scan(helper, session):
        """
        show all available services
        """

        all_services = helper.walk_snmp_values_or_exit(session, helper, BASE_OID, "Service Scan")

        print("Running services at host: " + helper.options.hostname)

        for service in all_services:
            print("Service: \t'" + service.decode("utf-8") + "'")

        # we don't want to return a icinga output, so we just end the script here
        quit()

    @staticmethod
    def check_service(helper, session):
        """
        check the defined services
        """

        # convert the service name to a oid
        service_oid = convert_in_oid(helper.options.service)
        result = session.get_oids(service_oid)[0]

        if not result or result == "NOSUCHOBJECT":
            service_status = "NOT RUNNING"
            helper.status(critical)
        else:
            service_status = "RUNNING"
            helper.status(ok)

        helper.add_summary("Status of Service '" + helper.options.service + "' is: "
                           + service_status)
