#!/usr/bin/python
# check_snmp_teledyne.py - Monitor the health status of Teledyne Paradise Datacom

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
# along with check_snmp_teledyne.py.  If not, see <http://www.gnu.org/licenses/>.

# Import PluginHelper and some utility constants from the Plugins module
import sys
import os
import netsnmp
sys.path.insert(1, os.path.join(sys.path[0], os.pardir)) 
from snmpSessionBaseClass import add_common_options, get_common_options, verify_host, get_data
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown


# Create an instance of PluginHelper()
helper = PluginHelper()

# add the common command line options
add_common_options(helper)
helper.parse_arguments()

# get the options
host, version, community = get_common_options(helper)


# OIDs from MBG-LANTIME-NG-MIB.mib
oids = {
"Unit 1" : "iso.3.6.1.4.1.20712.2.1.3.1.2.1",
"Unit 2" : "iso.3.6.1.4.1.20712.2.1.3.1.2.2",
"Unit 3" : "iso.3.6.1.4.1.20712.2.1.3.1.2.3",
"Fault Summary" : "iso.3.6.1.4.1.20712.2.1.3.1.2.4",
"Power Supply 1" : "iso.3.6.1.4.1.20712.2.1.3.1.2.5",
"Power Supply 2" : "iso.3.6.1.4.1.20712.2.1.3.1.2.6",
"RF Switch 1" : "iso.3.6.1.4.1.20712.2.1.3.1.2.11",
"RF Switch 2" : "iso.3.6.1.4.1.20712.2.1.3.1.2.12"
}

status = {
    "0" : "No Fault",
    "1" : "Fault",
    "2" : "N/A",
    "3" : "Pos1",
    "4" : "Pos2"
    }

def check_status():
    """
    check and show the current NTP status
    """
    ntp_status_int = get_data(sess, oid_ntp_current_state_int, helper)

    # convert the ntp_status integer value in a human readable value
    try:
        ntp_status_string = ntp_status[ntp_status_int]
    except KeyError:
        # if we receive an value, that is not in the dict
        helper.exit(summary="received an undefined value from device: " + ntp_status_int, exit_code=unknown, perfdata='')

    # the ntp status should be synchronized (new MIB) or normalOperation (old mib)
    if ntp_status_string != "synchronized" and ntp_status_string != "normalOperationPPS":    
        # that is a critical condition, because the time reference will not be reliable anymore
        helper.status(critical)
        helper.add_summary("NTP status: " + ntp_status_string)

def check_gps_status():
    """
    check and show the current GPS status
    """
    gps_status_int = get_data(sess, oid_gps_mode_int, helper)

    try:
        gps_mode_string = gps_mode[gps_status_int]
    except KeyError:
        # if we receive an value, that is not in the dict
        helper.exit(summary="received an undefined value from device: " + gps_status_int, exit_code=unknown, perfdata='')

    if gps_mode_string != "normalOperation" and gps_mode_string != "gpsSync" :
        # that is a warning condition, NTP could still work without the GPS antenna
        helper.status(warning)
        helper.add_summary("GPS status: " + gps_mode_string)

def check_satellites():
    """
    check and show the good satellites
    """
    # here we get the value for the satellites
    good_satellites = get_data(sess, oid_gps_satellites_good, helper)

    # Show the summary and add the metric and afterwards check the metric
    helper.add_summary("Good satellites: %s" % good_satellites)
    helper.add_metric(label='satellites',value=good_satellites) 

if __name__ == "__main__":

    # verify that a hostname is set
    verify_host(host, helper)

    # The default return value should be always OK
    helper.status(ok)

    sess = netsnmp.Session(Version=version, DestHost=host, Community=community)

    # here we check the status
    for name in sorted(oids):
        
        # get the snmp values
        value = get_data(sess, oids[name], helper)

        helper.add_summary("%s: %s" % (name, status[value]))
        
        if value == "1":
            helper.status(critical)


    # Print out plugin information and exit nagios-style
    helper.exit()
