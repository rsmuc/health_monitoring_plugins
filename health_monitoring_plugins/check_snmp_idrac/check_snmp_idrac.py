#!/usr/bin/env python

# Copyright (C) 2016 - 2018 rsmuc <rsmuc@mailbox.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with check_snmp_idrac.py.  If not, see <http://www.gnu.org/licenses/>.

from pynag.Plugins import ok
import health_monitoring_plugins.idrac

if __name__ == '__main__':
    HELPER = health_monitoring_plugins.SnmpHelper()

    HELPER.parser.add_option('--noPowerRedundancy', help='Do not check powersupply redundancy',
                             default=True,
                             action='store_false', dest='no_pwr_redund')
    HELPER.parser.add_option('--no-system', help='Do not check the global system status',
                             default=True, action='store_false', dest='system')
    HELPER.parser.add_option('--no-power', help='Do not check the power status',
                             default=True, action='store_false', dest='power')
    HELPER.parser.add_option('--no-storage', help='Do not check the storage status',
                             default=True, action='store_false', dest='storage')
    HELPER.parser.add_option('--no-disks', help='Do not check the disks',
                             default=True, action='store_false', dest='disks')
    HELPER.parser.add_option('--no-lcd', help='Do not check the lcd status',
                             default=True, action='store_false', dest='lcd')
    HELPER.parser.add_option('--no-power_unit', help='Do not check the power unit',
                             default=True, action='store_false', dest='power_unit')
    HELPER.parser.add_option('--no-redundancy', help='Do not check the power unit redundancy',
                             default=True, action='store_false', dest='power_unit_redundancy')
    HELPER.parser.add_option('--no-intrusion', help='Do not check the intrusion sensor',
                             default=True, action='store_false', dest='intrusion')
    HELPER.parser.add_option('--no-cooling', help='Do not check the cooling unit',
                             default=True, action='store_false', dest='cooling_unit')
    HELPER.parser.add_option('--no-temperature', help='Do not check the temperature',
                             default=True, action='store_false', dest='temperature')


    HELPER.parse_arguments()

    # TODO: we need to increase the default timeout. the snmp session takes too long.
    if HELPER.options.timeout < 2000:
        HELPER.options.timeout = 2000

    SESS = health_monitoring_plugins.SnmpSession(**HELPER.get_snmp_args())

    # The default return value should be always OK
    HELPER.status(ok)

    IDRAC = health_monitoring_plugins.idrac.Idrac(SESS)

    # Device information
    IDRAC.add_device_information(HELPER, SESS)

    # SYSTEM STATUS
    if HELPER.options.system:
        IDRAC.process_system_status(HELPER, SESS)

    # SYSTEM POWER STATUS
    if HELPER.options.power:
        IDRAC.process_power_status(HELPER, SESS)

    # SYSTEM STORAGE STATUS
    if HELPER.options.storage:
        IDRAC.process_storage_status(HELPER, SESS)

    # LCD STATUS
    if HELPER.options.lcd:
        IDRAC.process_lcd_status(HELPER, SESS)

    # DISK STATES
    if HELPER.options.disks:
        IDRAC.process_disk_states(HELPER, SESS)

    # POWER UNIT Status
    if HELPER.options.power_unit:
        IDRAC.process_power_unit_states(HELPER, SESS)

    # POWER UNIT Redundancy Status
    if HELPER.options.power_unit_redundancy:
        IDRAC.process_power_redundancy_status(HELPER, SESS)

    # CHASSIS INTRUSION Status
    if HELPER.options.intrusion:
        IDRAC.process_chassis_intrusion(HELPER, SESS)

    # COOLING UNIT Status
    if HELPER.options.cooling_unit:
        IDRAC.process_cooling_unit_states(HELPER, SESS)

    # Temperature Sensors
    if HELPER.options.temperature:
        IDRAC.process_temperature_sensors(HELPER, SESS)

    # check all metrics we added
    HELPER.check_all_metrics()

    # Print out plugin information and exit nagios-style
    HELPER.exit()
