#!/usr/bin/env python
# check_snmp_time2.py - Check

#    Copyright (C) 2016 Retakfual
#                  2016-2019 rsmuc <rsmuc@sec-dev.de>

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
from pynag.Plugins import ok
import health_monitoring_plugins.timesource

if __name__ == '__main__':
    # pylint: disable=C0103
    helper = health_monitoring_plugins.SnmpHelper()

    helper.parser.add_option('-o', '--tzoffset', dest='tzoffset',
                             default=0, type='int',
                             help='the local systems utc offset to the servers utc, in minutes ('
                                  'use only if your remote device is in a different timezone)')

    helper.parser.add_option('-l', '--localtime', dest='time_flag',
                             default=False, action="store_true",
                             help='force to use local time (only recommended if you have a non '
                                  'Windows OS remote device, that returns localtime and not utc)')

    helper.parse_arguments()

    sess = health_monitoring_plugins.SnmpSession(**helper.get_snmp_args())

    # The default return value should be always OK
    helper.status(ok)

    timesource = health_monitoring_plugins.timesource.Timesource(sess)

    timesource.check_time(helper, sess)

    helper.check_all_metrics()
    helper.exit()

