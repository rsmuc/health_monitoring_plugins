"""
Module for check_snmp_idrac
"""
# Copyright (C) 2018 rsmuc <rsmuc@mailbox.org>

from pynag.Plugins import unknown, warning, critical, ok

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


def normal_check(name, status, device_type):
    """if the status is "ok" in the NORMAL_STATE dict, return ok + string
    if the status is not "ok", return critical + string"""
    status_string = NORMAL_STATE.get(int(status), "unknown")

    if status_string == "ok":
        return ok, "{} '{}': {}".format(device_type, name, status_string)

    elif status_string == "unknown":
        return unknown, "{} '{}': {}".format(device_type, name, status_string)

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
        self.oids = self.get_oids()

    @staticmethod
    def get_oids():
        """return the OIDs"""

        return {
            # from IDRAC-MIB-SMIv2
            "oid_host_name": '.1.3.6.1.2.1.1.5.0',
            "oid_product_type": '.1.3.6.1.4.1.674.10892.5.4.300.10.1.9.1',
            "oid_service_tag": '.1.3.6.1.4.1.674.10892.5.4.300.10.1.11.1',

            "oid_global_system": '.1.3.6.1.4.1.674.10892.5.2.1.0',
            "oid_system_lcd": '.1.3.6.1.4.1.674.10892.5.2.2.0',
            "oid_global_storage": '.1.3.6.1.4.1.674.10892.5.2.3.0',
            "oid_system_power": '.1.3.6.1.4.1.674.10892.5.2.4.0',

            "oid_power_unit_redundancy": '.1.3.6.1.4.1.674.10892.5.4.600.10.1.5',
            "oid_power_unit_name": '.1.3.6.1.4.1.674.10892.5.4.600.12.1.8',
            "oid_power_unit_status": '.1.3.6.1.4.1.674.10892.5.4.600.12.1.5',

            "oid_chassis_intrusion": '.1.3.6.1.4.1.674.10892.5.4.300.70.1.5',
            "oid_chassis_intrusion_location": '.1.3.6.1.4.1.674.10892.5.4.300.70.1.8',

            "oid_cooling_unit_name": '.1.3.6.1.4.1.674.10892.5.4.700.10.1.7',
            "oid_cooling_unit_status": '.1.3.6.1.4.1.674.10892.5.4.700.10.1.8',

            "oid_temperature_probe_status": '.1.3.6.1.4.1.674.10892.5.4.700.20.1.5',
            "oid_temperature_probe_reading": '.1.3.6.1.4.1.674.10892.5.4.700.20.1.6',
            "oid_temperature_probe_location": '.1.3.6.1.4.1.674.10892.5.4.700.20.1.8',

            "oid_voltage_probe_status": '.1.3.6.1.4.1.674.10892.5.4.600.20.1.5',
            "oid_voltage_probe_reading": '.1.3.6.1.4.1.674.10892.5.4.600.20.1.6',
            "oid_voltage_probe_location": '.1.3.6.1.4.1.674.10892.5.4.600.20.1.8',

            "oid_drive_names": '.1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.2',
            "oid_drive_status": '.1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.4'
        }

    def add_device_information(self, helper, session):
        """ add general device information to summary """
        host_name_data = helper.get_snmp_value(session, helper,
                                               self.oids['oid_host_name'])

        product_type_data = helper.get_snmp_value(session, helper,
                                                  self.oids['oid_product_type'])

        service_tag_data = helper.get_snmp_value(session, helper,
                                                 self.oids['oid_service_tag'])

        helper.add_summary('Name: {} - Typ: {} - Service tag: {}'.format(
            host_name_data, product_type_data, service_tag_data))

    def process_system_status(self, helper, session):
        """ process the global system status """
        snmp_result_system_status = helper.get_snmp_value(session, helper,
                                                          self.oids['oid_global_system'])
        helper.update_status(
            helper, self.check_system_status(snmp_result_system_status))

    def process_power_status(self, helper, session):
        """ process the power status """
        snmp_result_power_status = helper.get_snmp_value(session, helper,
                                                         self.oids['oid_system_power'])
        helper.update_status(
            helper, self.check_system_power_status(snmp_result_power_status))

    def process_storage_status(self, helper, session):
        """ process the storage status """
        snmp_result_storage_status = helper.get_snmp_value(session, helper, self.oids[
            'oid_global_storage'])
        helper.update_status(
            helper, self.check_system_storage_status(snmp_result_storage_status))

    def process_lcd_status(self, helper, session):
        """"process the lcd status"""
        snmp_result_lcd_status = helper.get_snmp_value(session, helper, self.oids[
            'oid_global_system'])
        helper.update_status(
            helper, self.check_system_lcd_status(snmp_result_lcd_status))

    def process_disk_states(self, helper, session):
        """ process the disks """
        snmp_result_drive_status = helper.walk_snmp_values(session, helper,
                                                           self.oids['oid_drive_status'],
                                                           "disk status")
        snmp_result_drive_names = helper.walk_snmp_values(session, helper,
                                                          self.oids['oid_drive_names'],
                                                          "disk status")
        for i, _result in enumerate(snmp_result_drive_status):
            helper.update_status(
                helper, self.check_drives(snmp_result_drive_names[i],
                                          snmp_result_drive_status[i]))

    def process_power_unit_states(self, helper, session):
        """process the power units"""
        snmp_result_power_status = helper.walk_snmp_values(session, helper,
                                                           self.oids['oid_power_unit_status'],
                                                           "power unit status")
        snmp_result_power_names = helper.walk_snmp_values(session, helper,
                                                          self.oids['oid_power_unit_name'],
                                                          "power unit status")
        for i, _result in enumerate(snmp_result_power_status):
            helper.update_status(
                helper, self.check_power_units(snmp_result_power_names[i],
                                               snmp_result_power_status[i]))

    def process_power_redundancy_status(self, helper, session):
        """process the power redundancy status"""
        power_redundancy_status = helper.walk_snmp_values(
            session, helper, self.oids['oid_power_unit_redundancy'], "power redundancy status")
        power_names = helper.walk_snmp_values(
            session, helper, self.oids['oid_power_unit_name'], "power redundancy status")

        for i, _result in enumerate(power_redundancy_status):
            helper.update_status(
                helper, self.check_power_unit_redundancy(power_names[i],
                                                         power_redundancy_status[i]))

    def process_chassis_intrusion(self, helper, session):
        """process the chassis intrusion sensor"""
        chassis_intrusion_status = helper.walk_snmp_values(
            session, helper, self.oids['oid_chassis_intrusion'], "intrusion status")
        chassis_location = helper.walk_snmp_values(
            session, helper, self.oids['oid_chassis_intrusion_location'], "intrusion status")

        for i, _result in enumerate(chassis_intrusion_status):
            helper.update_status(
                helper, self.check_chassis_intrusion(chassis_intrusion_status[i],
                                                     chassis_location[i]))

    def process_cooling_unit_states(self, helper, session):
        """process the cooling unit"""
        snmp_result_cooling_unit_states = helper.walk_snmp_values(
            session, helper, self.oids['oid_cooling_unit_status'], "cooling unit status")
        snmp_result_cooling_unit_names = helper.walk_snmp_values(
            session, helper, self.oids['oid_cooling_unit_name'], "cooling unit status")

        for i, _result in enumerate(snmp_result_cooling_unit_states):
            helper.update_status(
                helper, self.check_cooling_unit(snmp_result_cooling_unit_names[i],
                                                snmp_result_cooling_unit_states[i]))

    def process_temperature_sensors(self, helper, session):
        """process the temperature sensors"""
        snmp_result_temp_sensor_names = helper.walk_snmp_values(
            session, helper, self.oids['oid_temperature_probe_location'], "temperature sensors")
        snmp_result_temp_sensor_states = helper.walk_snmp_values(
            session, helper, self.oids['oid_temperature_probe_status'], "temperature sensors")
        snmp_result_temp_sensor_values = helper.walk_snmp_values(
            session, helper, self.oids['oid_temperature_probe_reading'], "temperature sensors")

        for i, _result in enumerate(snmp_result_temp_sensor_states):
            helper.update_status(
                helper, self.check_temperature_sensor(snmp_result_temp_sensor_names[i],
                                                      snmp_result_temp_sensor_states[i]))
            if i < len(snmp_result_temp_sensor_values):
                helper.add_metric(label=snmp_result_temp_sensor_names[i] + " -Celsius-",
                                  value=float(snmp_result_temp_sensor_values[i]) / 10)

    @staticmethod
    def check_drives(drivename, drivestatus):
        """ check the drive status """

        return DISK_STATES[int(drivestatus)]["icingastatus"], "Drive '{}': {}".format(
            drivename, DISK_STATES[int(drivestatus)]["result"])

    @staticmethod
    def check_system_status(lcd_status):
        """ check the global system status """
        return normal_check("global", lcd_status, "Device status")

    @staticmethod
    def check_system_lcd_status(lcd_status):
        """ check the LCD front panel status """
        return normal_check("global", lcd_status, "LCD status")

    @staticmethod
    def check_system_storage_status(storage_status):
        """ check the storage status """
        return normal_check("global", storage_status, "Storage status")

    @staticmethod
    def check_system_power_status(power_state):
        """ check the global system power state """
        return SYSTEM_POWER_STATE[int(power_state)]["icingastatus"],\
               "System power status: '{}'".format(SYSTEM_POWER_STATE[int(power_state)]["result"])

    @staticmethod
    def check_power_unit_redundancy(power_unit_name_data, power_unit_redundancy_data):
        """ check the status of the power units """
        return POWER_UNIT_REDUNDANCY_STATE[int(power_unit_redundancy_data)]["icingastatus"], \
               "Power unit '{}' redundancy: {}".format(power_unit_name_data,
                POWER_UNIT_REDUNDANCY_STATE[int(power_unit_redundancy_data)]["result"])

    @staticmethod
    def check_power_units(power_unit_name_data, power_unit_status_data):
        """ check the status of the power units """
        return normal_check(power_unit_name_data, power_unit_status_data, "Power unit")

    @staticmethod
    def check_chassis_intrusion(chassis_intrusion_data, chassis_intrusion_location_data):
        """check the chassis intrusion"""
        return normal_check(chassis_intrusion_location_data, chassis_intrusion_data,
                            "Chassis intrusion sensor")

    @staticmethod
    def check_cooling_unit(cooling_unit_name_data, cooling_unit_status_data):
        """ check the status of the cooling units"""
        return normal_check(cooling_unit_name_data, cooling_unit_status_data, "Cooling unit")

    @staticmethod
    def check_temperature_sensor(temperature_sensor_name, temperature_sensor_status):
        """ check the temperature sensors """
        return probe_check(temperature_sensor_name, temperature_sensor_status, "Temperature sensor")

    @staticmethod
    def check_voltage_probe(voltage_probe_name, voltage_probe_status):
        """ check the voltage probe """
        return probe_check(voltage_probe_name, voltage_probe_status, "Voltage probe")
