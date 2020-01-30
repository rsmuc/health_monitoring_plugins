"""
Module for check_snmp_idrac
"""

#    Copyright (C) 2018-2019 rsmuc <rsmuc@sec-dev.de>

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

from pynag.Plugins import unknown, warning, critical, ok

# required OIDS from IDRAC-MIB-SMIv2

DEVICE_INFORMATION_OIDS = {
    "oid_host_name": '.1.3.6.1.2.1.1.5.0',
    "oid_product_type": '.1.3.6.1.4.1.674.10892.5.4.300.10.1.9.1',
    "oid_service_tag": '.1.3.6.1.4.1.674.10892.5.4.300.10.1.11.1'
}

DEVICE_GLOBAL_OIDS = {
    "oid_global_system": '.1.3.6.1.4.1.674.10892.5.2.1.0',
    "oid_system_lcd": '.1.3.6.1.4.1.674.10892.5.2.2.0',
    "oid_global_storage": '.1.3.6.1.4.1.674.10892.5.2.3.0',
    "oid_system_power": '.1.3.6.1.4.1.674.10892.5.2.4.0'
}

DEVICE_NAMES_OIDS = {

    "oid_power_unit_redundancy": '.1.3.6.1.4.1.674.10892.5.4.600.12.1.8',
    "oid_power_unit": '.1.3.6.1.4.1.674.10892.5.4.600.12.1.8',
    "oid_chassis_intrusion": '.1.3.6.1.4.1.674.10892.5.4.300.70.1.8',
    "oid_cooling_unit": '.1.3.6.1.4.1.674.10892.5.4.700.10.1.7',
    "oid_drive": '.1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.2',
    "oid_predictive_drive_status": '.1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.2'

}

DEVICE_STATES_OIDS = {

    "oid_power_unit_redundancy": '.1.3.6.1.4.1.674.10892.5.4.600.10.1.5',
    "oid_power_unit": '.1.3.6.1.4.1.674.10892.5.4.600.12.1.5',
    "oid_chassis_intrusion": '.1.3.6.1.4.1.674.10892.5.4.300.70.1.5',
    "oid_cooling_unit": '.1.3.6.1.4.1.674.10892.5.4.700.10.1.8',
    "oid_drive": '.1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.4',
    "oid_predictive_drive_status": '.1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.31'

}

DEVICE_TEMPERATURE_OIDS = {
    "oid_temperature_probe_status": '.1.3.6.1.4.1.674.10892.5.4.700.20.1.5',
    "oid_temperature_probe_reading": '.1.3.6.1.4.1.674.10892.5.4.700.20.1.6',
    "oid_temperature_probe_location": '.1.3.6.1.4.1.674.10892.5.4.700.20.1.8'
}

# States definitions
NORMAL_STATE = {
    1: 'other',
    2: 'unknown',
    3: 'ok',
    4: 'nonCritical',
    5: 'critical',
    6: 'nonRecoverable'
}

SYSTEM_POWER_STATE = {
    1: {
        "result": "other",
        "icingastatus": warning
    },
    2: {
        "result": "unknown",
        "icingastatus": unknown
    },
    3: {
        "result": "off",
        "icingastatus": critical
    },
    4: {
        "result": "on",
        "icingastatus": ok
    }
}

POWER_UNIT_REDUNDANCY_STATE = {
    1: {
        "result": "other",
        "icingastatus": warning
    },
    2: {
        "result": "unknown",
        "icingastatus": unknown
    },
    3: {
        "result": "full",
        "icingastatus": ok
    },
    4: {
        "result": "degraded",
        "icingastatus": critical
    },
    5: {
        "result": "lost",
        "icingastatus": critical
    },
    6: {
        "result": "notRedundant",
        "icingastatus": warning
    },
    7: {
        "result": "failed",
        "icingastatus": critical
    }
}

PROBE_STATE = {
    1: 'other',
    2: 'unknown',
    3: 'ok',
    4: 'nonCriticalUpper',
    5: 'criticalUpper',
    6: 'nonRecoverableUpper',
    7: 'nonCriticalLower',
    8: 'criticalLower',
    9: 'nonRecoverableLower',
    10: 'failed'
}

DISK_STATES = {
    1: {
        "result": "unknown",
        "icingastatus": unknown
    },
    2: {
        "result": "ready",
        "icingastatus": ok
    },
    3: {
        "result": "online",
        "icingastatus": ok
    },
    4: {
        "result": "foreign",
        "icingastatus": warning
    },
    5: {
        "result": "offline",
        "icingastatus": warning
    },
    6: {
        "result": "blocked",
        "icingastatus": warning
    },
    7: {
        "result": "failed",
        "icingastatus": critical
    },
    8: {
        "result": "non-raid",  # for example an internal m.2 will be shown as non-raid
        "icingastatus": ok
    },
    9: {
        "result": "removed",
        "icingastatus": critical
    }
}



PREDICTIVE_DISK_STATES = {
    0: {
        "result": "ok",
        "icingastatus": ok
    },

    1: {
        "result": "predictive failure - replace drive",
        "icingastatus": warning
    }

}





def normal_check(name, status, device_type):
    """if the status is "ok" in the NORMAL_STATE dict, return ok + string
    if the status is not "ok", return critical + string"""
    status_string = NORMAL_STATE.get(int(status), "unknown")

    if status_string == "ok":
        return ok, "{} '{}': {}".format(device_type, name, status_string)

    elif status_string == "unknown":
        return warning, "{} '{}': {}".format(device_type, name, status_string)

    # nonCritical is confusing - so we want to return "warning" as string and status
    elif status_string == "nonCritical":
        return warning, "{} '{}': {}".format(device_type, name, "warning")

    return critical, "{} '{}': {}".format(device_type, name, status_string)


def probe_check(name, status, device_type):
    """if the status is "ok" in the PROBE_STATE dict, return ok + string
    if the status is not "ok", return critical + string"""
    status_string = PROBE_STATE.get(int(status), "unknown")

    if status_string == "ok":
        return ok, "{} '{}': {}".format(device_type, name, status_string)

    if status_string == "unknown":
        return unknown, "{} '{}': {}".format(device_type, name, status_string)

    return critical, "{} '{}': {}".format(device_type, name, status_string)


class Idrac(object):
    """Class for check_meinberg_ntp"""

    def __init__(self, session):
        self.sess = session

    @staticmethod
    def add_device_information(helper, session):
        """ add general device information to summary """
        host_name_data = helper.get_snmp_value_or_exit(session, helper,
                                                       DEVICE_INFORMATION_OIDS['oid_host_name'])

        product_type_data = helper.get_snmp_value_or_exit(session, helper,
                                                          DEVICE_INFORMATION_OIDS[
                                                              'oid_product_type'])

        service_tag_data = helper.get_snmp_value_or_exit(session, helper,
                                                         DEVICE_INFORMATION_OIDS['oid_service_tag'])

        helper.add_summary('Name: {} - Typ: {} - Service tag: {}'.format(
            host_name_data, product_type_data, service_tag_data))

    def process_status(self, helper, session, check):
        """"process a single status"""
        snmp_result_status = helper.get_snmp_value_or_exit(session, helper,
                                                           DEVICE_GLOBAL_OIDS['oid_' + check])

        if check == "system_lcd":
            helper.update_status(helper, normal_check("global", snmp_result_status, "LCD status"))
        elif check == "global_storage":
            helper.update_status(helper,
                                 normal_check("global", snmp_result_status, "Storage status"))
        elif check == "system_power":
            helper.update_status(helper, self.check_system_power_status(snmp_result_status))
        elif check == "global_system":
            helper.update_status(helper,
                                 normal_check("global", snmp_result_status, "Device status"))

    def process_states(self, helper, session, check):
        """process status values from a table"""
        snmp_result_status = helper.walk_snmp_values_or_exit(session, helper,
                                                             DEVICE_STATES_OIDS["oid_" + check],
                                                             check)

        snmp_result_names = helper.walk_snmp_values_or_exit(session, helper,
                                                            DEVICE_NAMES_OIDS["oid_" + check],
                                                            check)

        for i, _result in enumerate(snmp_result_status):
            if check == "power_unit":
                helper.update_status(
                    helper,
                    normal_check(snmp_result_names[i], snmp_result_status[i], "Power unit"))
            elif check == "drive":
                helper.update_status(
                    helper,
                    self.check_drives(snmp_result_names[i], snmp_result_status[i]))
            elif check == "predictive_drive_status":
                helper.update_status(
                    helper,
                    self.check_predictive_drive_status(snmp_result_names[i], snmp_result_status[i]))
            elif check == "power_unit_redundancy":
                helper.update_status(
                    helper,
                    self.check_power_unit_redundancy(snmp_result_names[i], snmp_result_status[i]))
            elif check == "chassis_intrusion":
                helper.update_status(
                    helper,
                    normal_check(snmp_result_names[i], snmp_result_status[i],
                                 "Chassis intrusion sensor"))
            elif check == "cooling_unit":
                helper.update_status(
                    helper,
                    normal_check(snmp_result_names[i], snmp_result_status[i], "Cooling unit"))

    @staticmethod
    def process_temperature_sensors(helper, session):
        """process the temperature sensors"""
        snmp_result_temp_sensor_names = helper.walk_snmp_values_or_exit(
            session, helper,
            DEVICE_TEMPERATURE_OIDS['oid_temperature_probe_location'], "temperature sensors")
        snmp_result_temp_sensor_states = helper.walk_snmp_values_or_exit(
            session, helper,
            DEVICE_TEMPERATURE_OIDS['oid_temperature_probe_status'], "temperature sensors")
        snmp_result_temp_sensor_values = helper.walk_snmp_values_or_exit(
            session, helper,
            DEVICE_TEMPERATURE_OIDS['oid_temperature_probe_reading'], "temperature sensors")

        for i, _result in enumerate(snmp_result_temp_sensor_states):
            helper.update_status(
                helper, probe_check(snmp_result_temp_sensor_names[i],
                                    snmp_result_temp_sensor_states[i], "Temperature sensor"))

            if i < len(snmp_result_temp_sensor_values):
                helper.add_metric(label=snmp_result_temp_sensor_names[i] + " -Celsius-",
                                  value=float(snmp_result_temp_sensor_values[i]) / 10)

    @staticmethod
    def check_drives(drivename, drivestatus):
        """ check the drive status """
        return DISK_STATES[int(drivestatus)]["icingastatus"], "Drive '{}': {}".format(
            drivename, DISK_STATES[int(drivestatus)]["result"])

    @staticmethod
    def check_predictive_drive_status(drivename, drivestatus):
        """ check the predictive drive status """
        return PREDICTIVE_DISK_STATES[int(drivestatus)]["icingastatus"], "Predictve Drive Status '{}': {}".format(
            drivename, PREDICTIVE_DISK_STATES[int(drivestatus)]["result"])


    @staticmethod
    def check_system_power_status(power_state):
        """ check the global system power state """
        return (SYSTEM_POWER_STATE[int(power_state)]["icingastatus"],
                "System power status: '{}'".format(SYSTEM_POWER_STATE[int(power_state)]["result"]))

    @staticmethod
    def check_power_unit_redundancy(power_unit_name_data, power_unit_redundancy_data):
        """ check the status of the power units """
        return (POWER_UNIT_REDUNDANCY_STATE[int(power_unit_redundancy_data)]["icingastatus"],
                "Power unit '{}' redundancy: {}".format(power_unit_name_data,
                                                        POWER_UNIT_REDUNDANCY_STATE[
                                                            int(power_unit_redundancy_data)]
                                                        ["result"]))
