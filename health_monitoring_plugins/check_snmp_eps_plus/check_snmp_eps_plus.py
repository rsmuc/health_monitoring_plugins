#!/usr/bin/env python

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

from pynag.Plugins import ok, unknown
import health_monitoring_plugins.eps_plus

if __name__ == '__main__':
    # pylint: disable=C0103
    helper = health_monitoring_plugins.SnmpHelper()

    helper.parser.add_option('--device', help='Select the device whose outlet shall be monitored '
                                              '(0 = master, 1 = first slave, 2 = second slave)',
                             default=None, type='str', dest='device')
    helper.parser.add_option('--outlet', help='Select the outlet which shall be monitored '
                                              '(0 = first outlet)',
                             default=None, type='str', dest='outlet')
    
    helper.parser.add_option('--expected', help='Define if On or Off shall be the OK sate '
                                              '(On, Off)',
                             default="On", dest='expected')
    
    helper.parser.add_option('--sensor', help='Select the sensor which shall be monitored '
                                              '(T1, T2, Tx, H1, H2, Hx)',
                             default=None, dest='sensor')
       

    helper.parse_arguments()
    
    sess = health_monitoring_plugins.SnmpSession(**helper.get_snmp_args())

    # The default return value should be always OK
    helper.status(ok)

    eps_plus = health_monitoring_plugins.eps_plus.EPSplus()

    # Outlet
    if helper.options.device is not None and helper.options.outlet is not None:
        eps_plus.check_outlet(helper, sess)

    # Sensor
    elif helper.options.sensor:
        eps_plus.check_sensor(helper, sess)

    else:
        helper.exit(summary="Please select --device and --outlet or --sensor",
                    exit_code=unknown, perfdata='')

    # check all metrics we added
    helper.check_all_metrics()

    # Print out plugin information and exit nagios-style
    helper.exit()
