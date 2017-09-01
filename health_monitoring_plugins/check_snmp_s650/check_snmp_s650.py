#!/usr/bin/env python

# check_snmp_s650.py - Monitor a Microsemi S650 Timeserver

# Copyright (C) 2017 rsmuc rsmuc@mailbox.org
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
# along check_snmp_s650.py.  If not, see <http://www.gnu.org/licenses/>.

# based on the S650ALARM.mib

import sys
import os
import netsnmp
sys.path.insert(1, os.path.join(sys.path[0], os.pardir)) 
from snmpSessionBaseClass import add_common_options, get_common_options, verify_host, get_data
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown

# Create an instance of PluginHelper()
helper = PluginHelper()

# Define the command line options
add_common_options(helper)
helper.parser.add_option('-U', '--unit', dest='unit', help='Select the unit you want to monitor, if no unit is selected both units will be monitored', default="1") 
helper.parse_arguments()

# get the options
host, version, community = get_common_options(helper)
unit = helper.options.unit

# OIDs from S650ALARM.mib
unit1_oid = "iso.1.3.6.1.4.1.31210.52.1.9.0"
unit2_oid = "iso.1.3.6.1.4.1.31210.52.1.13.0"

status = {
    "0" : "Online",
    "1" : "Standby",
    "2" : "Alarmed"
    }

if __name__ == "__main__":

    # verify that a hostname is set
    verify_host(host, helper)

    # The default return value should be always OK
    helper.status(ok)

    sess = netsnmp.Session(Version=version, DestHost=host, Community=community)

    # get the values
    if unit == "1":
        value = get_data(sess, unit1_oid, helper)
    elif unit == "2":
        value = get_data(sess, unit2_oid, helper)
    else:
        helper.exit(summary="Wrong unit specified", exit_code=unknown, perfdata='')


    # add the summary
    helper.add_summary("Unit status is: %s" % (status[value]))

    if value == "2":
        helper.status(critical)

    # Print out plugin information and exit nagios-style
    helper.exit()
