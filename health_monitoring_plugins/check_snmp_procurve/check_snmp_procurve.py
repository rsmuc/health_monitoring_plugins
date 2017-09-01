#!/usr/bin/env python
# check_snmp_procurve.py - Check the sensors of HP / Aruba procurve switches via SNMP

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
# along with check_snmp_procurve.py.  If not, see <http://www.gnu.org/licenses/>.

# Import PluginHelper and some utility constants from the Plugins module
import sys
import os
import netsnmp
sys.path.insert(1, os.path.join(sys.path[0], os.pardir))
from snmpSessionBaseClass import add_common_options, get_common_options, verify_host, walk_data
from pynag.Plugins import PluginHelper, ok, critical, unknown, warning

# Create an instance of PluginHelper()
helper = PluginHelper()

# Add command line parameters
add_common_options(helper)
helper.parse_arguments()

# get the options
host, version, community = get_common_options(helper)

# The OIDs we need
oid_description                 = ".1.3.6.1.4.1.11.2.14.11.1.2.6.1.7" # The sensor description (e.g. Power Supply Sensor or Fan Sensor)
oid_status                      = ".1.3.6.1.4.1.11.2.14.11.1.2.6.1.4" # The status of the sensor

# Status table
senor_status_table = {
    "1" : "unknown",
    "2" : "bad",
    "3" : "warning",
    "4" : "good",
    "5" : "notPresent"
    }

def check_sensors():
    """
    collect and check all available sensors
    """
    
    all_sensors           = walk_data(sess, oid_description, helper)[0]
    all_status            = walk_data(sess, oid_status, helper)[0]
    

    # here we zip all index and descriptions to have a list like
    # [('Fan Sensor', '2'), ('Power Supply Sensor', '4')]
    # we are doomed if the lists do not have the same length ...  but that should never happen ... hopefully
    zipped = zip(all_sensors, all_status)

    for sensor in zipped:
        description       = sensor[0]
        status            = sensor[1]
        # translate the value to human readable
        try:
            status_string     = senor_status_table[status]       
        except KeyError:
            # if we receive an invalid value, we don't want to crash... 
            helper.exit(summary="received an undefined value from device: " + status, exit_code=unknown, perfdata='')
       
        # for each sensor the summary is added like: Fan Sensor: good
        helper.add_summary("%s: %s" % (description, status_string))

        # set the status
        if status == "2":
            helper.status(critical)
        if status == "3":
            helper.status(warning)

# The default return value should be always OK
helper.status(ok)

if __name__ == "__main__":

    # verify that a hostname is set
    verify_host(host, helper)

    sess = netsnmp.Session(Version=version, DestHost=host, Community=community)

    check_sensors()

    helper.check_all_metrics()

    # Print plugin information and exit nagios-style
    helper.exit()