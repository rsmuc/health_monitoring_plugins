#!/usr/bin/env python

# check_snmp_sencere.py - Monitor Sencere via SNMP.

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
# along check_snmp_sencere.py.  If not, see <http://www.gnu.org/licenses/>.

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
helper.parser.add_option('-s', '--service', dest='service', help='Select the service that shall be monitored: IPProcessing, Thurayaprocessing, EventAssembler, ContentAssembler, ContentModelling, ContentWriter, ContentReader, EventReader, EventWriter, WebServer, PostProcessing, ISATprocessing, UserStore, AnnotationStore, RuleStore, HandoverConnectionsIn, HandoverConnectionsOut', default="IPProcessing") 
helper.parse_arguments()

# get the options
host, version, community = get_common_options(helper)
service = helper.options.service

# OIDs from RS8IP-BACKEND-MIB.mib

services = {
              "IPProcessing" : ".1.3.6.1.4.1.2566.127.5.315.1.1.1.0",
              "Thurayaprocessing" : ".1.3.6.1.4.1.2566.127.5.315.1.2.1.0",
              "EventAssembler" : ".1.3.6.1.4.1.2566.127.5.315.1.3.1.0",
              "ContentAssembler" : ".1.3.6.1.4.1.2566.127.5.315.1.4.1.0",
              "ContentModelling" : ".1.3.6.1.4.1.2566.127.5.315.1.5.1.0",
              "ContentWriter" : ".1.3.6.1.4.1.2566.127.5.315.1.6.1.0",
              "ContentReader" : ".1.3.6.1.4.1.2566.127.5.315.1.7.1.0",
              "EventReader" : ".1.3.6.1.4.1.2566.127.5.315.1.8.1.0",
              "EventWriter" : ".1.3.6.1.4.1.2566.127.5.315.1.9.1.0",
              "WebServer" : ".1.3.6.1.4.1.2566.127.5.315.1.10.1.0",
              "PostProcessing" : ".1.3.6.1.4.1.2566.127.5.315.1.11.1.0",
              "ISATprocessing" : ".1.3.6.1.4.1.2566.127.5.315.1.12.1.0",
              "UserStore" : ".1.3.6.1.4.1.2566.127.5.315.1.13.1.0",
              "AnnotationStore" : ".1.3.6.1.4.1.2566.127.5.315.1.14.1.0",
              "RuleStore" : ".1.3.6.1.4.1.2566.127.5.315.1.15.1.0",
              "HandoverConnectionsIn" : ".1.3.6.1.4.1.2566.127.5.300.1.2.9.0",
              "HandoverConnectionsOut" : ".1.3.6.1.4.1.2566.127.5.300.1.2.10.0"
              }



if __name__ == "__main__":

    # verify that a hostname is set
    verify_host(host, helper)

    # The default return value is unknown
    helper.status(ok)

    sess = netsnmp.Session(Version=version, DestHost=host, Community=community)

    #query the data depending on the service
    try:
        oid = services[service]
        value = get_data(sess, oid, helper)
    except KeyError:
        helper.exit(summary="Wrong service specified", exit_code=unknown, perfdata='')

    # if one of the handover values drop to 0, show a warning.
    if service in ["HandoverConnectionsIn", "HandoverConnectionsOut"]:
        helper.add_summary("Currently %s %s" % (value, service))
        if int(value) == 0:
            helper.status(warning)
        else:
            helper.status(ok)
    
    else:
        # add the summary
        helper.add_summary("%s status is: %s" % (service, value))

        if value == "error":
            helper.status(critical)
        elif value == "stopping":
            helper.status(warning)
        elif value in ["initializing", "running", "backingoff"]:
            helper.status(ok)
        else:
            helper.status(unknown)
    
    # Print out plugin information and exit nagios-style
    helper.exit()
