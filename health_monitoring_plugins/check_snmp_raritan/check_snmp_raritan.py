#!/usr/bin/env python
# check_snmp_raritan.py - Check a Raritan Dominition PX PDU (Power Distribution Unit), the inlets, outlets and the connected sensors

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
import math
import netsnmp
sys.path.insert(1, os.path.join(sys.path[0], os.pardir)) 
from snmpSessionBaseClass import add_common_options, get_common_options, verify_host, get_data, walk_data
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown

# Create an instance of PluginHelper()
helper = PluginHelper()

# define the command line options
add_common_options(helper)
helper.parser.add_option('-t', help="The type you want to monitor (inlet, outlet, sensor)", default="inlet", dest="typ")
helper.parser.add_option('-i', help="The id of the outlet / sensor you want to monitor (1-99)", default="1", dest="id")
helper.parse_arguments()

# get the options
number = helper.options.id
typ = helper.options.typ
host, version, community = get_common_options(helper)

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
    0 : "open",
    1 : "closed",
    2 : "belowLowerCritical",
    3 : "belowLowerWarning",
    4 : "normal",
    5 : "aboveUpperWarning",
    6 : "aboveUpperCritical",
    7 : "on",
    8 : "off",
    9 : "detected",
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

units =  {
    -1: "",
    0 : "other",
    1 : "V",
    2 : "A",
    3 : "W",
    4 : "VA",
    5 : "Wh",
    6 : "Vh",
    7 : "C",
    8 : "Hz",
    9 : "%",
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

# OIDs for Inlet from PDU2-MIB
oid_inlet_value              = '.1.3.6.1.4.1.13742.6.5.2.3.1.4' # the value from the sensor (must be devided by the digit)
oid_inlet_unit               = '.1.3.6.1.4.1.13742.6.3.3.4.1.6' # the unit of the value
oid_inlet_digits             = '.1.3.6.1.4.1.13742.6.3.3.4.1.7' # the digit we need for the real_value
oid_inlet_state              = '.1.3.6.1.4.1.13742.6.5.2.3.1.3' # the state if this is ok or not ok
oid_inlet_warning_upper      = '.1.3.6.1.4.1.13742.6.3.3.4.1.24' # warning_upper_threhsold (must be divided by the digit)
oid_inlet_critical_upper     = '.1.3.6.1.4.1.13742.6.3.3.4.1.23' # critical_upper_threhold (must be divided by the digit)
oid_inlet_warning_lower      = '.1.3.6.1.4.1.13742.6.3.3.4.1.22' # warning_lower_threshold (must be divided by the digit)
oid_inlet_critical_lower     = '.1.3.6.1.4.1.13742.6.3.3.4.1.21' # critical_lower_threshold (must be divided by the digit)
    
#OIDs for the Sensors from PDU2-MIB    
oid_sensor_name             =   '.1.3.6.1.4.1.13742.6.3.6.3.1.4.1.'     + number    #Name
oid_sensor_state            =   '.1.3.6.1.4.1.13742.6.5.5.3.1.3.1.'     + number	#State
oid_sensor_unit             =   '.1.3.6.1.4.1.13742.6.3.6.3.1.16.1.'    + number	#Unit
oid_sensor_value            =   '.1.3.6.1.4.1.13742.6.5.5.3.1.4.1.'     + number	#Value
oid_sensor_digit            =   '.1.3.6.1.4.1.13742.6.3.6.3.1.17.1.'    + number	#Digits
oid_sensor_type             =   '.1.3.6.1.4.1.13742.6.3.6.3.1.2.1.'		+ number	#Type
oid_sensor_warning_upper    =   '.1.3.6.1.4.1.13742.6.3.6.3.1.34.1.'    + number    #Upper Warning Threshold
oid_sensor_critical_upper   =   '.1.3.6.1.4.1.13742.6.3.6.3.1.33.1.'    + number    #Upper Critical Threshold    
oid_sensor_warning_lower    =   '.1.3.6.1.4.1.13742.6.3.6.3.1.32.1.'    + number    #Lower Warning Threshold
oid_sensor_critical_lower   =   '.1.3.6.1.4.1.13742.6.3.6.3.1.31.1.'    + number    #Lower Critical Threshold    

# OIDs for the Outlets from PDU2-MIB
base_oid_outlet_name    = '.1.3.6.1.4.1.13742.6.3.5.3.1.3.1' 		# Name
base_oid_outlet_state   = '.1.3.6.1.4.1.13742.6.5.4.3.1.3.1' 		# Value
oid_outlet_name         = base_oid_outlet_name + "." + number           # here we add the id, to get the name
oid_outlet_state        = base_oid_outlet_state + "." + number + ".14"   # here we add the id, to get the state

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

def check_inlet(sess):
    """
    check the Inlets of Raritan PDUs
    """
    # walk the data
    inlet_values                = walk_data(sess, oid_inlet_value, helper)[0]
    inlet_units                 = walk_data(sess, oid_inlet_unit, helper)[0]
    inlet_digits                = walk_data(sess, oid_inlet_digits, helper)[0]
    inlet_states                = walk_data(sess, oid_inlet_state, helper)[0]
    inlet_warning_uppers        = walk_data(sess, oid_inlet_warning_upper, helper)[0]
    inlet_critical_uppers       = walk_data(sess, oid_inlet_critical_upper, helper)[0]
    inlet_critical_lowers       = walk_data(sess, oid_inlet_critical_lower, helper)[0]
    inlet_warning_lowers        = walk_data(sess, oid_inlet_warning_lower, helper)[0]

    # just print the summary, that the inlet sensors are checked
    helper.add_summary("Inlet")

    # all list must have the same length, if not something went wrong. that makes it easier and we need less loops    
    # translate the data in human readable units with help of the dicts
    for x in range(len(inlet_values)):   
        inlet_unit              = units[int(inlet_units[x])]
        inlet_digit             = inlet_digits[x]
        inlet_state             = states[int(inlet_states[x])]
        inlet_value             = real_value(inlet_values[x], inlet_digit)        
        inlet_warning_upper     = real_value(inlet_warning_uppers[x], inlet_digit)
        inlet_critical_upper    = real_value(inlet_critical_uppers[x], inlet_digit)
        inlet_warning_lower     = real_value(inlet_warning_lowers[x], inlet_digit)
        inlet_critical_lower    = real_value(inlet_critical_lowers[x], inlet_digit)
        
        if inlet_state != "normal":
            # we don't want to use the thresholds. we rely on the state value of the device
            helper.add_summary("%s %s is %s" % (inlet_value, inlet_unit, inlet_state))
            helper.status(critical)
                
        # we always want to see the values in the long output and in the perf data
        helper.add_summary("%s %s" % (inlet_value, inlet_unit))
        helper.add_long_output("%s %s: %s" % (inlet_value, inlet_unit, inlet_state))
        helper.add_metric("Sensor " + str(x), inlet_value, inlet_warning_lower +\
                          ":" + inlet_warning_upper, inlet_critical_lower + ":" +\
                          inlet_critical_upper, "", "", inlet_unit)
        
def check_outlet(sess):
    """
    check the status of the specified outlet
    """
    outlet_name                 = get_data(sess, oid_outlet_name, helper)
    outlet_state                = get_data(sess, oid_outlet_state, helper)
    outlet_real_state           = states[int(outlet_state)]
    
    # here we check if the outlet is powered on
    if outlet_real_state != "on":
        helper.status(critical)
    
    # print the status
    helper.add_summary("Outlet %s - '%s' is: %s" % (number, outlet_name, outlet_real_state.upper()))
    
def check_sensor(sess):
    """
    check the status of the specified sensor
    """

    sensor_name             = get_data(sess, oid_sensor_name, helper)
    sensor_state            = get_data(sess, oid_sensor_state, helper)
    sensor_state_string     = states[int(sensor_state)]
    sensor_unit             = "" # if it's a onOff Sensor or something like that, we need an empty string for the summary
    sensor_unit_string      = ""
    sensor_value            = ""
    sensor_digit            = ""
    real_sensor_value       = ""
    sensor_type             = get_data(sess, oid_sensor_type, helper)
    sensor_warning_upper    = ""
    sensor_critical_upper   = ""
    sensor_warning_lower    = ""
    sensor_critical_lower   = ""

    if int(sensor_type) not in [14, 16, 17, 18, 19, 20]:
        # for all sensors except these, we want to calculate the real value and show the metric.
        # 14: onOff
        # 16: vibration
        # 17: waterDetection
        # 18: smokeDetection
        # 19: binary
        # 20: contact
        sensor_unit                 = int(get_data(sess, oid_sensor_unit, helper))
        sensor_unit_string          = units[int(sensor_unit)]
        sensor_digit                = get_data(sess, oid_sensor_digit, helper)
        sensor_warning_upper        = get_data(sess, oid_sensor_warning_upper, helper)
        sensor_critical_upper       = get_data(sess, oid_sensor_critical_upper, helper)
        sensor_warning_lower        = get_data(sess, oid_sensor_warning_lower, helper)
        sensor_critical_lower       = get_data(sess, oid_sensor_critical_lower, helper)
        sensor_value                = int(get_data(sess, oid_sensor_value, helper))
        real_sensor_value           = real_value(sensor_value, sensor_digit)
        real_sensor_warning_upper   = real_value(sensor_warning_upper, sensor_digit)
        real_sensor_critical_upper  = real_value(sensor_critical_upper, sensor_digit)
        real_sensor_warning_lower   = real_value(sensor_warning_lower, sensor_digit)
        real_sensor_critical_lower  = real_value(sensor_critical_lower, sensor_digit)
        # metrics are only possible for these sensors
        helper.add_metric(sensor_name, real_sensor_value, real_sensor_warning_lower +\
                          ":" + real_sensor_warning_upper, real_sensor_critical_lower +\
                          ":" + real_sensor_critical_upper, "", "", sensor_unit_string)
    
    # "OK" state
    if sensor_state_string in ["closed", "normal", "on", "notDetected", "ok", "yes", "one", "two", "inSync"]:
        helper.status(ok)
    
    # "WARNING" state
    elif sensor_state_string in ["open", "belowLowerWarning", "aboveUpperWarning", "marginal", "standby"]:
        helper.status(warning)
    
    # "CRITICAL" state
    elif sensor_state_string in ["belowLowerCritical", "aboveUpperCritical", "off", "detected", "alarmed", "fail", "no", "outOfSync"]:
        helper.status(critical)
    
    # "UNKOWN" state    
    elif sensor_state_string in ["unavailable"]:
        helper.status(unknown)
    
    # received an undefined state    
    else:
        helper.exit(summary="Something went wrong - received undefined state", exit_code=unknown, perfdata='')

    # summary is shown for all sensors
    helper.add_summary("Sensor %s - '%s' %s%s is: %s" % (number, sensor_name, real_sensor_value, sensor_unit_string, sensor_state_string))
    

if __name__ == "__main__":
       
    # verify that a hostname is set
    verify_host(host, helper)

    sess = netsnmp.Session(Version=version, DestHost=host, Community=community)

    # The default return value should be always OK
    helper.status(ok)
    
    ######
    ## here we check the inlet
    ######
    if typ.lower() == "inlet":
        check_inlet(sess)
    
    ######
    # here we check the outlets
    ######
    
    if typ.lower() == "outlet":
        check_outlet(sess)

    #######
    # here we check the sensors
    #######
        
    if typ.lower() == "sensor":
        check_sensor(sess)
        
    ## Print out plugin information and exit nagios-style
    helper.exit()
