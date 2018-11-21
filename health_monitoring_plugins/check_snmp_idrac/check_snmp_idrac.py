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
    HELPER.parse_arguments()
    SESS = health_monitoring_plugins.SnmpSession(**HELPER.get_snmp_args())

    # The default return value should be always OK
    HELPER.status(ok)

    IDRAC = health_monitoring_plugins.idrac.Idrac(SESS)

    # Device information
    IDRAC.add_device_information(HELPER, SESS)

    # SYSTEM POWER STATUS
    SNMP_RESULT_SYSTEM_STATUS = HELPER.get_snmp_value(SESS, HELPER, IDRAC.oids['oid_global_system'])
    IDRAC.update_status(
        HELPER, IDRAC.check_system_status(SNMP_RESULT_SYSTEM_STATUS))

    # SYSTEM POWER STATUS
    SNMP_RESULT_POWER_STATUS = HELPER.get_snmp_value(SESS, HELPER, IDRAC.oids['oid_system_power'])
    IDRAC.update_status(
        HELPER, IDRAC.check_system_power_status(SNMP_RESULT_POWER_STATUS))

    # SYSTEM STORAGE STATUS
    SNMP_RESULT_STORAGE_STATUS = HELPER.get_snmp_value(SESS, HELPER, IDRAC.oids[
        'oid_global_storage'])
    IDRAC.update_status(
        HELPER, IDRAC.check_system_storage_status(SNMP_RESULT_STORAGE_STATUS))

    # LCD STATUS
    SNMP_RESULT_LCD_STATUS = HELPER.get_snmp_value(SESS, HELPER, IDRAC.oids[
        'oid_global_system'])
    IDRAC.update_status(
        HELPER, IDRAC.check_system_lcd_status(SNMP_RESULT_LCD_STATUS))

    # DISK STATES
    SNMP_RESULT_DRIVE_STATUS = HELPER.walk_snmp_values(SESS, HELPER,
                                                       IDRAC.oids['oid_drive_status'])
    SNMP_RESULT_DRIVE_NAMES = HELPER.walk_snmp_values(SESS, HELPER,
                                                      IDRAC.oids['oid_drive_names'])
    for i, result in enumerate(SNMP_RESULT_DRIVE_STATUS):
        IDRAC.update_status(
            HELPER, IDRAC.check_drives(SNMP_RESULT_DRIVE_NAMES[i],
                                       SNMP_RESULT_DRIVE_STATUS[i]))


    # POWER UNIT Status
    SNMP_RESULT_POWER_STATUS = HELPER.walk_snmp_values(SESS, HELPER,
                                                       IDRAC.oids['oid_power_unit_status'])
    SNMP_RESULT_POWER_NAMES = HELPER.walk_snmp_values(SESS, HELPER,
                                                      IDRAC.oids['oid_power_unit_name'])
    for i, result in enumerate(SNMP_RESULT_POWER_STATUS):
        IDRAC.update_status(
            HELPER, IDRAC.check_power_units(SNMP_RESULT_POWER_NAMES[i],
                                            SNMP_RESULT_POWER_STATUS[i]))

    # POWER UNIT Redundancy Status
    SNMP_RESULT_POWER_REDUNDANCY_STATUS = HELPER.walk_snmp_values(
        SESS, HELPER, IDRAC.oids['oid_power_unit_redundancy'])
    SNMP_RESULT_POWER_NAMES = HELPER.walk_snmp_values(
        SESS, HELPER, IDRAC.oids['oid_power_unit_name'])

    for i, result in enumerate(SNMP_RESULT_POWER_REDUNDANCY_STATUS):
        IDRAC.update_status(
            HELPER, IDRAC.check_power_unit_redundancy(SNMP_RESULT_POWER_NAMES[i],
                                                      SNMP_RESULT_POWER_REDUNDANCY_STATUS[i]))

    # CHASSIS INTRUSION Status
    SNMP_RESULT_CHASSIS_INTRUSION_STATUS = HELPER.walk_snmp_values(
        SESS, HELPER, IDRAC.oids['oid_chassis_intrusion'])
    SNMP_RESULT_CHASSIS_LOCATION = HELPER.walk_snmp_values(
        SESS, HELPER, IDRAC.oids['oid_chassis_intrusion_location'])

    for i, result in enumerate(SNMP_RESULT_CHASSIS_INTRUSION_STATUS):
        IDRAC.update_status(
            HELPER, IDRAC.check_chassis_intrusion(SNMP_RESULT_CHASSIS_INTRUSION_STATUS[i],
                                                  SNMP_RESULT_CHASSIS_LOCATION[i]))

    # COOLING UNIT Status
    SNMP_RESULT_COOLING_UNIT_STATES = HELPER.walk_snmp_values(
        SESS, HELPER, IDRAC.oids['oid_cooling_unit_status'])
    SNMP_RESULT_COOLING_UNIT_NAMES = HELPER.walk_snmp_values(
        SESS, HELPER, IDRAC.oids['oid_cooling_unit_name'])

    for i, result in enumerate(SNMP_RESULT_COOLING_UNIT_STATES):
        IDRAC.update_status(
            HELPER, IDRAC.check_cooling_unit(SNMP_RESULT_COOLING_UNIT_NAMES[i],
                                             SNMP_RESULT_COOLING_UNIT_STATES[i]))

    # Temperature Sensors
    SNMP_RESULT_TEMP_SENSOR_NAMES = HELPER.walk_snmp_values(
        SESS, HELPER, IDRAC.oids['oid_temperature_probe_location'])
    SNMP_RESULT_TEMP_SENSOR_STATES = HELPER.walk_snmp_values(
        SESS, HELPER, IDRAC.oids['oid_temperature_probe_status'])
    SNMP_RESULT_TEMP_SENSOR_VALUES = HELPER.walk_snmp_values(
        SESS, HELPER, IDRAC.oids['oid_temperature_probe_reading'])

    for i, result in enumerate(SNMP_RESULT_TEMP_SENSOR_STATES):
        IDRAC.update_status(
            HELPER, IDRAC.check_temperature_sensor(SNMP_RESULT_TEMP_SENSOR_NAMES[i],
                                                   SNMP_RESULT_TEMP_SENSOR_STATES[i]))
        if i < len(SNMP_RESULT_TEMP_SENSOR_VALUES):
            HELPER.add_metric(label=SNMP_RESULT_TEMP_SENSOR_NAMES[i],
                              value=float(SNMP_RESULT_TEMP_SENSOR_VALUES[i]) / 10,
                              uom='Celsius')


    # TODO: add harddrives

    # # we need to refresh the session here ... i don't know why...
    #
    # SESS = health_monitoring_plugins.SnmpSession(**HELPER.get_snmp_args())
    # # Voltage Probe
    # SNMP_RESULT_VOLTAGE_PROBE_STATES = HELPER.walk_snmp_values(
    #     SESS, HELPER, IDRAC.oids['oid_voltage_probe_status'])
    #
    # SNMP_RESULT_VOLTAGE_PROBE_VALUES = HELPER.walk_snmp_values(
    #     SESS, HELPER, IDRAC.oids['oid_voltage_probe_reading'])
    #
    # SNMP_RESULT_VOLTAGE_PROBE_NAMES = HELPER.walk_snmp_values(
    #     SESS, HELPER, IDRAC.oids['oid_voltage_probe_location'])
    #
    # for i, result in enumerate(SNMP_RESULT_VOLTAGE_PROBE_STATES):
    #     IDRAC.update_status(
    #         HELPER, IDRAC.check_voltage_probe(SNMP_RESULT_VOLTAGE_PROBE_NAMES[i],
    #                                           SNMP_RESULT_VOLTAGE_PROBE_STATES[i]))
    #
    #     if i < len(SNMP_RESULT_VOLTAGE_PROBE_VALUES):
    #         HELPER.add_metric(label=SNMP_RESULT_VOLTAGE_PROBE_NAMES[i],
    #                           value=float(SNMP_RESULT_VOLTAGE_PROBE_VALUES[i]) / 1000,
    #                           uom='Volt')

    # check all metrics we added
    HELPER.check_all_metrics()

    # Print out plugin information and exit nagios-style
    HELPER.exit()
