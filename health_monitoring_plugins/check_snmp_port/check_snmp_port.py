#!/usr/bin/env python
# check_snmp_port.py - Check the status of a tcp/udp port via SNMP.

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

# Import PluginHelper and some utility constants from the Plugins module
from __future__ import absolute_import, division, print_function
from pynag.Plugins import ok
import health_monitoring_plugins.ipport

if __name__ == '__main__':
    # pylint: disable=C0103
    helper = health_monitoring_plugins.SnmpHelper()

    helper.parser.add_option('-p', '--port', dest='port', help='The port you want to monitor',
                             type='str', default='')
    helper.parser.add_option('-s', '--scan', dest='scan_flag', default=False, action="store_true",
                             help='Show all open ports')
    helper.parser.add_option('-t', '--type', dest="type", help="TCP or UDP", default="udp")
    helper.parser.add_option('-w', dest="warning", help="warning values", default="synSent")
    helper.parser.add_option('-c', dest="critical", help="critical vales", default="closed")

    helper.parse_arguments()

    sess = health_monitoring_plugins.SnmpSession(**helper.get_snmp_args())

    # The default return value should be always OK
    helper.status(ok)

    ipport = health_monitoring_plugins.ipport.Port(sess)

    if helper.options.scan_flag:
        ipport.run_scan(helper, sess)

    if helper.options.type.lower() == "udp" and not helper.options.scan_flag:
        ipport.check_port(helper)
        ipport.check_udp(helper, sess)

    elif helper.options.type.lower() == "tcp" and not helper.options.scan_flag:
        ipport.check_port(helper)
        ipport.check_tcp(helper, sess)

    # Print out plugin information and exit nagios-style
    helper.exit()



