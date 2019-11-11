#!/usr/bin/env python

# check_snmp_lband.py - Monitor a L-band redundancy controller via SNMP.

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

# OIDs from 2082-141.mib.txt
unit1_oid = ".1.3.6.1.4.1.31210.52.1.9.0"
unit2_oid = ".1.3.6.1.4.1.31210.52.1.13.0"

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
