#!/usr/bin/env python
# snmp_cambium_ptp700.py - Monitor the Cambium PTP700 radio.

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

from pynag.Plugins import ok
import health_monitoring_plugins.cambium

if __name__ == "__main__":
    # pylint: disable=C0103
    helper = health_monitoring_plugins.SnmpHelper()
    #helper.parser.add_option('-m',
    #                         help="Version of the Firmware (v5 or NG) "
    #                              "(NG = MBG-LANTIME-NG-MIB.mib used in Firmware 6 and newer)",
    #                         dest="mibversion")
    helper.parse_arguments()
    sess = health_monitoring_plugins.SnmpSession(**helper.get_snmp_args())

    # The default return value should be always OK
    helper.status(ok)

    cambium = health_monitoring_plugins.cambium.PTP700(sess)

    # Connection status
    cambium.process_connection_status(helper, sess)

    # there is only the satellites metric, but we will check all available
    #helper.check_all_metrics()

    # Print out plugin information and exit nagios-style
    helper.exit()
