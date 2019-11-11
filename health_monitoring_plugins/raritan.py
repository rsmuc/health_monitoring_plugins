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

import math
import health_monitoring_plugins
from pynag.Plugins import ok, warning, critical, unknown

# these dicts / definitions we need to get human readable values
names = {
    'C': 'Current',
    'V': 'Voltage',
    'c': 'Current',
    'v': 'Voltage',
    'P': 'Power',
    'p': 'Power',
}

states = {
    -1: "unavailable",
    0: "open",
    1: "closed",
    2: "belowLowerCritical",
    3: "belowLowerWarning",
    4: "normal",
    5: "aboveUpperWarning",
    6: "aboveUpperCritical",
    7: "on",
    8: "off",
    9: "detected",
    10: "notDetected",
    11: "alarmed",
    12: "ok",
    13: "marginal",
    14: "fail",
    15: "yes",
    16: "no",
    17: "standby",
    18: "one",
    19: "two",
    20: "inSync",
    21: "outOfSync"
}

units = {
    -1: "",
    0: "other",
    1: "V",
    2: "A",
    3: "W",
    4: "VA",
    5: "Wh",
    6: "Vh",
    7: "C",
    8: "Hz",
    9: "%",
    10: "ms",
    11: "Pa",
    12: "psi",
    13: "g",
    14: "F",
    15: "feet",
    16: "inches",
    17: "cm",
    18: "meters",
    19: "rpm",
    20: "degrees",
}


def real_value(value, digit):
    """
        function to calculate the real value
        we need to devide the value by the digit
        e.g.
            value = 100
            digit = 2
            return: "1.0"
    """
    return str(float(value) / math.pow(10, float(digit)))


class Raritan(object):
    def __init__(self, session, number):
        self.number = number
        self.sess = session
        self.oids = self.make_oids(number)

    # OIDs from PDU2-MIB
    def make_oids(self, number):
        base_oid_outlet_name = '.1.3.6.1.4.1.13742.6.3.5.3.1.3.1'  # Name
        base_oid_outlet_state = '.1.3.6.1.4.1.13742.6.5.4.3.1.3.1'  # Value
        return {
            'oid_inlet_value': '.1.3.6.1.4.1.13742.6.5.2.3.1.4',
            # the value from the sensor (must be divided by the digit)
            'oid_inlet_unit': '.1.3.6.1.4.1.13742.6.3.3.4.1.6',  # the unit of the value
            'oid_inlet_digits': '.1.3.6.1.4.1.13742.6.3.3.4.1.7',
            # the digit we need for the real_value
            'oid_inlet_state': '.1.3.6.1.4.1.13742.6.5.2.3.1.3',
            # the state if this is ok or not ok
            'oid_inlet_warning_upper': '.1.3.6.1.4.1.13742.6.3.3.4.1.24',
            # warning_upper_threhsold (must be divided by the digit)
            'oid_inlet_critical_upper': '.1.3.6.1.4.1.13742.6.3.3.4.1.23',
            # critical_upper_threhold (must be divided by the digit)
            'oid_inlet_warning_lower': '.1.3.6.1.4.1.13742.6.3.3.4.1.22',
            # warning_lower_threshold (must be divided by the digit)
            'oid_inlet_critical_lower': '.1.3.6.1.4.1.13742.6.3.3.4.1.21',
            # critical_lower_threshold (must be divided by the digit)
            'oid_sensor_name': '.1.3.6.1.4.1.13742.6.3.6.3.1.4.1.' + number,  # Name
            'oid_sensor_state': '.1.3.6.1.4.1.13742.6.5.5.3.1.3.1.' + number,  # State
            'oid_sensor_unit': '.1.3.6.1.4.1.13742.6.3.6.3.1.16.1.' + number,  # Unit
            'oid_sensor_value': '.1.3.6.1.4.1.13742.6.5.5.3.1.4.1.' + number,  # Value
            'oid_sensor_digit': '.1.3.6.1.4.1.13742.6.3.6.3.1.17.1.' + number,  # Digits
            'oid_sensor_type': '.1.3.6.1.4.1.13742.6.3.6.3.1.2.1.' + number,  # Type
            'oid_sensor_warning_upper': '.1.3.6.1.4.1.13742.6.3.6.3.1.34.1.' + number,
            # Upper Warning Threshold
            'oid_sensor_critical_upper': '.1.3.6.1.4.1.13742.6.3.6.3.1.33.1.' + number,
            # Upper Critical Threshold
            'oid_sensor_warning_lower': '.1.3.6.1.4.1.13742.6.3.6.3.1.32.1.' + number,
            # Lower Warning Threshold
            'oid_sensor_critical_lower': '.1.3.6.1.4.1.13742.6.3.6.3.1.31.1.' + number,
            # Lower Critical Threshold
            'oid_outlet_name': base_oid_outlet_name + "." + number,
            # here we add the id, to get the name
            'oid_outlet_state': base_oid_outlet_state + "." + number + ".14"
            # here we add the id, to get the state
        }

    def check_inlet(self, helper):
        """
        check the Inlets of Raritan PDUs
        """
        # walk the data
        try:
            inlet_values = self.sess.walk_oid(self.oids['oid_inlet_value'])
            inlet_units = self.sess.walk_oid(self.oids['oid_inlet_unit'])
            inlet_digits = self.sess.walk_oid(self.oids['oid_inlet_digits'])
            inlet_states = self.sess.walk_oid(self.oids['oid_inlet_state'])
            inlet_warning_uppers = self.sess.walk_oid(self.oids['oid_inlet_warning_upper'])
            inlet_critical_uppers = self.sess.walk_oid(self.oids['oid_inlet_critical_upper'])
            inlet_critical_lowers = self.sess.walk_oid(self.oids['oid_inlet_critical_lower'])
            inlet_warning_lowers = self.sess.walk_oid(self.oids['oid_inlet_warning_lower'])
        except health_monitoring_plugins.SnmpException as e:
            helper.exit(summary=str(e), exit_code=unknown, perfdata='')

        # just print the summary, that the inlet sensors are checked
        helper.add_summary("Inlet")

        # all list must have the same length, if not something went wrong.
        # that makes it easier and we need less loops
        # translate the data in human readable units with help of the dicts
        for x in range(len(inlet_values)):
            inlet_unit = units[int(inlet_units[x].val)]
            inlet_digit = inlet_digits[x].val
            inlet_state = states[int(inlet_states[x].val)]
            inlet_value = real_value(inlet_values[x].val, inlet_digit)
            inlet_warning_upper = real_value(inlet_warning_uppers[x].val, inlet_digit)
            inlet_critical_upper = real_value(inlet_critical_uppers[x].val, inlet_digit)
            inlet_warning_lower = real_value(inlet_warning_lowers[x].val, inlet_digit)
            inlet_critical_lower = real_value(inlet_critical_lowers[x].val, inlet_digit)

            if inlet_state != "normal":
                # we don't want to use the thresholds. we rely on the state value of the device
                helper.add_summary("%s %s is %s" % (inlet_value, inlet_unit, inlet_state))
                helper.status(critical)

            # we always want to see the values in the long output and in the perf data
            helper.add_summary("%s %s" % (inlet_value, inlet_unit))
            helper.add_long_output("%s %s: %s" % (inlet_value, inlet_unit, inlet_state))
            helper.add_metric("Sensor " + str(x) + " -%s-" % inlet_unit, inlet_value,
                              inlet_warning_lower + \
                              ":" + inlet_warning_upper, inlet_critical_lower + ":" + \
                              inlet_critical_upper, "", "", "")

    def check_outlet(self, helper):
        """
        check the status of the specified outlet
        """
        outlet_real_state = ""
        outlet_state = None

        try:
            outlet_name, outlet_state = helper.get_snmp_values_or_exit(self.sess,
                                                                       helper,
                                                                       self.oids['oid_outlet_name'],
                                                                       self.oids[
                                                                           'oid_outlet_state'])

        except health_monitoring_plugins.SnmpException as e:
            helper.exit(summary=str(e), exit_code=unknown, perfdata='')

        if outlet_state is not None:
            outlet_real_state = states.get(int(outlet_state), "unknown")

        # here we check if the outlet is powered on
        if outlet_real_state != "on":
            helper.status(critical)

        # print the status
        helper.add_summary(
            "Outlet %s - '%s' is: %s" % (self.number, outlet_name, outlet_real_state.upper()))

    def check_sensor(self, helper):
        """
        check the status of the specified sensor
        """
        try:
            sensor_name, \
            sensor_state, \
            sensor_type = helper.get_snmp_values_or_exit(self.sess,
                                                         helper,
                                                         self.oids[
                                                             'oid_sensor_name'],
                                                         self.oids[
                                                             'oid_sensor_state'],
                                                         self.oids[
                                                             'oid_sensor_type'])
        except health_monitoring_plugins.SnmpException as e:
            helper.exit(summary=str(e), exit_code=unknown, perfdata='')

        try:
            sensor_state_string = states[int(sensor_state)]
        except KeyError as e:
            helper.exit(summary="Invalid sensor response " + sensor_state, exit_code=unknown,
                        perfdata='')
        sensor_unit = ""  # if it's a onOff Sensor or something like that,
        # we need an empty string for the summary
        sensor_unit_string = ""
        sensor_value = ""
        sensor_digit = ""
        real_sensor_value = ""
        sensor_warning_upper = ""
        sensor_critical_upper = ""
        sensor_warning_lower = ""
        sensor_critical_lower = ""

        if int(sensor_type) not in [14, 16, 17, 18, 19, 20]:
            # for all sensors except these, we want to calculate the real value and show the metric.
            # 14: onOff
            # 16: vibration
            # 17: waterDetection
            # 18: smokeDetection
            # 19: binary
            # 20: contact
            try:
                sensor_unit, \
                sensor_digit, \
                sensor_warning_upper, \
                sensor_critical_upper, \
                sensor_warning_lower, \
                sensor_critical_lower, \
                sensor_value = helper.get_snmp_values_or_exit(
                    self.sess, helper,
                    self.oids['oid_sensor_unit'], self.oids['oid_sensor_digit'],
                    self.oids['oid_sensor_warning_upper'], self.oids['oid_sensor_critical_upper'],
                    self.oids['oid_sensor_warning_lower'], self.oids['oid_sensor_critical_lower'],
                    self.oids['oid_sensor_value'])
            except health_monitoring_plugins.SnmpException as e:
                helper.exit(summary=str(e), exit_code=unknown, perfdata='')

            sensor_unit_string = units[int(sensor_unit)]
            real_sensor_value = real_value(int(sensor_value), sensor_digit)
            real_sensor_warning_upper = real_value(sensor_warning_upper, sensor_digit)
            real_sensor_critical_upper = real_value(sensor_critical_upper, sensor_digit)
            real_sensor_warning_lower = real_value(sensor_warning_lower, sensor_digit)
            real_sensor_critical_lower = real_value(sensor_critical_lower, sensor_digit)
            # metrics are only possible for these sensors
            helper.add_metric(sensor_name + " -%s- " % sensor_unit_string, real_sensor_value,
                              real_sensor_warning_lower + \
                              ":" + real_sensor_warning_upper, real_sensor_critical_lower + \
                              ":" + real_sensor_critical_upper, "", "", "")

        # "OK" state
        if sensor_state_string in ["closed", "normal", "on", "notDetected", "ok", "yes", "one",
                                   "two", "inSync"]:
            helper.status(ok)

        # "WARNING" state
        elif sensor_state_string in ["open", "belowLowerWarning", "aboveUpperWarning", "marginal",
                                     "standby"]:
            helper.status(warning)

        # "CRITICAL" state
        elif sensor_state_string in ["belowLowerCritical", "aboveUpperCritical", "off", "detected",
                                     "alarmed", "fail", "no", "outOfSync"]:
            helper.status(critical)

        # "UNKOWN" state
        elif sensor_state_string in ["unavailable"]:
            helper.status(unknown)

        # received an undefined state
        else:
            helper.exit(summary="Something went wrong - received undefined state",
                        exit_code=unknown, perfdata='')

        # summary is shown for all sensors
        helper.add_summary("Sensor %s - '%s' %s%s is: %s" % (
            self.number, sensor_name, real_sensor_value, sensor_unit_string, sensor_state_string))
