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

# Import PluginHelper and some utility constants from the Plugins module
from __future__ import absolute_import, division, print_function
import health_monitoring_plugins.ilo
from pynag.Plugins import ok, unknown

if __name__ == '__main__':
    # pylint: disable=C0103
    helper = health_monitoring_plugins.SnmpHelper()

    # Define the command line options

    helper.parser.add_option('--drives', help='Amount of physical drives', dest='amount_drvs', type='int')
    helper.parser.add_option('--ps', help='Amount of connected power supplies',
                             dest='amount_pwr_sply', type='int')
    helper.parser.add_option('--fan', help='Amount of fans', dest='amount_fans', type='int')
    helper.parser.add_option('--scan', help='(obsolete)',
                             default=False, action='store_true', dest='scan_server')  # TODO
    helper.parser.add_option('--noStorage', help='Do not check global storage condition',
                             default=True, action='store_false', dest='no_storage')
    helper.parser.add_option('--noSystem', help='Do not check global system state',
                             default=True, action='store_false', dest='no_system')
    helper.parser.add_option('--noPowerSupply', help='Do not check global power supply condition',
                             default=True, action='store_false', dest='no_power_supply')
    helper.parser.add_option('--noPowerState', help='Do not check power state',
                             default=True, action='store_false', dest='no_power_state')
    helper.parser.add_option('--noTemp', help='Do not check Overall thermal environment condition',
                             default=True, action='store_false', dest='no_temp')
    helper.parser.add_option('--noTempSens', help='Do not check temperature sensor condition',
                             default=True, action='store_false', dest='no_temp_sens')
    helper.parser.add_option('--noDriveTemp', help='Do not check temperature sensor of the hard '
                                                   'drives', default=True, action='store_false',
                             dest='no_drive_sens')
    helper.parser.add_option('--noFan', help='Do not check global fan condition',
                             default=True, action='store_false', dest='no_fan')
    helper.parser.add_option('--noMemory', help='Do not check memory condition',
                             default=True, action='store_false', dest='no_mem')
    helper.parser.add_option('--noController', help='Do not check controller condition',
                             default=True, action='store_false', dest='no_ctrl')
    helper.parser.add_option('--noLogicalDrives', help='Do not check the logical drives',
                             default=True, action='store_false', dest='no_logical_drives')
    helper.parser.add_option('--noPowerRedundancy', help='Do not check powersupply redundancy',
                             default=True, action='store_false', dest='no_pwr_redund')

    helper.parse_arguments()

    sess = health_monitoring_plugins.SnmpSession(**helper.get_snmp_args())

    helper.status(ok)

    ilo = health_monitoring_plugins.ilo.ILo(sess)

    # Scan
    if helper.options.scan_server:
        helper.exit(summary="Not implemented", exit_code=unknown, perfdata='')
        # ilo.scan_ilo(helper, sess)

    # Add general Device information
    ilo.add_device_information(helper, sess)

    # Global system states:
    if helper.options.no_storage:
        ilo.process_status(helper, sess, "global_storage")
    if helper.options.no_system:
        ilo.process_status(helper, sess, "global_system")
    if helper.options.no_power_supply:
        ilo.process_status(helper, sess, "global_power_supply")
    if helper.options.no_power_state:
        ilo.process_status(helper, sess, "global_power_state")
    if helper.options.no_temp:
        ilo.process_status(helper, sess, "global_thermal_system")
        ilo.process_status(helper, sess, "global_temp_sensors")
    if helper.options.no_fan:
        ilo.process_status(helper, sess, "global_fans")
    if helper.options.no_mem:
        ilo.process_status(helper, sess, "global_mem")

    # Storage Controller States
    if helper.options.no_ctrl:
        ilo.process_storage_controllers(helper, sess)

    # Physical Drives
    if helper.options.amount_drvs == '' or helper.options.amount_drvs is None:
        helper.exit(summary="Amount of physical drives must be specified (--drives)",
                    exit_code=unknown,
                    perfdata='')

    elif helper.options.amount_drvs != 0:
        ilo.process_physical_drives(helper, sess)

    # Logical drives
    if helper.options.no_logical_drives:
        ilo.process_logical_drives(helper, sess)

    # Power supply
    if helper.options.amount_pwr_sply == '' or helper.options.amount_pwr_sply is None:
        helper.exit(summary="Amount of power supplies must be specified (--ps)", exit_code=unknown,
                    perfdata='')

    elif helper.options.amount_pwr_sply != 0:
        ilo.process_power_supplies(helper, sess)

    # Power redundancy
    if helper.options.no_pwr_redund:
        ilo.process_power_redundancy(helper, sess)

    # FANs
    if helper.options.amount_fans == '' or helper.options.amount_fans is None:
        helper.exit(summary="Amount of fans must be specified (--fan)", exit_code=unknown, perfdata='')

    elif helper.options.amount_fans != 0:
        ilo.process_fans(helper, sess)

    # Temperature sensors
    if helper.options.no_temp_sens:
        ilo.process_temperature_sensors(helper, sess)

    # check all metrics we added
    helper.check_all_metrics()

    # Print out plugin information and exit nagios-style
    helper.exit()



##### OLD



#
# # scan function. Show all Power supplies, fans and pyhsical drives
# def scan_ilo():
#     helper.status(critical)
#     ps_data = walk_data(sess, oid_ps, helper)[0]
#     fan_data = walk_data(sess, oid_fan, helper)[0]
#
#     # we don't receive a result, if no physical drives are available.
#     phy_drv_status = attempt_walk_data(sess, oid_phy_drv_status)[0]
#
#     helper.add_long_output('Available devices:')
#     helper.add_long_output('')
#
#     # show the physical drives
#     if phy_drv_status:
#         for x, data in enumerate(phy_drv_status, 1):
#             helper.add_long_output('Physical drive %d: %s' % (x, phy_drv_state[int(data)]))
#     else:
#         helper.add_long_output("No physical drives detected")
#     # add a empty line after the pyhsical drives
#     helper.add_long_output('')
#
#     # show the power supplies
#     for x, data in enumerate(ps_data, 1):
#         helper.add_long_output('Power supply %d: %s'  % (x, normal_state[int(data)]))
#     helper.add_long_output('')
#
#     # show the fans
#     for x, data in enumerate(fan_data, 1):
#         helper.add_long_output('Fan %d: %s'  % (x, normal_state[int(data)]))
#
#     helper.exit(exit_code=ok, perfdata='')
