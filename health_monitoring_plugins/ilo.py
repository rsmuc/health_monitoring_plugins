"""
Module for check_snmp_ilo4
"""

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

from __future__ import absolute_import, division, print_function
from pynag.Plugins import unknown, warning, critical, ok

DEVICE_INFORMATION_OIDS = {
    "oid_product_name": '.1.3.6.1.4.1.232.2.2.4.2.0',
    "oid_serial_number": '.1.3.6.1.4.1.232.2.2.2.1.0'
}

DEVICE_GLOBAL_OIDS = {
    "oid_global_storage": '.1.3.6.1.4.1.232.3.1.3.0',
    "oid_global_mem": '.1.3.6.1.4.1.232.6.2.14.4.0',
    "oid_global_system": '.1.3.6.1.4.1.232.6.1.3.0',
    "oid_global_power_supply": '.1.3.6.1.4.1.232.6.2.9.1.0',
    "oid_global_power_state": '.1.3.6.1.4.1.232.9.2.2.32.0',
    "oid_global_thermal_system": '.1.3.6.1.4.1.232.6.2.6.1.0',
    "oid_global_temp_sensors": '.1.3.6.1.4.1.232.6.2.6.3.0',
    "oid_global_fans": '.1.3.6.1.4.1.232.6.2.6.4.0',

}

DEVICE_STATES_OIDS = {

    "oid_controllers": '.1.3.6.1.4.1.232.3.2.2.1.1.6',
    "oid_power_supplies": '.1.3.6.1.4.1.232.6.2.9.3.1.4',
    "oid_ps_redundant": '.1.3.6.1.4.1.232.6.2.9.3.1.9',
    "oid_fan": '.1.3.6.1.4.1.232.6.2.6.7.1.9'

}

DRIVE_OIDS = {

    "oid_status": '.1.3.6.1.4.1.232.3.2.5.1.1.6',
    "oid_smart": '.1.3.6.1.4.1.232.3.2.5.1.1.57',
    "oid_temperature": '.1.3.6.1.4.1.232.3.2.5.1.1.70',
    "oid_temperature_threshold": '.1.3.6.1.4.1.232.3.2.5.1.1.71',
    "oid_logical_drive_status": '.1.3.6.1.4.1.232.3.2.3.1.1.4'

}

TEMPERATURE_OIDS = {

    "oid_env_temp": '.1.3.6.1.4.1.232.6.2.6.8.1.4',
    "oid_env_temp_thres": '.1.3.6.1.4.1.232.6.2.6.8.1.5'

}

# State definitions
NORMAL_STATE = {
    1: 'other',
    2: 'ok',
    3: 'degraded',
    4: 'failed'
}

SERVER_POWER_STATE = {
    1: 'unknown',
    2: 'poweredOff',
    3: 'poweredOn',
    4: 'insufficientPowerOrPowerOnDenied'
}

LOG_DRV_STATE = {
    1: 'other',
    2: 'ok',
    3: 'failed',
    4: 'unconfigured',
    5: 'recovering',
    6: 'readyForRebuild',
    7: 'rebuilding',
    8: 'wrongDrive',
    9: 'badConnect',
    10: 'overheating',
    11: 'shutdown',
    12: 'expanding',
    13: 'notAvailable',
    14: 'queuedForExpansion',
    15: 'multipathAccessDegraded',
    16: 'erasing',
    17: 'predictiveSpareRebuildReady',
    18: 'rapidParityInitInProgress',
    19: 'rapidParityInitPending',
    20: 'noAccessEncryptedNoCntlrKey',
    21: 'unencryptedToEncryptedInProgress',
    22: 'newLogDrvKeyRekeyInProgress',
    23: 'noAccessEncryptedCntlrEncryptnNotEnbld',
    24: 'unencryptedToEncryptedNotStarted',
    25: 'newLogDrvKeyRekeyRequestReceived'
}

PHY_DRV_STATES = {
    1: 'other',
    2: 'ok',
    3: 'failed',
    4: 'predictiveFailure',
    5: 'erasing',
    6: 'eraseDone',
    7: 'eraseQueued',
    8: 'ssdWearOut',
    9: 'notAuthenticated'
}

PHY_DRV_SMART_STATES = {
    1: 'other',
    2: 'ok',
    3: 'replaceDrive',
    4: 'replaceDriveSSDWearOut'
}

PS_REDUNDANT_STATE = {
    1: 'other',
    2: 'notRedundant',
    3: 'redundant'
}


def normal_check(name, status, device_type):
    """if the status is "ok" in the NORMAL_STATE dict, return ok + string
    if the status is not "ok", return critical + string"""
    status_string = NORMAL_STATE.get(int(status), "unknown")

    if status_string == "ok":
        return ok, "{} '{}': {}".format(device_type, name, status_string)

    elif status_string == "unknown":
        return warning, "{} '{}': {}".format(device_type, name, status_string)

    return critical, "{} '{}': {}".format(device_type, name, status_string)


def power_check(name, status, device_type):
    """if the status is "ok" in the NORMAL_STATE dict, return ok + string
    if the status is not "ok", return critical + string"""
    status_string = SERVER_POWER_STATE.get(int(status), "unknown")

    if status_string == "poweredOn":
        return ok, "{} '{}': {}".format(device_type, name, status_string)

    elif status_string == "unknown":
        return warning, "{} '{}': {}".format(device_type, name, status_string)

    return critical, "{} '{}': {}".format(device_type, name, status_string)


class ILo(object):
    """Class for check_meinberg_ntp"""

    def __init__(self, session):
        self.sess = session

    @staticmethod
    def add_device_information(helper, session):
        """ add general device information to summary """

        product_name = helper.get_snmp_value_or_exit(session, helper,
                                                     DEVICE_INFORMATION_OIDS['oid_product_name'])

        serial_number = helper.get_snmp_value_or_exit(session, helper,
                                                      DEVICE_INFORMATION_OIDS['oid_serial_number'])

        helper.add_summary('{} - Serial number: {}'.format(product_name, serial_number))

    # TODO: remove the if else shit
    def process_status(self, helper, session, check):
        """"process a single status"""
        snmp_result_status = helper.get_snmp_value_or_exit(session, helper,
                                                           DEVICE_GLOBAL_OIDS['oid_' + check])

        if check == "global_storage":
            helper.update_status(helper,
                                 normal_check("global", snmp_result_status, "Global storage"))

        elif check == "global_system":
            helper.update_status(helper,
                                 normal_check("global", snmp_result_status, "Global system"))

        elif check == "global_power_supply":
            helper.update_status(helper,
                                 normal_check("global", snmp_result_status, "Global power supply"))

        elif check == "global_power_state":
            helper.update_status(helper,
                                 power_check("global", snmp_result_status, "Global power state"))

        elif check == "global_thermal_system":
            helper.update_status(helper,
                                 normal_check("global", snmp_result_status,
                                              "Overall thermal environment"))

        elif check == "global_temp_sensors":
            helper.update_status(helper,
                                 normal_check("global", snmp_result_status, "Temperature sensors"))

        elif check == "global_fans":
            helper.update_status(helper,
                                 normal_check("global", snmp_result_status, "Fan(s)"))

        elif check == "global_mem":
            helper.update_status(helper,
                                 normal_check("global", snmp_result_status, "Memory"))

    @staticmethod
    def process_storage_controllers(helper, session):
        """ process the controller states """
        snmp_result_status = helper.walk_snmp_values_or_exit(session, helper,
                                                             DEVICE_STATES_OIDS["oid_controllers"],
                                                             "controllers")

        for i, _result in enumerate(snmp_result_status):
            helper.update_status(
                helper,
                normal_check(i, snmp_result_status[i], "Storage Controller"))

    @staticmethod
    def process_physical_drives(helper, session):

        drv_states = helper.walk_snmp_values_or_exit(session, helper,
                                                     DRIVE_OIDS["oid_status"],
                                                     "drive state")

        drv_smart_states = helper.walk_snmp_values_or_exit(session, helper,
                                                           DRIVE_OIDS["oid_smart"],
                                                           "smart state")

        drv_temps = helper.walk_snmp_values_or_exit(session, helper,
                                                    DRIVE_OIDS["oid_temperature"],
                                                    "drive temperature")

        drv_temps_thresh = helper.walk_snmp_values_or_exit(session, helper,
                                                           DRIVE_OIDS["oid_temperature_threshold"],
                                                           "drive temperature threshold")

        drv_count_ok = 0

        for x, data in enumerate(drv_states, 0):

            drv_status = PHY_DRV_STATES[int(drv_states[x])]
            drv_number = x + 1
            drv_smart_status = PHY_DRV_SMART_STATES[int(drv_smart_states[x])]
            drv_temp = int(drv_temps[x])
            drv_temp_thresh = drv_temps_thresh[x]

            # evaluate the drive status and the smart status
            if drv_status == "ok" and drv_smart_status == "ok":
                # the device is ok -> increase the number of ok devices
                drv_count_ok += 1
                status = ok

            else:
                # status is critical
                status = critical

            # if the status is ok, it will be shown in the long output. if the status is not ok
            # it will be shown in the summary
            helper.update_status(helper, [status, 'Physical drive {} status: {}'
                                 .format(drv_number, drv_status)])

            helper.update_status(helper, [status, 'Physical drive {} smart status: {}'
                                 .format(drv_number, drv_smart_status)])

            # evaluate the harddrive temperatures
            if helper.options.no_drive_sens:
                # OID returns -1 if the drive temperature (threshold)
                # cannot be calculated or if the controller does not
                # support reporting drive temperature threshold
                if drv_temp != -1 and int(drv_temp_thresh) != -1:
                    if drv_temp > int(drv_temp_thresh):
                        status = critical

                    helper.update_status(helper, [status, 'Physical drive {} '
                                                          'temperature: {} Celsius '
                                                          '(threshold: {} Celsius)'
                                         .format(drv_number, drv_temp, drv_temp_thresh)])

        # if the count of the found OK drives does not
        # match the amount of configured drives (--drives parameter)
        count_status = ok
        if helper.options.amount_drvs != drv_count_ok:
            count_status = critical

        helper.update_status(helper, [count_status, '{} physical drive(s) expected - '
                                                    '{} physical drive(s) in ok state!'
                             .format(str(helper.options.amount_drvs), drv_count_ok)])

    @staticmethod
    def process_logical_drives(helper, session):
        """check the logical drives"""

        logical_drv_states = helper.walk_snmp_values_or_exit(session, helper,
                                                             DRIVE_OIDS["oid_logical_drive_status"],
                                                             "logical drive state")

        icinga_status = ok

        for x, data in enumerate(logical_drv_states, 0):

            drv_status = LOG_DRV_STATE[int(logical_drv_states[x])]
            drv_number = x + 1

            if drv_status != "ok":
                icinga_status = critical

            helper.update_status(helper, [icinga_status, 'Logical drive {} {}'
                                 .format(drv_number, drv_status)])

    # TODO: Remove redundant code. There shall be one generic functions for checking the amount
    # TODO: and there should be one generic function for checking the status

    @staticmethod
    def process_power_supplies(helper, session):
        """check the power supplies"""

        status_power_supplies = helper.walk_snmp_values_or_exit(session, helper,
                                                                DEVICE_STATES_OIDS[
                                                                    "oid_power_supplies"],
                                                                "power supplies")

        ps_ok_count = 0
        icinga_status = ok
        count_status = ok

        for x, data in enumerate(status_power_supplies, 0):
            ps_status = NORMAL_STATE[int(status_power_supplies[x])]
            ps_number = x + 1

            if ps_status != "ok":
                icinga_status = critical
            else:
                ps_ok_count += 1

            helper.update_status(helper, [icinga_status, 'Power supply status {} {}'
                                 .format(ps_number, ps_status)])

        # check if the configured power supplies and power supplies in ok state are different
        if ps_ok_count != helper.options.amount_pwr_sply:
            count_status = critical

        helper.update_status(helper, [count_status, '{} power supplies expected - '
                                                    '{} power supplies ok'
                             .format(str(helper.options.amount_pwr_sply), ps_ok_count)])

    @staticmethod
    def process_fans(helper, session):
        """check the fans"""

        status_fans = helper.walk_snmp_values_or_exit(session, helper,
                                                      DEVICE_STATES_OIDS["oid_fan"],
                                                      "fans")

        fan_ok_count = 0
        icinga_status = ok
        count_status = ok

        for x, data in enumerate(status_fans, 0):
            fan_status = NORMAL_STATE[int(status_fans[x])]
            fan_number = x + 1

            if fan_status == "ok":
                fan_ok_count += 1

            helper.update_status(helper, [icinga_status, 'Fan {} {}'
                                 .format(fan_number, fan_status)])

        # check if the configured fans and fans in ok state are different
        if fan_ok_count != helper.options.amount_fans:
            count_status = critical

        helper.update_status(helper, [count_status, '{} fan(s) expected - '
                                                    '{} fan(s) ok'
                             .format(str(helper.options.amount_fans), fan_ok_count)])

    @staticmethod
    def process_power_redundancy(helper, session):
        """check the power redundancy"""

        redundancy_states = helper.walk_snmp_values_or_exit(session, helper,
                                                            DEVICE_STATES_OIDS["oid_ps_redundant"],
                                                            "power redundancy")

        icinga_status = ok

        for x, data in enumerate(redundancy_states, 0):
            redundancy_status = PS_REDUNDANT_STATE[int(redundancy_states[x])]
            redundancy_number = x + 1

            if redundancy_status != "redundant":
                icinga_status = critical

            helper.update_status(helper, [icinga_status, 'Power supply {} {}'
                                 .format(redundancy_number, redundancy_status)])

    @staticmethod
    def process_temperature_sensors(helper, session):

        temp_sensor_values = helper.walk_snmp_values_or_exit(session, helper,
                                                             TEMPERATURE_OIDS["oid_env_temp"],
                                                             "temperature sensor")

        temp_sensor_threholds = helper.walk_snmp_values_or_exit(session, helper,
                                                                TEMPERATURE_OIDS[
                                                                    "oid_env_temp_thres"],
                                                                "temperature threshold")

        values = zip(temp_sensor_values, temp_sensor_threholds)

        for count, data in enumerate(values, 1):
            temp_sensor_value = data[0]
            temp_sensor_threshold = data[1]
            sensor_status = ok

            # skip the check if -99 or 0 is in the value or threshold,
            # because these data we can not use
            if '-99' not in data and '0' not in data:
                if int(temp_sensor_value) > int(temp_sensor_threshold):
                    sensor_status = critical

                helper.update_status(helper, [sensor_status,
                                              'Temperature {}: {} Celsius (threshold: {} Celsius)'
                                     .format(count, temp_sensor_value, temp_sensor_threshold)])

                if count == 1:
                    helper.add_metric("Environment Temperature",
                                      temp_sensor_value, '', ":" + temp_sensor_threshold, "", "",
                                      "Celsius")
