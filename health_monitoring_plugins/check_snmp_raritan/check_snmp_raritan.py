#!/usr/bin/python
# check_snmp_raritan.py - Check a Raritan Dominition PX PDU (Power Distribution Unit), the outlets and the connected sensors

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
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown
import netsnmp
import math

# these dicts / definitions we need to get human readable values  
names = {
    'C': 'Current',
    'V': 'Voltage',
    'c': 'Current',
    'v': 'Voltage',
    'P': 'Power',
    'p': 'Power',
    }

#cleanup: for the inlet we should read the available 
#sensors = {
#    0: "rmsCurrent",
#    1: "None",
#    2: "unbalancedCurrent",
#    3: "rmsVoltage", 
#    4: "activePower",
#    5: "apparentPower",
#    6: "powerFactor",
#    7: "activeEnergy",
#    8: "apparentEnergy"
#}
    
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

def get_data(host, version, community, oid):
    """
    function for snmpget
    """
    try:
        var = netsnmp.Varbind(oid)
        data = netsnmp.snmpget(var, Version=version, DestHost=host, Community=community)
        value = data[0]
    except:
        helper.exit(summary="SNMP connection to device failed %s %s" % (host, oid), exit_code=unknown, perfdata='')
    if not value:
        helper.exit(summary="SNMP connection to device failed %s %s" % (host, oid), exit_code=unknown, perfdata='')
    return value

def walk_data(host, version, community, oid):
    """
    function for snmpwalk
    """
    var = netsnmp.Varbind(oid)
    try:
        data = netsnmp.snmpwalk(var, Version=version, DestHost=host, Community=community)
    except:
        helper.exit(summary="SNMP connection to device failed %s %s" % (host, oid), exit_code=unknown, perfdata='')
    if not data:
        helper.exit(summary="SNMP connection to device failed %s %s" % (host, oid), exit_code=unknown, perfdata='')
    return data

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

def check_inlet(host, version, community):
    """
    check the Inlets of Raritan PDUs
    """
    # OIDs for Inlet from PDU2-MIB
    oid_inlet_value              = '.1.3.6.1.4.1.13742.6.5.2.3.1.4' # the value from the sensor (must be devided by the digit)
    oid_inlet_unit               = '.1.3.6.1.4.1.13742.6.3.3.4.1.6' # the unit of the value
    oid_inlet_digits             = '.1.3.6.1.4.1.13742.6.3.3.4.1.7' # the digit we need for the real_value
    oid_inlet_state              = '.1.3.6.1.4.1.13742.6.5.2.3.1.3' # the state if this is ok or not ok
    oid_inlet_warning_upper      = '.1.3.6.1.4.1.13742.6.3.3.4.1.24' # warning_upper_threhsold (must be divided by the digit)
    oid_inlet_critical_upper     = '.1.3.6.1.4.1.13742.6.3.3.4.1.23' # critical_upper_threhold (must be divided by the digit)
    oid_inlet_warning_lower      = '.1.3.6.1.4.1.13742.6.3.3.4.1.22' # warning_lower_threshold (must be divided by the digit)
    oid_inlet_critical_lower     = '.1.3.6.1.4.1.13742.6.3.3.4.1.21' # critical_lower_threshold (must be divided by the digit)

    # walk the data
    inlet_values                = walk_data(host, version, community, oid_inlet_value)
    inlet_units                 = walk_data(host, version, community, oid_inlet_unit)
    inlet_digits                = walk_data(host, version, community, oid_inlet_digits)
    inlet_states                = walk_data(host, version, community, oid_inlet_state)    
    inlet_warning_uppers        = walk_data(host, version, community, oid_inlet_warning_upper)    
    inlet_critical_uppers       = walk_data(host, version, community, oid_inlet_critical_upper)
    inlet_critical_lowers       = walk_data(host, version, community, oid_inlet_critical_lower)
    inlet_warning_lowers        = walk_data(host, version, community, oid_inlet_warning_lower)

    # just print the summary, that the inlet sensors are checked
    helper.add_summary("Inlet")

    # all list must have the same length, if not something went wrong. that makes it easier and we need less loops    
    # translate the data in human readable units with help of the dicts
    for x in range(len(inlet_values)):   
        inlet_sensor            = "" # sensors[int(inlet_sensors[x])]
        inlet_unit              = units[int(inlet_units[x])]
        inlet_digit             = inlet_digits[x]
        inlet_state             = states[int(inlet_states[x])]
        inlet_value             = real_value(inlet_values[x], inlet_digit)        
        inlet_warning_upper     = real_value(inlet_warning_uppers[x], inlet_digit)
        inlet_critical_upper    = real_value(inlet_critical_uppers[x], inlet_digit)
        inlet_warning_lower     = real_value(inlet_warning_lowers[x], inlet_digit)
        inlet_critical_lower    = real_value(inlet_critical_lowers[x], inlet_digit)
        
        if inlet_state == "belowLowerCritical" or inlet_state == "aboveUpperCritical":
            # we don't want to use the thresholds. we rely on the state value of the device
            helper.add_summary("%s %s is %s" % (inlet_value, inlet_unit, inlet_state))
            helper.status(critical)
        
        if inlet_state == "belowLowerWarning" or inlet_state == "aboveUpperWarning":
            helper.add_summary("%s %s is %s" % (inlet_value, inlet_unit, inlet_state))
            helper.status(warning)
        
        # TODO: we should also care about the other values. everything is critical
        # except normal
                
        # we always want to see the values in the long output and in the perf data
        helper.add_summary("%s %s" % (inlet_value, inlet_unit))
        helper.add_long_output("%s %s: %s" % (inlet_value, inlet_unit, inlet_state))
        helper.add_metric("Sensor " + str(x), inlet_value, inlet_warning_lower + ":" + inlet_warning_upper, inlet_critical_lower + ":" + inlet_critical_upper, "", "", inlet_unit)
        

def check_outlet(host, version, community):
    # here we need the id
    base_oid_outlet_name    = '.1.3.6.1.4.1.13742.6.3.5.3.1.3.1' 		# Name
    base_oid_outlet_state   = '.1.3.6.1.4.1.13742.6.5.4.3.1.3.1' 		# Value
    oid_outlet_name         = base_oid_outlet_name + "." + id           # here we add the id, to get the name
    oid_outlet_state        = base_oid_outlet_state + "." + id + ".14"   # here we add the id, to get the state

    # we just want to receive the status of one sensor
    outlet_name                 = get_data(host, version, community, oid_outlet_name)
    outlet_state                = get_data(host, version, community, oid_outlet_state)
    outlet_real_state           = states[int(outlet_state)]
    
    # here we check if the outlet is powered on
    # cleanup: don't use a string compare here to improve performance
    if outlet_real_state != "on":
        helper.status(critical)
    
        # print the status
    helper.add_summary("Outlet %s - '%s' is: %s" % (id, outlet_name, outlet_real_state.upper()))
    
def check_sensor(host, version, community):
    oid_sensor_name             =   '.1.3.6.1.4.1.13742.6.3.6.3.1.4.1.'     + id    #Name
    oid_sensor_state            =   '.1.3.6.1.4.1.13742.6.5.5.3.1.3.1.'     + id	#State
    oid_sensor_unit             =   '.1.3.6.1.4.1.13742.6.3.6.3.1.16.1.'    + id	#Unit
    oid_sensor_value            =   '.1.3.6.1.4.1.13742.6.5.5.3.1.4.1.'     + id	#Value
    oid_sensor_digit            =   '.1.3.6.1.4.1.13742.6.3.6.3.1.17.1.'    + id	#Digits
    oid_sensor_type             =   '.1.3.6.1.4.1.13742.6.3.6.3.1.2.1.'		+ id	#Type
    oid_sensor_warning_upper    =   '.1.3.6.1.4.1.13742.6.3.6.3.1.34.1.'    + id    #Upper Warning Threshold
    oid_sensor_critical_upper   =   '.1.3.6.1.4.1.13742.6.3.6.3.1.33.1.'    + id    #Upper Critical Threshold    
    oid_sensor_warning_lower    =   '.1.3.6.1.4.1.13742.6.3.6.3.1.32.1.'    + id    #Lower Warning Threshold
    oid_sensor_critical_lower   =   '.1.3.6.1.4.1.13742.6.3.6.3.1.31.1.'    + id    #Lower Critical Threshold    

    sensor_name             = get_data(host, version, community, oid_sensor_name)
    sensor_state            = get_data(host, version, community, oid_sensor_state)
    sensor_state_string     = states[int(sensor_state)]
    sensor_unit             = "" # if it's a onOff Sensor or something like that, we need an empty string for the summary
    sensor_unit_string      = ""
    sensor_value            = ""
    sensor_digit            = ""
    real_sensor_value       = ""
    sensor_type             = get_data(host, version, community, oid_sensor_type)
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
        sensor_unit                 = int(get_data(host, version, community, oid_sensor_unit))
        sensor_unit_string          = units[int(sensor_unit)]
        sensor_digit                = get_data(host, version, community, oid_sensor_digit)
        sensor_warning_upper        = get_data(host, version, community, oid_sensor_warning_upper)
        sensor_critical_upper       = get_data(host, version, community, oid_sensor_critical_upper)
        sensor_warning_lower        = get_data(host, version, community, oid_sensor_warning_lower)
        sensor_critical_lower       = get_data(host, version, community, oid_sensor_critical_lower)
        sensor_value                = int(get_data(host, version, community, oid_sensor_value))
        real_sensor_value           = real_value(sensor_value, sensor_digit)
        real_sensor_warning_upper   = real_value(sensor_warning_upper, sensor_digit)
        real_sensor_critical_upper  = real_value(sensor_critical_upper, sensor_digit)
        real_sensor_warning_lower   = real_value(sensor_warning_lower, sensor_digit)
        real_sensor_critical_lower  = real_value(sensor_critical_lower, sensor_digit)
        # metric are only possible for these sensors
        helper.add_metric(sensor_name, real_sensor_value, real_sensor_warning_lower + ":" + real_sensor_warning_upper, real_sensor_critical_lower + ":" + real_sensor_critical_upper, "", "", sensor_unit_string)
    
    if int(sensor_state) in [1, 4, 7, 10, 12, 15, 18, 19, 20]:
        # 1:    closed
        # 4:    normal
        # 7:    on
        # 10:   not detected
        # 12:   ok
        # 15:   yes
        # 18:   one
        # 19:   two
        # 20:   in sync
        helper.status(ok)
    elif int(sensor_state) in [0, 3, 5, 8, 13, 17]:
        # 0:    open
        # 3:    belowLowerWarning
        # 5:    aboveUpperWarning
        # 13:   marginal
        # 17:   standby
        helper.status(warning)
    elif int(sensor_state) in [2, 6, 9, 8, 11, 14, 16, 21]:
        # 2:    belowLowerCritical
        # 6:    aboveUpperCritical
        # 8:    off 
        # 9:    detected
        # 11:   alarmed
        # 14:   fail
        # 16:   no
        # 21:   outofsync (that should be critical)
        helper.status(critical)
    elif int(sensor_state) in [-1]:
        # -1:   unavailable
        helper.status(unknown)
    else:
        # something went wrong
        helper.exit(summary="Something went wrong", exit_code=unknown, perfdata='')

    # summary is shown for all sensors
    helper.add_summary("Sensor %s - '%s' %s%s is: %s" % (id, sensor_name, real_sensor_value, sensor_unit_string, sensor_state_string))
    

# Create an instance of PluginHelper()
helper = PluginHelper()

if __name__ == "__main__":
    
    # define the command line options
    helper.parser.add_option('-H', help="Hostname or ip address", dest="hostname")
    helper.parser.add_option('-C', '--community', dest='community', help='SNMP community of the SNMP service on target host.', default='public')
    helper.parser.add_option('-V', '--snmpversion', dest='version', help='SNMP version. (1 or 2)', default=2, type='int')
    helper.parser.add_option('-t', help="The type you want to monitor (inlet, outlet, sensor)", default="inlet", dest="typ")
    helper.parser.add_option('-i', help="The id of the outlet / sensor you want to monitor (1-99)", default="1", dest="id")
    helper.parse_arguments()
    
    # get the options
    id = helper.options.id
    typ = helper.options.typ
    host = helper.options.hostname
    version = helper.options.version
    community = helper.options.community
    
    # verify that a hostname is set
    if host == "" or host == None:
        helper.exit(summary="Hostname must be specified", exit_code=unknown, perfdata='')

    # The default return value should be always OK
    helper.status(ok)
    
    ######
    ## here we check the inlet
    ######
    if typ.lower() == "inlet":
        check_inlet(host, version, community)
    
    ######
    # here we check the outlets
    ######
    
    if typ.lower() == "outlet":
        check_outlet(host, version, community)

    #######
    # here we check the sensors
    #######
        
    if typ.lower() == "sensor":
        check_sensor(host, version, community)
        
    ## Print out plugin information and exit nagios-style
    helper.exit()
