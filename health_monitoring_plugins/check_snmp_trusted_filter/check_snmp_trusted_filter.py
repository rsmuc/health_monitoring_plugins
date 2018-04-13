#!/usr/bin/env python
# check_snmp_trusted_filter.py - Check a trusted filter

# Copyright (C) 2017 rsmuc <rsmuc@mailbox.org>
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
# along with check_snmp_trusted_filter.py.  If not, see <http://www.gnu.org/licenses/>.

# Import PluginHelper and some utility constants from the Plugins module
import sys
import os
import math
import netsnmp
sys.path.insert(1, os.path.join(sys.path[0], os.pardir)) 
from snmpSessionBaseClass import add_common_options, get_common_options, verify_host, get_data
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown

# Create an instance of PluginHelper()
helper = PluginHelper()

# define the command line options
add_common_options(helper)
helper.parser.add_option('-s', '--secondhost', dest='secondhost', help = "Enter a second host to be checked for ActivityState", type='str')
helper.parse_arguments()

# get the options
secondhost = helper.options.secondhost
host, version, community = get_common_options(helper)

# these dicts / definitions we need to get human readable values  
    
states = {
    1 : "ok",
    2 : "failed"
}

activity = {
    1 : "standby",
    2 : "active",
    3 : "error"
}

# OIDs
activity_oid   = '.1.3.6.1.4.1.2566.107.41.1.0'   #   tfDeviceActivityState
logfill_oid    = '.1.3.6.1.4.1.2566.107.31.2.1.0' #   slIpStatusLogFillLevel
ps1_oid        = '.1.3.6.1.4.1.2566.107.31.2.2.0' #   slIpStatusPowerSupplyUnit1
ps2_oid        = '.1.3.6.1.4.1.2566.107.31.2.3.0' #   slIpStatusPowerSupplyUnit2
fan1_oid       = '.1.3.6.1.4.1.2566.107.31.2.4.0' #   slIpStatusPowerFanUnit1
fan2_oid       = '.1.3.6.1.4.1.2566.107.31.2.5.0' #   slIpStatusPowerFanUnit2
bat_oid        = '.1.3.6.1.4.1.2566.107.31.2.7.0' #   slIpStatusInternalVoltage
temp_oid       = '.1.3.6.1.4.1.2566.107.31.2.8.0' #   slIpStatusInternalTemperature
activity_oid   = '.1.3.6.1.4.1.2566.107.41.1.0'   #   tfDeviceActivityState


def check_status(sess):
    """
    check the status
    """
    # get the data
    ps1_value              = states[int(get_data(sess, ps1_oid, helper))]
    ps2_value              = states[int(get_data(sess, ps2_oid, helper))]
    fan1_value             = states[int(get_data(sess, fan1_oid, helper))]
    fan2_value             = states[int(get_data(sess, fan2_oid, helper))]
    bat_value              = states[int(get_data(sess, bat_oid, helper))]
    temp_value             = states[int(get_data(sess, temp_oid, helper))]
    activity_value         = activity[int(get_data(sess, activity_oid, helper))]
    logfill_value          = get_data(sess, logfill_oid, helper)
    
    helper.add_summary("Filter Status")
    helper.add_long_output("Power Supply 1: %s" % ps1_value)
    if ps1_value != "ok":
        helper.status(critical)
        helper.add_summary("Power Supply 1: %s" % ps1_value)

    helper.add_long_output("Power Supply 2: %s" % ps2_value)
    if ps2_value != "ok":
        helper.status(critical)
        helper.add_summary("Power Supply 2: %s" % ps2_value)
    
    helper.add_long_output("Fan 1: %s" % fan1_value)
    if fan1_value != "ok":
        helper.status(critical)
        helper.add_summary("Fan 1: %s" % fan1_value)
    
    helper.add_long_output("Fan 2: %s" % fan2_value)
    if fan2_value != "ok":
        helper.status(critical)
        helper.add_summary("Fan 2: %s" % fan2_value)
    
    helper.add_long_output("Battery: %s" % bat_value)
    if bat_value != "ok":
        helper.status(critical)
        helper.add_summary("Battery: %s" % bat_value)
     
    helper.add_long_output("Temperature: %s" % temp_value)
    if temp_value != "ok":
        helper.status(critical)
        helper.add_summary("Temperature: %s" % temp_value)
    
    helper.add_metric(label='logfill',value=logfill_value, uom="%%")
    helper.add_long_output("Fill Level internal log: %s%%" % logfill_value)

    helper.add_long_output("Activity State: %s" % activity_value)
    if activity_value == "error":
        helper.status(critical)
        helper.add_summary("Activity State: %s" % activity_value)    

def check_secondhost(sess, sess1):
    """
    check the status of the second host
    """
    # get the data    
    activity_value1         = activity[int(get_data(sess, activity_oid, helper))]
    activity_value2         = activity[int(get_data(sess2, activity_oid, helper))]
        
    helper.add_long_output("Activity State 2: %s" % activity_value2)
    if activity_value1 == "active" and activity_value2 == "active":
        helper.status(critical)
        helper.add_summary("Filter 1 and Filter 2 active!")
            
    if activity_value1 == "standby" and activity_value2 == "standby":
        helper.status(critical)
        helper.add_summary("Filter 1 and Filter 2 standby!")

if __name__ == "__main__":
       
    # verify that a hostname is set
    verify_host(host, helper)

    sess = netsnmp.Session(Version=version, DestHost=host, Community=community)

    # The default return value should be always OK
    helper.status(ok)
    
    ######
    ## here we check the status of one controller
    ######
    
    check_status(sess)
        

    #######
    ### here we a second host
    #######
    if secondhost:
        sess2 = netsnmp.Session(Version=version, DestHost=secondhost, Community=community)
        check_secondhost(sess, sess2)


    helper.check_all_metrics()

    ## Print out plugin information and exit nagios-style
    helper.exit()
