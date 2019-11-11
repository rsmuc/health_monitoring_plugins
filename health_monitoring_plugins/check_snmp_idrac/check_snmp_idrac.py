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

from pynag.Plugins import ok
import health_monitoring_plugins.idrac

if __name__ == '__main__':
    # pylint: disable=C0103
    helper = health_monitoring_plugins.SnmpHelper()

    helper.parser.add_option('--no-system', help='Do not check the global system status',
                             default=True, action='store_false', dest='system')
    helper.parser.add_option('--no-power', help='Do not check the power status',
                             default=True, action='store_false', dest='power')
    helper.parser.add_option('--no-storage', help='Do not check the storage status',
                             default=True, action='store_false', dest='storage')
    helper.parser.add_option('--no-disks', help='Do not check the disks',
                             default=True, action='store_false', dest='disks')
    helper.parser.add_option('--no-predictive', help='Do not check the predictive status of the disks',
                             default=True, action='store_false', dest='predictive')
    helper.parser.add_option('--no-lcd', help='Do not check the lcd status',
                             default=True, action='store_false', dest='lcd')
    helper.parser.add_option('--no-power_unit', help='Do not check the power unit',
                             default=True, action='store_false', dest='power_unit')
    helper.parser.add_option('--no-redundancy', help='Do not check the power unit redundancy',
                             default=True, action='store_false', dest='power_unit_redundancy')
    helper.parser.add_option('--no-intrusion', help='Do not check the intrusion sensor',
                             default=True, action='store_false', dest='intrusion')
    helper.parser.add_option('--no-cooling', help='Do not check the cooling unit',
                             default=True, action='store_false', dest='cooling_unit')
    helper.parser.add_option('--no-temperature', help='Do not check the temperature',
                             default=True, action='store_false', dest='temperature')

    helper.parse_arguments()

    sess = health_monitoring_plugins.SnmpSession(**helper.get_snmp_args())

    # The default return value should be always OK
    helper.status(ok)

    idrac = health_monitoring_plugins.idrac.Idrac(sess)

    # Device information
    idrac.add_device_information(helper, sess)

    # SYSTEM STATUS
    if helper.options.system:
        idrac.process_status(helper, sess, "global_system")

    # SYSTEM POWER STATUS
    if helper.options.power:
        idrac.process_status(helper, sess, "system_power")

    # SYSTEM STORAGE STATUS
    if helper.options.storage:
        idrac.process_status(helper, sess, "global_storage")

    # LCD STATUS
    if helper.options.lcd:
        idrac.process_status(helper, sess, "system_lcd")

    # DISK STATES
    if helper.options.disks:
        idrac.process_states(helper, sess, "drive")

    # PREDICTIVE SMART DISK STATUS
    if helper.options.predictive:
        idrac.process_states(helper, sess, "predictive_drive_status")

    # POWER UNIT Status
    if helper.options.power_unit:
        idrac.process_states(helper, sess, "power_unit")

    # POWER UNIT Redundancy Status
    if helper.options.power_unit_redundancy:
        idrac.process_states(helper, sess, "power_unit_redundancy")

    # CHASSIS INTRUSION Status
    if helper.options.intrusion:
        idrac.process_states(helper, sess, "chassis_intrusion")

    # COOLING UNIT Status
    if helper.options.cooling_unit:
        idrac.process_states(helper, sess, "cooling_unit")

    # Temperature Sensors
    if helper.options.temperature:
        idrac.process_temperature_sensors(helper, sess)

    # check all metrics we added
    helper.check_all_metrics()

    # Print out plugin information and exit nagios-style
    helper.exit()
