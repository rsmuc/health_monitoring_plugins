#!/usr/bin/env python
# check_snmp_service.py - Check if a Windows service is in running state via SNMP.

#    Copyright (C) 2017-2019 rsmuc <rsmuc@sec-dev.de>

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
import health_monitoring_plugins.windowsservice

if __name__ == '__main__':
    # pylint: disable=C0103
    helper = health_monitoring_plugins.SnmpHelper()

    helper.parser.add_option('-s', '--service',
                             help="The name of the service you want to monitor "
                                  "(-s scan for scanning)",
                             dest="service", default='')
    helper.parser.add_option('-S', '--scan', dest='scan_flag', default=False, action="store_true",
                             help='Show all available services')

    helper.parse_arguments()

    sess = health_monitoring_plugins.SnmpSession(**helper.get_snmp_args())

    # The default return value should be always OK
    helper.status(ok)

    windowsservice = health_monitoring_plugins.windowsservice.Windowsservice(sess)

    # if no service is set, we will do a scan; or if scan_flag is set
    if helper.options.service == "" or \
            helper.options.service is None or \
            helper.options.scan_flag:
        # Device information
        # run_scan()
        windowsservice.run_scan(helper, sess)

    else:
        windowsservice.check_service(helper, sess)

    # Print out plugin information and exit nagios-style
    helper.exit()
