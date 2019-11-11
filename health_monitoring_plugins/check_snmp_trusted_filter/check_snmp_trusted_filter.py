#!/usr/bin/env python
# check_snmp_trusted_filter.py - Check a trusted filter

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

import netsnmp
import pynag.Plugins
import health_monitoring_plugins.trustedfilter

if __name__ == "__main__":
    helper = health_monitoring_plugins.SnmpHelper()
    helper.parser.add_option('-s', '--secondhost', dest='secondhost', type='str',
                             help = "Enter a second host to be checked for ActivityState")
    helper.parse_arguments()
    helper.status(pynag.Plugins.ok)

    snmp_args = helper.get_snmp_args()
    snmp1 = health_monitoring_plugins.SnmpSession(**snmp_args)
    if helper.options.secondhost:
        snmp_args['DestHost'] = helper.options.secondhost
        snmp2 = health_monitoring_plugins.SnmpSession(**snmp_args)
    else:
        snmp2 = None

    trustedFilter = health_monitoring_plugins.trustedfilter.TrustedFilter(helper, snmp1, snmp2)
    trustedFilter.check()

    helper.exit()