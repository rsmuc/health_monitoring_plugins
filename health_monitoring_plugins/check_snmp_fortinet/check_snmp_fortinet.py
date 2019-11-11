#!/usr/bin/env python
# check_snmp_fortinet.py - Check a Fortinet WIFI controller

#    Copyright (C) 2017-2019 rsmuc <rsmuc@sec-dev.de>

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
helper.parser.add_option('-t', '--type', dest='type', default="ressources", help = "Check type to execute. Available types are: ressources, controller, accesspoints", type='str')
helper.parse_arguments()

# get the options
type = helper.options.type
host, version, community = get_common_options(helper)

# these dicts / definitions we need to get human readable values  
    
operational_states = {
    0 : "unknown",
    1 : "enabled",    
    2 : "disabled",
    3 : "unlicensed",
    4 : "enabled with 11nlic",
    5 : "power down"
}

availability_states = {
    1 : "powered off",
    2 : "offline",    
    3 : "online",
    4 : "failed",
    5 : "in test",
    6 : "not installed"
}

alarm_states = {
    1 : "no alarm",
    2 : "minor alarm",    
    3 : "major alarm",
    4 : "critical alarm"
}


# OIDs for Controller Ressources  
cpu_oid                         = '.1.3.6.1.4.1.15983.1.1.3.1.14.13.0' #  mwSystemResourceCurCpuUsagePercentage
memory_oid                      = '.1.3.6.1.4.1.15983.1.1.3.1.14.16.0' #  mwSystemResourceCurMemUsagePercentage
filesystem_oid                  = '.1.3.6.1.4.1.15983.1.1.3.1.14.10.0' #  mwSystemResourceRootFileSystemUsagePercentage

  
# OIDs for Controller Status
operational_oid                 = '.1.3.6.1.4.1.15983.1.1.4.1.1.21.0' #  mwWncVarsOperationalState
availability_oid                = '.1.3.6.1.4.1.15983.1.1.4.1.1.22.0' #  mwWncVarsAvailabilityStatus
alarm_oid                       = '.1.3.6.1.4.1.15983.1.1.4.1.1.23.0' #  mwWncVarsAlarmState  


# OIDs for AccessPoints
name_ap_oid                        = '.1.3.6.1.4.1.15983.1.1.4.2.1.1.2'  # mwApDescr
operational_ap_oid                 = '.1.3.6.1.4.1.15983.1.1.4.2.1.1.26' # mwApOperationalState
availability_ap_oid                = '.1.3.6.1.4.1.15983.1.1.4.2.1.1.27' # mwApAvailabilityStatus
alarm_ap_oid                       = '.1.3.6.1.4.1.15983.1.1.4.2.1.1.21' # mwApAlarmState  
#ip_ap_oid                           = '.1.3.6.1.4.1.15983.1.1.4.2.1.1.39' #  mwApIpAddress  # no result


def check_ressources(sess):
    """
    check the Ressources of the Fortinet Controller
    all thresholds are currently hard coded. should be fine.
    """
    # get the data
    cpu_value                    = get_data(sess, cpu_oid, helper)
    memory_value                 = get_data(sess, memory_oid, helper)
    filesystem_value             = get_data(sess, filesystem_oid, helper)

    helper.add_summary("Controller Status")
    helper.add_long_output("Controller Ressources - CPU: %s%%" % cpu_value)
    helper.add_metric("CPU", cpu_value, "0:90", "0:90", "", "", "%%")
    if int(cpu_value) > 90:
        helper.status(critical)
        helper.add_summary("Controller Ressources - CPU: %s%%" % cpu_value)

    helper.add_long_output("Memory: %s%%" % memory_value)
    helper.add_metric("Memory", memory_value, "0:90", "0:90", "", "", "%%")
    if int(memory_value) > 90:
        helper.add_summary("Memory: %s%%" % memory_value)
        helper.status(critical)
    
    helper.add_long_output("Filesystem: %s%%" % filesystem_value)
    helper.add_metric("Filesystem", filesystem_value, "0:90", "0:90", "", "", "%%")
    if int(filesystem_value) > 90:
        helper.add_summary("Filesystem: %s%%" % filesystem_value)
        helper.status(critical)
        
            
def check_controller(sess):
    """
    check the status of the controller
    """
    controller_operational             = get_data(sess, operational_oid, helper)
    controller_availability            = get_data(sess, availability_oid, helper)
    controller_alarm                   = get_data(sess, alarm_oid, helper)
    
    # Add summary
    helper.add_summary("Controller Status")

    # Add all states to the long output
    helper.add_long_output("Controller Operational State: %s" % operational_states[int(controller_operational)])
    helper.add_long_output("Controller Availability State: %s" % availability_states[int(controller_availability)])
    helper.add_long_output("Controller Alarm State: %s" % alarm_states[int(controller_alarm)])

    # Operational State
    if controller_operational != "1" and controller_operational != "4":
        helper.status(critical)
        helper.add_summary("Controller Operational State: %s" % operational_states[int(controller_operational)])

    # Avaiability State
    if controller_availability != "3":
        helper.status(critical)
        helper.add_summary("Controller Availability State: %s" % availability_states[int(controller_availability)])

    # Alarm State
    if controller_alarm == "2":
        helper.status(warning)
        helper.add_summary("Controller Alarm State: %s" % alarm_states[int(controller_alarm)])
    if controller_alarm == "3" or controller_alarm == "4":
        helper.status(critical)
        helper.add_summary("Controller Alarm State: %s" % alarm_states[int(controller_alarm)])
    
 
def check_accesspoints(sess):
    """
    check the status of all connected access points
    """
    ap_names              = walk_data(sess, name_ap_oid, helper)[0]
    ap_operationals       = walk_data(sess, operational_ap_oid, helper)[0]
    ap_availabilitys      = walk_data(sess, availability_ap_oid, helper)[0]
    ap_alarms             = walk_data(sess, alarm_ap_oid, helper)[0]
    #ap_ip                = walk_data(sess, ip_ap_oid, helper) # no result
    
    helper.add_summary("Access Points Status")

    for x in range(len(ap_names)):
        ap_name              = ap_names[x]
        ap_operational       = ap_operationals[x]
        ap_availability      = ap_availabilitys[x]
        ap_alarm             = ap_alarms[x]               

        # Add all states to the long output
        helper.add_long_output("%s - Operational: %s - Availabilty: %s - Alarm: %s" % (ap_name, operational_states[int(ap_operational)], availability_states[int(ap_availability)], alarm_states[int(ap_alarm)]))

        # Operational State
        if ap_operational != "1" and ap_operational != "4":
            helper.status(critical)
            helper.add_summary("%s Operational State: %s" % (ap_name, operational_states[int(ap_operational)]))

        # Avaiability State
        if ap_availability != "3":
            helper.status(critical)
            helper.add_summary("%s Availability State: %s" % (ap_name, availability_states[int(ap_availability)]))

        # Alarm State
        if ap_alarm == "2":
            helper.status(warning)
            helper.add_summary("%s Controller Alarm State: %s" % (ap_name, alarm_states[int(ap_alarm)]))
        
        if ap_alarm == "3" or ap_alarm == "4":
            helper.status(critical)
            helper.add_summary("%s Controller Alarm State: %s" % (ap_name, alarm_states[int(ap_alarm)]))

if __name__ == "__main__":
       
    # verify that a hostname is set
    verify_host(host, helper)

    sess = netsnmp.Session(Version=version, DestHost=host, Community=community)

    # The default return value should be always OK
    helper.status(ok)
    
    ######
    ## here we check the ressources
    ######
    if type.lower() == "ressources":
        check_ressources(sess)

    ######
    ## here we check the controller
    ######
    if type.lower() == "controller":
        check_controller(sess)

    ######
    ## and finally the access points
    ######
    if type.lower() == "accesspoints":
        check_accesspoints(sess)
        
    ## Print out plugin information and exit nagios-style
    helper.exit()
