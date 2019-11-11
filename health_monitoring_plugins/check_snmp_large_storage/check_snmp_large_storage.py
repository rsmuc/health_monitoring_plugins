#!/usr/bin/env python

# check_snmp_large_storage.py - Check the used / free disk space of a device via SNMP
# (using the HOST-RESOURCES-MIB hrStorageSize).

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
import health_monitoring_plugins.storage

if __name__ == '__main__':
    # pylint: disable=C0103
    helper = health_monitoring_plugins.SnmpHelper()

    helper.parser.add_option('-p', '--partition',
                             dest='partition',
                             help='The disk / partition you want to monitor',
                             type='str')
    helper.parser.add_option('-u', '--unit', dest="targetunit",
                             help="The unit you want to have (MB, GB, TB)", default="GB")
    helper.parser.add_option('-s', '--scan', dest='scan_flag', default=False, action="store_true",
                             help='Show all available storages')

    helper.parse_arguments()

    sess = health_monitoring_plugins.SnmpSession(**helper.get_snmp_args())

    # The default return value should be always OK
    helper.status(ok)

    storage = health_monitoring_plugins.storage.Storage(sess)

    # if no partition is set, we will do a scan; or if scan_flag is set
    if helper.options.partition == "" or \
            helper.options.partition is None or \
            helper.options.scan_flag:
        # Device information
        # run_scan()
        storage.run_scan(helper, sess)

    # the check for the defined partition
    else:
        storage.check_partition(helper, sess)

    helper.check_all_metrics()

    # Print out plugin information and exit nagios-style
    helper.exit()
