#!/usr/bin/env python
# check_snmp_apc_ups.py - Check a Schneider APC UPS health state via SNMP

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
import sys
import os
import netsnmp
import pynag

# snmpSessionBaseClass module with some common snmp functions
# reside under the plugins parent dir. So we have to add the plugin parent dir
# to the module search path.  
sys.path.insert(1, os.path.join(sys.path[0], os.pardir))
import snmpSessionBaseClass

# import add_common_options
# from snmpSessionBaseClass import verify_host
# from snmpSessionBaseClass import get_data

# from pynag.Plugins import PluginHelper,ok,warning,critical,unknown

# APC OIDS
# Based on MIB powernet414 
apc_oid_base                        = ".1.3.6.1.4.1.318"
apc_oid_basic_battery_status        = apc_oid_base + ".1.1.1.2.1.1.0"
apc_oid_time_on_battery             = apc_oid_base + ".1.1.1.2.1.2.0"
apc_oid_battery_capacity            = apc_oid_base + ".1.1.1.2.2.1.0"
apc_oid_internal_temperature        = apc_oid_base + ".1.1.1.2.2.2.0"
apc_oid_runtime_remaining           = apc_oid_base + ".1.1.1.2.2.3.0"
apc_oid_battery_replace_indicator   = apc_oid_base + ".1.1.1.2.2.4.0"
apc_oid_input_voltage               = apc_oid_base + ".1.1.1.3.2.1.0"
apc_oid_input_frequency             = apc_oid_base + ".1.1.1.3.2.4.0"
apc_oid_output_voltage              = apc_oid_base + ".1.1.1.4.2.1.0"
apc_oid_output_load                 = apc_oid_base + ".1.1.1.4.2.3.0"
apc_oid_output_current              = apc_oid_base + ".1.1.1.4.2.4.0"
apc_oid_output_power                = apc_oid_base + ".1.1.1.4.2.8.0"
apc_oid_last_test_result            = apc_oid_base + ".1.1.1.7.2.3.0"
apc_oid_environment_temperature     = apc_oid_base + ".1.1.10.2.3.2.1.4.1.0"
apc_oid_environment_temperature_unit= apc_oid_base + ".1.1.10.2.3.2.1.5.0"


def calc_minutes_from_ticks(the_ticks):
    """
    Convert snmp TimeTicks type to minutes. A time tick is defined as 
    the hundreths of a second.
    """
    return float(the_ticks) / 6000.0


def check_basic_battery_status(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.4.1.318.1.1.1.2.1.1.0
    MIB Excerpt 
    The status of the UPS batteries.  A batteryLow(3) 
    value indicates the UPS will be unable to sustain the 
    current load, and its services will be lost if power is 
    not restored.  The amount of run time in reserve at the 
    time of low battery can be configured by the 
    upsAdvConfigLowBatteryRunTime.

    Value List
    unknown (1)
    batteryNormal (2)
    batteryLow (3)
    batteryInFaultCondition (4)
    """

    apc_battery_states = {
        '1' : 'unknown',
        '2' : 'batteryNormal',
        '3' : 'batteryLow',
        '4' : 'batteryInFaultCondition'
        }
    a_state = apc_battery_states.get(the_snmp_value, 'unknown')

    if the_snmp_value == '2':
        the_helper.add_status(pynag.Plugins.ok)
    elif the_snmp_value == '3':
        the_helper.add_status(pynag.Plugins.warning)
    else:
        the_helper.add_status(pynag.Plugins.critical)

    the_helper.set_summary("UPS batteries state is {}".format(a_state))


def check_time_on_battery(the_session, the_helper, the_snmp_value):
    """
    OID 1.3.6.1.4.1.318.1.1.1.2.1.2
    MIB excerpt
    The elapsed time since the UPS has switched to battery 
    power.    
    """
    a_minute_value = calc_minutes_from_ticks(the_snmp_value)
    the_helper.add_metric(
        label=the_helper.options.type,
        value=a_minute_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom="Minutes")

    the_helper.check_all_metrics()
    # if the_helper.status() is not pynag.Plugins.ok:
    the_helper.set_summary("{} minutes already running on battery".format(a_minute_value))


def check_battery_capacity(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.4.1.318.1.1.1.2.2.1.0
    MIB Excerpt
    The remaining battery capacity expressed in 
    percent of full capacity.
    """

    the_helper.add_metric(
        label=the_helper.options.type,
        value=a_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='%')

    the_helper.check_all_metrics()
    the_helper.set_summary("{} % remainig battery capacity ".format(the_snmp_value))


def check_internal_temperature(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.4.1.318.1.1.1.2.2.2.0
    MIB Excerpt
    The current internal UPS temperature expressed in 
    Celsius.
    """

    the_helper.add_metric(
        label=the_helper.options.type,
        value=the_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='C')

    the_helper.check_all_metrics()
    the_helper.set_summary("Current internal temperature is {} degree Celsius".format(the_snmp_value))


def check_runtime_remaining(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.4.1.318.1.1.1.2.2.3.0
    MIB excerpt
    The UPS battery run time remaining before battery 
    exhaustion.
    SNMP value is in TimeTicks aka hundredths of a second
    """
    a_minute_value = calc_minutes_from_ticks(the_snmp_value)
    the_helper.add_metric(
        label=the_helper.options.type,
        value=a_minute_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom="Minutes")
    the_helper.check_all_metrics()
    the_helper.set_summary("Remaining runtime on battery is {} minutes".format(a_minute_value))


def check_battery_replace_indicator(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.4.1.318.1.1.1.2.2.4.0
    MIB Excerpt
    Indicates whether the UPS batteries need replacing.
    Value List
    noBatteryNeedsReplacing (1)
    batteryNeedsReplacing (2)
    """

    apc_states = {
        '1' : 'Battery does not need to be replaced',
        '2' : 'Battery needs to be replaced!'}
    a_state = apc_states.get(the_snmp_value, "Unknown battery replacement state!")

    if the_snmp_value == '1':
        the_helper.add_status(pynag.Plugins.ok)
    else:
        the_helper.add_status(pynag.Plugins.critical)

    the_helper.set_summary(a_state)


def check_input_voltage(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.4.1.318.1.1.1.3.2.1.0
    MIB excerpt
    The current utility line voltage in VAC.
    """
    the_helper.add_metric(
        label=the_helper.options.type,
        value=the_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='VAC')
    the_helper.check_all_metrics()
    the_helper.set_summary("Input Voltage is {} VAC".format(the_snmp_value))


def check_input_frequency(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.4.1.318.1.1.1.3.2.4.0
    MIB excerpt
    The current input frequency to the UPS system in Hz.
    """
    the_helper.add_metric(
        label=the_helper.options.type,
        value=the_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='Hz')
    the_helper.check_all_metrics()
    the_helper.set_summary("Input Frequency is {} Hz".format(the_snmp_value))


def check_output_voltage(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.4.1.318.1.1.1.4.2.1.0
    MIB excerpt
    The output voltage of the UPS system in VAC.
    """
    the_helper.add_metric(
        label=the_helper.options.type,
        value=the_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='VAC')
    the_helper.check_all_metrics()
    the_helper.set_summary("Output voltage is {} VAC".format(the_snmp_value))


def check_output_load(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.4.1.318.1.1.1.4.2.3.0
    MIB excerpt
    The current UPS load expressed in percent 
    of rated capacity.
    """
    the_helper.add_metric(
        label=the_helper.options.type,
        value=the_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='%')
    the_helper.check_all_metrics()
    the_helper.set_summary("Output load is {} %%".format(the_snmp_value))


def check_output_current(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.4.1.318.1.1.1.4.2.4.0
    MIB excerpt
    The current in amperes drawn by the load on the UPS.
    """
    the_helper.add_metric(
        label=the_helper.options.type,
        value=the_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='A')
    the_helper.check_all_metrics()
    the_helper.set_summary("Output current is {} A".format(the_snmp_value))


def check_output_power(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.4.1.318.1.1.1.4.2.8
    MIB excerpt
    The total output active power of the UPS system in W.
    The total active power is the sum of phase 1, phase 2 and
    phase 3 power.
    """
    the_helper.add_metric(
        label=the_helper.options.type,
        value=the_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='W')

    the_helper.check_all_metrics()
    the_helper.set_summary("Output total power is {} W".format(the_snmp_value))


def check_last_test_result(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.4.1.318.1.1.1.7.2.3.0
    MIB excerpt
    The results of the last UPS diagnostics test performed.
    Value List
    ok (1)
    failed (2)
    invalidTest (3)
    testInProgress (4)    
    """
    snmp_test_result = {
        '1' : 'ok',
        '2' : 'failed',
        '3' : 'invalid test',
        '4' : 'test in progress'
        }

    a_test_result = snmp_test_result.get(the_snmp_value, 'unknown SNMP value')

    if (the_snmp_value == '1') or (the_snmp_value == '4'):
        the_helper.add_status(pynag.Plugins.ok)
    else:
        the_helper.add_status(pynag.Plugins.critical)

    the_helper.set_summary("Result of last UPS diagnostic test was {}".format(a_test_result))


def check_environment_temperature(the_session, the_helper, the_snmp_value, the_unit=1):
    """
    OID .1.3.6.1.4.1.318.1.1.10.2.3.2.1.4.1
    MIB Excerpt
    The current temperature reading from the probe displayed
    in the units shown in the 'iemStatusProbeTempUnits' OID
    (Celsius or Fahrenheit).

    Description of unit OID
    OID .1.3.6.1.4.1.318.1.1.10.2.3.2.1.5
    The temperature scale used to display the temperature
    thresholds of the probe, Celsius(1) or Fahrenheit(2).
    This setting is based on the system preferences
    configuration in the agent.    
    """

    a_snmp_unit = snmpSessionBaseClass.get_data(
        the_session,
        apc_oid_environment_temperature_unit,
        the_helper)
    snmp_units = {
        '1' : 'C',
        '2' : 'F'
        }
    a_unit = snmp_units.get(a_snmp_unit, 'UNKNOWN_UNIT')

    the_helper.add_metric(
        label=the_helper.options.type,
        value=the_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom=a_unit)

    the_helper.check_all_metrics()
    the_helper.set_summary("Current environmental temperature is {}{}".format(the_snmp_value, a_unit))


# Define available check types for this plugin
# Keys are the allowed -t arguments for this script
# The etries define which OID to use for the SNMP get
# and which check function to call.
apc_check_configs = {
    "BASIC_BATTERY_STATUS"      : {"oid" : apc_oid_basic_battery_status,
                                   "check" : check_basic_battery_status},
    "TIME_ON_BATTERY"           : {"oid" : apc_oid_time_on_battery,
                                   "check" : check_time_on_battery},
    "BATTERY_CAPACITY"          : {"oid" : apc_oid_battery_capacity,
                                   "check" : check_battery_capacity},
    "INTERNAL_TEMPERATURE"      : {"oid" : apc_oid_internal_temperature,
                                   "check" : check_internal_temperature},
    "RUNTIME_REMAINING"         : {"oid" : apc_oid_runtime_remaining,
                                   "check" : check_runtime_remaining},
    "BATTERY_REPLACE_INDICATOR" : {"oid" : apc_oid_battery_replace_indicator,
                                   "check" : check_battery_replace_indicator},
    "INPUT_VOLTAGE"             : {"oid" : apc_oid_input_voltage,
                                   "check" : check_input_voltage},
    "INPUT_FREQUENCY"           : {"oid" : apc_oid_input_frequency,
                                   "check" : check_input_frequency},
    "OUTPUT_VOLTAGE"            : {"oid" : apc_oid_output_voltage,
                                   "check" : check_output_voltage},
    "OUTPUT_LOAD"               : {"oid" : apc_oid_output_load,
                                   "check" : check_output_load},
    "OUTPUT_CURRENT"            : {"oid" : apc_oid_output_current,
                                   "check" : check_output_current},
    "OUTPUT_POWER"              : {"oid" : apc_oid_output_power,
                                   "check" : check_output_power},
    "LAST_TEST_RESULT"          : {"oid" : apc_oid_last_test_result,
                                   "check" : check_last_test_result},
    "ENVIRONMENT_TEMPERATURE"   : {"oid" : apc_oid_environment_temperature,
                                   "check" : check_environment_temperature}
    }


def verify_type(the_type, the_helper):
    if not the_type:
        the_helper.exit(
            summary="Check type must be specified",
            exit_code=pynag.Plugins.UNKNOWN,
            perfdata='')
    elif a_helper.options.type not in apc_check_configs:
        the_helper.exit(
            summary="Invalid check type {} specified".format(the_type),
            exit_code=pynag.Plugins.UNKNOWN,
            perfdata='')


def setup_plugin_helper():
    # Create an instance of PluginHelper()
    a_helper = pynag.Plugins.PluginHelper()

    # define the command line options
    snmpSessionBaseClass.add_common_options(a_helper)

    # Add all defined check types (dictionary keys) as help text 
    a_helper.parser.add_option('-t', '--type', dest='type',
        help = "Check type to execute. Available types are: {}".format(
            ", ".join(apc_check_configs.keys())),
        type='str')
    a_helper.parser.add_option('-c', '--critical', dest='critical', help='Critical thresholds in Icinga range format.', type='str')
    a_helper.parser.add_option('-w', '--warning', dest='warning', help='Warning thresholds in Icinga range format.', type='str')
    snmpSessionBaseClass.add_snmpv3_options(a_helper)

    a_helper.parse_arguments()

    return a_helper


if __name__ == "__main__":
    a_helper = setup_plugin_helper()

    secname, seclevel, authproto, authpass, privproto, privpass = a_helper.options.secname, \
                                                                  a_helper.options.seclevel, \
                                                                  a_helper.options.authproto, \
                                                                  a_helper.options.authpass, \
                                                                  a_helper.options.privproto, \
                                                                  a_helper.options.privpass

    host, version, community = snmpSessionBaseClass.get_common_options(a_helper)

    snmpSessionBaseClass.verify_host(host, a_helper)
    verify_type(a_helper.options.type, a_helper)

    snmp_session = netsnmp.Session(Version=version, DestHost=host, SecLevel=seclevel, SecName=secname, AuthProto=authproto,
                              AuthPass=authpass, PrivProto=privproto, PrivPass=privpass, Community=community)

    # The default return value should be always OK
    a_helper.status(pynag.Plugins.ok)

    apc_check = apc_check_configs[a_helper.options.type]["check"]
    apc_oid = apc_check_configs[a_helper.options.type]["oid"]
    a_snmp_value = snmpSessionBaseClass.get_data(snmp_session, apc_oid, a_helper)
    apc_check(snmp_session, a_helper, a_snmp_value)

    # Print out plugin information and exit nagios-style
    a_helper.exit()
