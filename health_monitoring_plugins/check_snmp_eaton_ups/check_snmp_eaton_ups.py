#!/usr/bin/env python
# check_snmp_apc_ups.py - Check a Eaton APC UPS health state via SNMP

# Copyright (C) 2016 rsmuc <rsmuc@mailbox.org>
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
# along with check_snmp_raritan.py.  If not, see <http://www.gnu.org/licenses/>.


# Import PluginHelper and some utility constants from the Plugins module
import sys
import os
import netsnmp
import pynag.Plugins

# snmpSessionBaseClass module with some common snmp functions
# reside under the plugins parent dir. So we have to add the plugin parent dir
# to the module search path.  
sys.path.insert(1, os.path.join(sys.path[0], os.pardir)) 
import snmpSessionBaseClass


def calc_frequency_from_snmpvalue(the_snmp_value):
    return int(the_snmp_value)/10

def calc_output_current_from_snmpvalue(the_snmp_value):
    return int(the_snmp_value)/10

def check_ups_seconds_on_battery(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.2.1.33.1.2.2.0
    MIB excerpt
    If the unit is on battery power, the elapsed time
    since the UPS last switched to battery power, or the
    time since the network management subsystem was last
    restarted, whichever is less.  Zero shall be returned
    if the unit is not on battery power.    
    """
    the_helper.add_metric(
        label=the_helper.options.type,
        value=the_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom="Seconds")
    
    the_helper.check_all_metrics()
    # if the_helper.status() is not pynag.Plugins.ok:
    the_helper.set_summary(
        "{} seconds already running on battery".format(the_snmp_value))


def check_ups_estimated_minutes_remaining(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.2.1.33.1.2.3.0
    MIB excerpt
    An estimate of the time to battery charge depletion
    under the present load conditions if the utility power
    is off and remains off, or if it were to be lost and
    remain off.
    """
    the_helper.add_metric(
        label=the_helper.options.type,
        value=the_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom="minutes")
    the_helper.check_all_metrics()
    the_helper.set_summary("Remaining runtime on battery is {} minutes".format(the_snmp_value))


def check_ups_input_frequency(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.2.1.33.1.3.3.1.2.1
    MIB excerpt
    The present input frequency.
    """
    a_frequency = calc_frequency_from_snmpvalue(the_snmp_value)
    the_helper.add_metric(
        label=the_helper.options.type,
        value=a_frequency,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='Hz')
    the_helper.check_all_metrics()
    the_helper.set_summary("Input Frequency is {} Hz".format(a_frequency))


def check_ups_input_voltage(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.2.1.33.1.3.3.1.3.1
    MIB excerpt
    The magnitude of the present input voltage.
    """
    the_helper.add_metric(
        label=the_helper.options.type,
        value=the_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='VAC')
    the_helper.check_all_metrics()
    the_helper.set_summary("Input Voltage is {} VAC".format(the_snmp_value))


def check_ups_output_voltage(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.2.1.33.1.4.4.1.2.1
    MIB excerpt
    The present output voltage.
    """
    the_helper.add_metric(
        label=the_helper.options.type,
        value=the_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='VAC')
    the_helper.check_all_metrics()
    the_helper.set_summary("Output Voltage is {} VAC".format(the_snmp_value))


def check_ups_output_current(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.2.1.33.1.4.4.1.3.1
    MIB excerpt
    The present output current.
    """
    
    a_current = calc_output_current_from_snmpvalue(the_snmp_value)
    the_helper.add_metric(
        label=the_helper.options.type,
        value=a_current,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='A')
    the_helper.check_all_metrics()
    the_helper.set_summary("Output Current is {} A".format(a_current))


def check_ups_output_power(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.2.1.33.1.4.4.1.4.1
    MIB excerpt
    The present output true power.
    """
    the_helper.add_metric(
        label=the_helper.options.type,
        value=the_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='W')

    the_helper.check_all_metrics()
    the_helper.set_summary("Output Power is {} W".format(the_snmp_value))


def check_ups_output_percent_load(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.2.1.33.1.4.4.1.5.1
    MIB excerpt
    The percentage of the UPS power capacity presently
    being used on this output line, i.e., the greater of
    the percent load of true power capacity and the
    percent load of VA.
    """
    the_helper.add_metric(
        label=the_helper.options.type,
        value=the_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='%')
    the_helper.check_all_metrics()
    the_helper.set_summary("Output Load is {} %".format(the_snmp_value))


def check_ups_alarms_present(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.2.1.33.1.6.1.0
    MIB excerpt
    The present number of active alarm conditions.
    """
    if the_snmp_value != '0':
        the_helper.add_status(pynag.Plugins.critical)
    else:
        the_helper.add_status(pynag.Plugins.ok)
    the_helper.set_summary("{} active alarms ".format(the_snmp_value))


def check_ups_test_results_summary(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.2.1.33.1.7.3.0
    MIB excerpt
    The results of the current or last UPS diagnostics
    test performed.  The values for donePass(1),
    doneWarning(2), and doneError(3) indicate that the
    test completed either successfully, with a warning, or
    with an error, respectively.  The value aborted(4) is
    returned for tests which are aborted by setting the
    value of upsTestId to upsTestAbortTestInProgress.
    Tests which have not yet concluded are indicated by
    inProgress(5).  The value noTestsInitiated(6)
    indicates that no previous test results are available,
    such as is the case when no tests have been run since
    the last reinitialization of the network management
    subsystem and the system has no provision for non-
    volatile storage of test results.
    
    Value List
    donePass (1)
    doneWarning (2)
    doneError (3)
    aborted (4)
    inProgress (5)
    noTestsInitiated (6)
    """
    snmp_test_result = {
        '1' : 'pass',
        '2' : 'warning',
        '3' : 'error',
        '4' : 'aborted',
        '5' : 'in progress',
        '6' : 'no test initiated'
        }
    
    a_test_result = snmp_test_result.get(the_snmp_value, 'unknown SNMP value')
    
    if (the_snmp_value == '1') or (the_snmp_value == '5') or (the_snmp_value == '6'):
        the_helper.add_status(pynag.Plugins.ok)
    elif (the_snmp_value == '2') or (the_snmp_value == '4'):
        the_helper.add_status(pynag.Plugins.warning)
    else:
        the_helper.add_status(pynag.Plugins.critical)

    the_helper.set_summary("Result of last UPS diagnostic test was {}".format(a_test_result))


def check_ups_test_results_detail(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.2.1.33.1.7.4.0
    MIB excerpt
    Additional information about upsTestResultsSummary.
    If no additional information available, a zero length
    string is returned.
    
    TODO Performance data does not make any sense here. How to handle this? 
    """
    
    the_helper.set_summary("Details of last UPS diagnostic test: {}".format(the_snmp_value))


def check_xups_bat_capacity(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.4.1.534.1.2.4.0
    MIB Excerpt
    Battery percent charge.
    """

    the_helper.add_metric(
        label=the_helper.options.type,
        value=a_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='%')
    
    the_helper.check_all_metrics()
    the_helper.set_summary("Remaining Battery Capacity {} %".format(the_snmp_value))


def check_xups_env_ambient_temp(the_session, the_helper, the_snmp_value, the_unit=1):
    """
    OID .1.3.6.1.4.1.534.1.6.1.0
    MIB Excerpt
    The reading of the ambient temperature in the vicinity of the 
    UPS or SNMP agent.
    """
    
    the_helper.add_metric(
        label=the_helper.options.type,
        value=the_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='degree')
    
    the_helper.check_all_metrics()
    the_helper.set_summary("Environment Temperature is {} degree".format(the_snmp_value))


def check_xups_env_remote_temp(the_session, the_helper, the_snmp_value, the_unit=1):
    """
    OID .1.3.6.1.4.1.534.1.6.5.0
    MIB Excerpt
    The reading of a remote temperature sensor connected to the  
    UPS or SNMP agent.
    """
    
    the_helper.add_metric(
        label=the_helper.options.type,
        value=the_snmp_value,
        warn=the_helper.options.warning,
        crit=the_helper.options.critical,
        uom='degree')
    
    the_helper.check_all_metrics()
    the_helper.set_summary("External Environment Temperature is {} degree".format(the_snmp_value))


def check_upsmg_battery_fault_battery(the_session, the_helper, the_snmp_value):
    """
    OID .1.3.6.1.4.1.705.1.5.9.0
    MIB Excerpt
    The battery fault status.
    Value List
    yes (1)
    no (2)
    """
    
    apc_states = {
        '1' : 'Battery is in fault state ',
        '2' : 'Battery is not in fault state '}
    a_state = apc_states.get(the_snmp_value, "Unknown battery state!")

    if (the_snmp_value == '2'):
        the_helper.add_status(pynag.Plugins.ok)
    else:
        the_helper.add_status(pynag.Plugins.critical)

    the_helper.set_summary(a_state)


def check_upsmg_battery_replacement(the_session, the_helper, the_snmp_value):
    """
    OID 1.3.6.1.4.1.705.1.5.11.0
    MIB Excerpt
    The UPS Battery to be replaced status.
    Value List
    yes (1)
    no (2)
    """
    
    apc_states = {
        '1' : 'Battery needs to be replaced ',
        '2' : 'Battery does not need to be replaced '}
    a_state = apc_states.get(the_snmp_value, "Unknown battery replacement state!")

    if (the_snmp_value == '2'):
        the_helper.add_status(pynag.Plugins.ok)
    else:
        the_helper.add_status(pynag.Plugins.critical)

    the_helper.set_summary(a_state)


def check_upsmg_battery_low_battery(the_session, the_helper, the_snmp_value):
    """
    OID 1.3.6.1.4.1.705.1.5.14.0
    MIB Excerpt
    The battery low status.
    Value List
    yes (1)
    no (2)
    """
    
    apc_states = {
        '1' : 'Battery is in low state ',
        '2' : 'Battery is not in low state '}
    a_state = apc_states.get(the_snmp_value, "Unknown battery low state!")

    if (the_snmp_value == '2'):
        the_helper.add_status(pynag.Plugins.ok)
    else:
        the_helper.add_status(pynag.Plugins.critical)

    the_helper.set_summary(a_state)



# Eaton OIDS
eaton_oid_ups_seconds_on_battery           = ".1.3.6.1.2.1.33.1.2.2.0"
eaton_oid_ups_estimated_minutes_remaining  = ".1.3.6.1.2.1.33.1.2.3.0"
eaton_oid_ups_input_frequency              = ".1.3.6.1.2.1.33.1.3.3.1.2.1"
eaton_oid_ups_input_voltage                = ".1.3.6.1.2.1.33.1.3.3.1.3.1"
eaton_oid_ups_output_voltage               = ".1.3.6.1.2.1.33.1.4.4.1.2.1"
eaton_oid_ups_output_current               = ".1.3.6.1.2.1.33.1.4.4.1.3.1"
eaton_oid_ups_output_power                 = ".1.3.6.1.2.1.33.1.4.4.1.4.1"
eaton_oid_ups_output_percent_load          = ".1.3.6.1.2.1.33.1.4.4.1.5.1"
eaton_oid_ups_alarms_present               = ".1.3.6.1.2.1.33.1.6.1.0"
eaton_oid_ups_test_results_summary         = ".1.3.6.1.2.1.33.1.7.3.0"
eaton_oid_ups_test_results_detail          = ".1.3.6.1.2.1.33.1.7.4.0"
eaton_oid_xups_bat_capacity                = ".1.3.6.1.4.1.534.1.2.4.0"
eaton_oid_xups_env_ambient_temp            = ".1.3.6.1.4.1.534.1.6.1.0"
eaton_oid_xups_env_remote_temp             = ".1.3.6.1.4.1.534.1.6.5.0"
eaton_oid_upsmg_battery_fault_battery      = ".1.3.6.1.4.1.705.1.5.9.0"
eaton_oid_upsmg_battery_replacement        = ".1.3.6.1.4.1.705.1.5.11.0"
eaton_oid_upsmg_battery_low_battery        = ".1.3.6.1.4.1.705.1.5.14.0"

# Define available check types for this plugin
# Keys are the allowed -t arguments for this script
# The etries define which OID to use for the SNMP get
# and which check function to call.
eaton_check_configs = {
    "ON_BATTERY"                        : {"oid" : eaton_oid_ups_seconds_on_battery,
                                           "check" : check_ups_seconds_on_battery},
    "REMAINING_BATTERY_TIME"            : {"oid" : eaton_oid_ups_estimated_minutes_remaining,
                                           "check" : check_ups_estimated_minutes_remaining},
    "INPUT_FREQUENCY"                   : {"oid" : eaton_oid_ups_input_frequency,
                                           "check" : check_ups_input_frequency},           
    "INPUT_VOLTAGE"                     : {"oid" : eaton_oid_ups_input_voltage,
                                           "check" : check_ups_input_voltage},             
    "OUTPUT_VOLTAGE"                    : {"oid" : eaton_oid_ups_output_voltage,
                                           "check" : check_ups_output_voltage},            
    "OUTPUT_CURRENT"                    : {"oid" : eaton_oid_ups_output_current,
                                           "check" : check_ups_output_current},            
    "OUTPUT_POWER"                      : {"oid" : eaton_oid_ups_output_power,
                                           "check" : check_ups_output_power},              
    "OUTPUT_LOAD"                       : {"oid" : eaton_oid_ups_output_percent_load,
                                           "check" : check_ups_output_percent_load},               
    "ALARMS"                            : {"oid" : eaton_oid_ups_alarms_present,
                                           "check" : check_ups_alarms_present},
    "BATTERY_TEST_SUMMARY"              : {"oid" : eaton_oid_ups_test_results_summary,
                                           "check" : check_ups_test_results_summary},          
    "BATTERY_TEST_DETAIL"               : {"oid" : eaton_oid_ups_test_results_detail,
                                           "check" : check_ups_test_results_detail,
                                           "allow_snmp_empty" : True},          
    "BATTERY_CAPACITY"                  : {"oid" : eaton_oid_xups_bat_capacity,
                                           "check" : check_xups_bat_capacity},
    "ENVIRONMENT_TEMPERATURE"           : {"oid" : eaton_oid_xups_env_ambient_temp,
                                           "check" : check_xups_env_ambient_temp},   
    "EXTERNAL_ENVIRONMENT_TEMPERATURE"  : {"oid" : eaton_oid_xups_env_remote_temp,
                                           "check" : check_xups_env_remote_temp},   
    "BATTERY_LOW_WARNING"               : {"oid" : eaton_oid_upsmg_battery_low_battery,
                                           "check" : check_upsmg_battery_low_battery},      
    "BATTERY_REPLACEMENT_WARNING"       : {"oid" : eaton_oid_upsmg_battery_replacement,
                                           "check" : check_upsmg_battery_replacement},      
    "BATTERY_FAULT_WARNING"             : {"oid" : eaton_oid_upsmg_battery_fault_battery,
                                           "check" : check_upsmg_battery_fault_battery}      
    }


def verify_type(the_type, the_helper):
    if not the_type:
        the_helper.exit(
            summary="Check type must be specified",
            exit_code=pynag.Plugins.UNKNOWN,
            perfdata='')
    elif a_helper.options.type not in eaton_check_configs:
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
            ", ".join(eaton_check_configs.keys())),
        type='str')
    a_helper.parser.add_option('-c', '--critical', dest='critical', help='Critical thresholds in Icinga range format.', type='str')
    a_helper.parser.add_option('-w', '--warning', dest='warning', help='Warning thresholds in Icinga range format.', type='str')
    
    a_helper.parse_arguments()
    
    return a_helper
    

if __name__ == "__main__":
    a_helper = setup_plugin_helper()

    snmpSessionBaseClass.verify_host(a_helper.options.hostname, a_helper)     
    verify_type(a_helper.options.type, a_helper)

    snmp_session = netsnmp.Session(
        Version=1,
        DestHost=a_helper.options.hostname,
        Community=a_helper.options.community)

    # The default return value should be always OK
    a_helper.status(pynag.Plugins.ok)

    eaton_check = eaton_check_configs[a_helper.options.type]["check"]
    eaton_oid = eaton_check_configs[a_helper.options.type]["oid"]
    allow_empty = eaton_check_configs[a_helper.options.type].get("allow_snmp_empty", False)
    
    a_snmp_value = snmpSessionBaseClass.get_data(snmp_session, eaton_oid, a_helper, allow_empty)
    eaton_check(snmp_session, a_helper, a_snmp_value)
    
    ## Print out plugin information and exit nagios-style
    a_helper.exit()
