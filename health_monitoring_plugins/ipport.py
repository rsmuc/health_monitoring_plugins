"""
Module for check_snmp_port.py
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
from pynag.Plugins import critical, ok, unknown, warning

# that is the base oid
OPEN_UDP_PORTS_OID = ".1.3.6.1.2.1.7.5.1.2"
TCP_PORTS_OID = ".1.3.6.1.2.1.6.13.1.3"
TCP_PORTS_STATUS_OID = ".1.3.6.1.2.1.6.13.1.1"

# from tcpConnState from TCP-MIB
TCP_STATES = {
    "1": "closed",
    "2": "listen",
    "3": "synSent",
    "4": "synReceived",
    "5": "established",
    "6": "finWait1",
    "7": "finWait2",
    "8": "closeWait",
    "9": "lastAck",
    "10": "closing",
    "11": "timeWait",
    "12": "deleteTCB"
}


class Port(object):
    """Class for check_snmp_port"""

    def __init__(self, session):
        self.sess = session

    @staticmethod
    def check_port(helper):
        """
        check if the port parameter is really a port or "scan"
        """
        try:
            int(helper.options.port)
        except ValueError:
            helper.exit(summary="Port (-p) must be a integer value.", exit_code=unknown,
                        perfdata='')

    @staticmethod
    def get_open_udp_ports(helper, session):
        """ get the open UDP ports """
        open_ports = helper.walk_snmp_values_or_exit(session, helper,
                                                     OPEN_UDP_PORTS_OID, "Open UDP Ports")
        return open_ports

    @staticmethod
    def get_open_tcp_ports(helper, session):
        """ get the open tcp ports and the status"""
        open_ports = helper.walk_snmp_values_or_exit(session, helper,
                                                     TCP_PORTS_OID, "Open TCP Ports")
        port_status = helper.walk_snmp_values_or_exit(session, helper,
                                                      TCP_PORTS_STATUS_OID, "Port Status")

        return open_ports, port_status

    def run_scan(self, helper, session):
        """
        show all open ports
        """

        # UDP ports
        print("All open UDP ports at host " + helper.options.hostname)
        for port in self.get_open_udp_ports(helper, session):
            print("UDP: \t" + port)

        # TCP ports
        # make a dict out of the two lists (ports & status)
        ports_and_status = dict(zip(self.get_open_tcp_ports(helper, session)[0],
                                    self.get_open_tcp_ports(helper, session)[1]))

        # here we show all open TCP ports and it's status
        print ("\n\n\nAll open TCP ports at host " + helper.options.hostname)

        for port in ports_and_status:
            tcp_status = ports_and_status[port]
            tcp_status = TCP_STATES[tcp_status]
            print("TCP: \t" + port + "\t Status: \t" + tcp_status)

        quit()

    def check_udp(self, helper, session):
        """
        check the status of the UDP ports
        """
        open_ports = self.get_open_udp_ports(helper, session)

        if helper.options.port in open_ports:
            udp_status = "OPEN"

        else:
            udp_status = "CLOSED"
            helper.status(critical)

        helper.add_summary("Current status for UDP port "
                           + helper.options.port
                           + " is: "
                           + udp_status)

    def check_tcp(self, helper, session):
        """
        check the status of the TCP ports
        """

        open_ports = self.get_open_tcp_ports(helper, session)[0]
        port_states = self.get_open_tcp_ports(helper, session)[1]

        ports_and_states = dict(zip(open_ports, port_states))

        if helper.options.port in open_ports:

            # if the port is available in the list of open_ports, then extract the status
            tcp_status = ports_and_states[helper.options.port]

            # translate the status from the integer value to a human readable string
            tcp_status = TCP_STATES[tcp_status]

            # now let's set the status according to the warning / critical "threshold" parameter
            if tcp_status in helper.options.warning:
                helper.status(warning)

            elif tcp_status in helper.options.critical:
                helper.status(critical)

            else:
                helper.status(ok)
        else:
            # if there is no value in the list => the port is closed for sure
            tcp_status = "CLOSED"
            helper.status(critical)

        helper.add_summary("Current status for TCP port "
                           + helper.options.port
                           + " is: "
                           + tcp_status)
