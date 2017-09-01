#!/usr/bin/env python
# check_snmp_service.py - Check if a Windows service is in running state via SNMP.

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
# along with check_snmp_service.py.  If not, see <http://www.gnu.org/licenses/>.

# Import PluginHelper and some utility constants from the Plugins module
import sys
import os
import netsnmp
sys.path.insert(1, os.path.join(sys.path[0], os.pardir)) 
from snmpSessionBaseClass import add_common_options, get_common_options, verify_host, attempt_get_data, walk_data
from pynag.Plugins import PluginHelper,ok,critical


# Create an instance of PluginHelper()
helper = PluginHelper()

# Add command line parameters
add_common_options(helper)
helper.parser.add_option('-s', '--service', help="The name of the service you want to monitor (-s scan for scanning)", dest="service", default='')
helper.parser.add_option('-S', '--scan',   dest  = 'scan_flag', default   = False,    action = "store_true", help      = 'Show all available services')

helper.parse_arguments()
    
# get the options
host, version, community = get_common_options(helper)
service = helper.options.service
scan = helper.options.scan_flag

# that is the base id
base_oid = ".1.3.6.1.4.1.77.1.2.3.1.1"

'''
# for check_snmp_service we need to adapt the service_get_data function
def service_get_data(sess, host, version, community, oid):
    var = netsnmp.Varbind(oid)
    data = netsnmp.snmpget(var, Version=version, DestHost=host, Community=community)
    value = data[0]
    return value
'''

def convert_in_oid(service_name):
    """
    calculate the correct OID for the service name
    """
    s = service_name
    # convert the service_name to ascci
    service_ascii = [ord(c) for c in s] 
    # we need the length of the service name
    length = str(len(s))
    # make the oid
    oid = base_oid + "." + length + "." + ".".join(str(x) for x in service_ascii)
    return oid

if __name__ == "__main__":
    
    # verify that a hostname is set
    verify_host(host, helper)

    sess = netsnmp.Session(Version=version, DestHost=host, Community=community)

    # The default return value should be always OK
    helper.status(ok)

    # if no partition / disk is set, we will do a scan
    if service == "" or service is None:
        scan = True
    
    ##########
    # Here we do a scan
    ##########
    if scan:
        
        services = walk_data(sess, base_oid, helper)[0]

        if not services:
            print "No services found - SNMP disabled?"
            quit()
            
        print "Running services at host '" + host + "':\n"
        
        for service in services:
            print service
            
        if len(services) == 0:
            # if there are no running services, print the message
            print "no service running at host"
    
        # we don't want to return a icinga output, so we just end the script here
        quit()
    
    
    else:
        #############
        # Here we check the service
        #############
    
        ## convert the service name to a oid
        service_oid = convert_in_oid(service)
        # get the data
        result = attempt_get_data(sess, service_oid)
    
        if not result or result == "NOSUCHOBJECT":
            service_status = "NOT RUNNING"
            helper.status(critical)
        else:
            service_status = "RUNNING"
            helper.status(ok)
        
    
    helper.add_summary("Status of Service '" + service + "' is: " + service_status)
    
    # Print out plugin information and exit nagios-style
    helper.exit()
