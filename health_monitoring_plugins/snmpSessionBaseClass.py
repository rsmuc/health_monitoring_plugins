#!/usr/bin/python

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
# along with health_monitoring_plugins. If not, see <http://www.gnu.org/licenses/>.

from pynag.Plugins import unknown
import netsnmp

def add_common_options(helper):
    # Define the common command line parameters
    helper.parser.add_option('-H', help="Hostname or ip address", dest="hostname")
    helper.parser.add_option('-C', '--community', dest='community', help='SNMP community of the SNMP service on target host.', default='public')
    helper.parser.add_option('-V', '--snmpversion', dest='version', help='SNMP version. (1 or 2)', default=2, type='int')
    
def get_common_options(helper):
    # get the common options
    host = helper.options.hostname
    version = helper.options.version
    community = helper.options.community
    return host, version, community

def verify_host(host, helper):
    if host == "" or host is None:
        helper.exit(summary="Hostname must be specified", exit_code=unknown, perfdata='')
        
def get_data(host, version, community, oid, helper):
    # make an snmp get, if it fails exit the plugin
    var = netsnmp.Varbind(oid)
    data = netsnmp.snmpget(var, Version=version, DestHost=host, Community=community)
    value = data[0]    
    if not value:
        helper.exit(summary="snmpget failed - no data for host " + host + " OID: " +oid, exit_code=unknown, perfdata='')
    return value

def walk_data(host, version, community, oid, helper):
    var = netsnmp.Varbind(oid)
    data = netsnmp.snmpwalk(var, Version=version, DestHost=host, Community=community)
    if len(data) == 0:
        helper.exit(summary="snmpwalk failed - no data for host " + host + " OID: " +oid, exit_code=unknown, perfdata='')
    return data
