#!/usr/bin/env python
# check_snmp_teledyne.py - Monitor the health status of Teledyne Paradise Datacom

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

# Import PluginHelper and some utility constants from the Plugins module
import sys
import os
import netsnmp
sys.path.insert(1, os.path.join(sys.path[0], os.pardir)) 
from snmpSessionBaseClass import add_common_options, get_common_options, verify_host, get_data
from pynag.Plugins import PluginHelper,ok,critical


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
        
        # if the value is 1 / Fault the status is set to critical
        if value == "1":
            helper.status(critical)

    # Print out plugin information and exit nagios-style
    helper.exit()
