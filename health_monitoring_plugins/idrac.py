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
    1: 'other',
    2: 'unknown',
    3: 'off',
    4: 'on'
}

POWER_UNIT_REDUNDANCY_STATE = {
    1: 'other',
    2: 'unknown',
    3: 'full',
    4: 'degraded',
    5: 'lost',
    6: 'notRedundant',
    7: 'redundancyOffline'
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
# Todo: Check if a nested dict is the better solution
# DISK_STATES = {
#     1: {
#         "result": "unknown",
#         "icingastatus": unknown
#     },
#     2: {
#         "result": "ready",
#         "icingaastatus": ok
#     }
# }

DISK_STATES = {
    1: 'unknown',   # unknown
    2: 'ready',     # good
    3: 'online',    # good
    4: 'foreign',   # warning
    5: 'offline',   # warning
    6: 'blocked',   # warning
    7: 'failed',    # critical
    8: 'non-raid',  # warning
    9: 'removed'    # critical
}


def normal_check(name, status, device_type):
    """if the status is "ok" in the NORMAL_STATE dict, return ok + string
    if the status is not "ok", return critical + string"""
    status_string = NORMAL_STATE.get(int(status), "unknown")

    if status_string == "ok":
        return ok, "%s '%s': %s" % (device_type, name, status_string)

    elif status_string == "unknown":
        return unknown, "%s '%s': %s" % (device_type, name, status_string)

    return critical, "%s '%s': %s" % (device_type, name, status_string)


def probe_check(name, status, device_type):
    """if the status is "ok" in the PROBE_STATE dict, return ok + string
    if the status is not "ok", return critical + string"""
    status_string = PROBE_STATE.get(int(status), "unknown")

    if status_string == "ok":
        return ok, "%s '%s': %s" % (device_type, name, status_string)

    if status_string == "unknown":
        return unknown, "%s '%s': %s" % (device_type, name, status_string)

    return critical, "%s '%s': %s" % (device_type, name, status_string)


class Idrac(object):
    """Class for check_meinberg_ntp"""
    def __init__(self, session):
        self.sess = session
        self.oids = self.get_oids()
        #self.ntp_status = self.get_ntp_status(mibversion)
        #self.gps_mode = self.get_gps_mode(mibversion)

    @staticmethod
    def get_oids():
        """return the OIDs"""

        return {
            # from IDRAC-MIB-SMIv2
            "oid_user_assigned_name": '.1.3.6.1.4.1.674.10892.5.4.300.10.1.7.1',
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
            "oid_cooling_unit_status":  '.1.3.6.1.4.1.674.10892.5.4.700.10.1.8',

            "oid_temperature_probe_status": '.1.3.6.1.4.1.674.10892.5.4.700.20.1.5',
            "oid_temperature_probe_reading": '.1.3.6.1.4.1.674.10892.5.4.700.20.1.6',
            "oid_temperature_probe_location": '.1.3.6.1.4.1.674.10892.5.4.700.20.1.8',

            "oid_voltage_probe_status": '.1.3.6.1.4.1.674.10892.5.4.600.20.1.5',
            "oid_voltage_probe_reading": '.1.3.6.1.4.1.674.10892.5.4.600.20.1.6',
            "oid_voltage_probe_location": '.1.3.6.1.4.1.674.10892.5.4.600.20.1.8',

            "oid_drive_names": '.1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.2',
            "oid_drive_status": '.1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.4'
        }

    @staticmethod
    def update_status(helper, status):
        """ update the helper """
        if status:
            helper.status(status[0])

            # if the status is ok, add it to the long output
            if status[0] == 0:
                helper.add_long_output(status[1])
            # if the status is not ok, add it to the summary
            else:
                helper.add_summary(status[1])

    def add_device_information(self, helper, session):
        """ add general device information to summary """
        user_assigned_name_data = helper.get_snmp_value(session, helper,
                                                        self.oids['oid_user_assigned_name'])

        product_type_data = helper.get_snmp_value(session, helper,
                                                  self.oids['oid_product_type'])

        service_tag_data = helper.get_snmp_value(session, helper,
                                                 self.oids['oid_service_tag'])

        helper.add_summary('User assigned name: %s - Typ: %s - Service tag: %s' % (
            user_assigned_name_data, product_type_data, service_tag_data))

    @staticmethod
    def check_drives(drivename, drivestatus):

        status_string = DISK_STATES.get(int(drivestatus), "unknown")

        if status_string == "ready" or status_string == "online":
            return ok, "Drive '%s' status is': %s" % (drivename, status_string)

        elif status_string == "unknown":
            return unknown, "Drive '%s' status is': %s" % (drivename, status_string)

        elif status_string == "failed" or status_string == "removed":
            return critical, "Drive '%s' status is': %s" % (drivename, status_string)

        return warning, "Drive '%s' status is': %s" % (drivename, status_string)

        # Todo: the solution with the nested dict would look like that
        # return DISK_STATES[drivestate]["icingastatus"], "Drive is %s" % DISK_STATES[drivestate][
        #     "result"]

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
        status_string = SYSTEM_POWER_STATE.get(int(power_state), "unknown")

        if status_string == "on":
            return ok, "System power status': %s" % status_string

        if status_string == "unknown":
            return unknown, "System power status': %s" % status_string

        return critical, "System power status': %s" % status_string

    @staticmethod
    def check_power_unit_redundancy(power_unit_name_data, power_unit_redundancy_data):
        """ check the status of the power units """
        power_unit_redundancy_status = \
            POWER_UNIT_REDUNDANCY_STATE.get(int(power_unit_redundancy_data), "unknown")

        if power_unit_redundancy_status == "unknown":
            return unknown, "Power unit '%s' redundancy: %s" \
                   % (power_unit_name_data, power_unit_redundancy_status)

        elif power_unit_redundancy_status != "full":
            return critical, "Power unit '%s' redundancy: %s" \
                   % (power_unit_name_data, power_unit_redundancy_status)

        return ok, "Power unit '%s' redundancy: %s" \
               % (power_unit_name_data, power_unit_redundancy_status)

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
