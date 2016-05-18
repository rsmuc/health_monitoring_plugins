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

from pynag.Plugins import PluginHelper,ok,warning,critical,unknown
import netsnmp
'''
This is the base class for all snmp classes.
It is not used itself, it only used for Inheritance.
'''

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

class snmpSessionBaseClass:

    def __init__(self, parameter_list, oid):
        self._Host = parameter_list[0]
        self._Version = parameter_list[1]
        self._Community = parameter_list[2]
        self._Helper = parameter_list[3]
        self._Oid = oid

'''

'''
class snmp_walk_data_class(snmpSessionBaseClass):

    def __init__(self, parameter_list ,oid):
        snmpSessionBaseClass.__init__(self, parameter_list, oid)
        self._Data = []
        self.walk_data()

    def walk_data(self):
        var = netsnmp.Varbind(self._Oid)
        try:
            self._Data = netsnmp.snmpwalk(var, Version=self._Version, DestHost=self._Host, Community=self._Community)
        except:
            self._Helper.exit(summary="\n SNMP connection to device failed " + self._Oid, exit_code=unknown, perfdata='')
        #
        if not self._Data:
            self._Helper.exit(summary="\n SNMP connection to device failed " + self._Oid, exit_code=unknown, perfdata='')
        return self._Data
    # get the amount of variables which _Data contains
    def get_len(self):
        return len(self._Data)
    # get the value at a specific position
    def valueAt(self,x):
        return self._Data[x]

'''

'''
class snmp_get_data_class(snmpSessionBaseClass):

    def __init__(self, parameter_list, oid):
        snmpSessionBaseClass.__init__(self, parameter_list, oid)
        self.get_data()

    def get_data(self):
        try:
            var = netsnmp.Varbind(self._Oid)
            data = netsnmp.snmpget(var, Version=self._Version, DestHost=self._Host, Community=self._Community)
            value = data[0]
        except:
            self._Helper.exit(summary="\n SNMP connection to device failed " + self._Oid, exit_code=unknown, perfdata='')
        if not value:
            self._Helper.exit(summary="\n SNMP connection to device failed " + self._Oid, exit_code=unknown, perfdata='')
        return value

'''
With this class you can check an OID and see if it contains some data.
Does not exit plugin helper or pynag, if the OID is not reachable or it contains nothing.
'''
class snmp_try_walk_data_class(snmpSessionBaseClass):

    def __init__(self, parameter_list, oid, error_text = None):
        snmpSessionBaseClass.__init__(self, parameter_list, oid)
        self._Error_text = error_text
        self._Data = []

    def try_walk_data(self):
        output = ''
        if not self._Error_text:
            self._Error_text = ''
        var = netsnmp.Varbind(self._Oid)
        try:
            self._Data = netsnmp.snmpwalk(var, Version=self._Version, DestHost=self._Host, Community=self._Community)
        except:
            self._Helper.exit(summary="\n SNMP connection to device failed " + self._Oid, exit_code=unknown, perfdata='')
        if not self._Data:
            output = 'Does not retrieve data from OID %d. %s' % (self._Oid, self._Error_text)
        return self._Data, output
    # get the amount of variables which _Data contains
    def get_len(self):
        return len(self._Data)
    # get the value at a specific position
    def valueAt(self,x):
        return self._Data[x]