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
    '''
    This is the base class for all snmp classes.
    It is should only be used to verify that there is a hostname set.
    '''
    def __init__(self, parameter_list, oid = None):
        self._Host = parameter_list[0]
        self._Version = parameter_list[1]
        self._Community = parameter_list[2]
        self._Helper = parameter_list[3]
        self._Oid = oid
        self.verify_host()
    # Verify that there is a hostname set
    def verify_host(self):
        if self._Host == '' or self._Host == None:
            self._Helper.exit(summary='Hostname must be specified', exit_code=unknown, perfdata='')

class snmp_walk_data_class(snmpSessionBaseClass):
    '''
    class for the snmpwalk command to retrieve data from a remote host. snmpwalk is a sequence of chained GETNEXT requests.
    '''

    def __init__(self, parameter_list ,oid):
        snmpSessionBaseClass.__init__(self, parameter_list, oid)
        self._Data = []
        self.walk_data()

    def walk_data(self):
        var = netsnmp.Varbind(self._Oid)
        self._Data = netsnmp.snmpwalk(var, Version=self._Version, DestHost=self._Host, Community=self._Community)
        # if we do not retrieve a value, either the connection to the device failed or the retrieved data is empty
        if not self._Data:
            self._Helper.exit(summary="\n SNMP connection to device failed or data retrieved from OID %s is empty" % self._Oid, exit_code=unknown, perfdata='')
        # function returns list of retrieved data
        return self._Data
    # get the amount of variables which _Data contains
    def get_len(self):
        return len(self._Data)
    # get the value at a specific position
    def valueAt(self,x):
        return self._Data[x]


class snmp_get_data_class(snmpSessionBaseClass):
    '''
    class for the snmpget command to retrieve data from a remote host.
    '''

    def __init__(self, parameter_list, oid):
        snmpSessionBaseClass.__init__(self, parameter_list, oid)
        self.get_data()

    def get_data(self):
        var = netsnmp.Varbind(self._Oid)
        data = netsnmp.snmpget(var, Version=self._Version, DestHost=self._Host, Community=self._Community)
        value = data[0]
        # if we do not retrieve a value, either the connection to the device failed or the retrieved data is empty
        if not value:
            self._Helper.exit(summary="\n SNMP connection to device failed or data retrieved from OID %s is empty" % self._Oid, exit_code=unknown, perfdata='')
        return value


class snmp_try_walk_data_class(snmpSessionBaseClass):
    '''
    With this class you can check an OID, to see if it contains data.
    Does not exit plugin helper, even when the OID/host is not reachable or it contains nothing!
    '''

    def __init__(self, parameter_list, oid, error_text = None):
        snmpSessionBaseClass.__init__(self, parameter_list, oid)
        self._Error_text = error_text
        self._Data = []
        if not self._Error_text:
            self._Error_text = ''

    def try_walk_data(self):
        err_msg = ''
        var = netsnmp.Varbind(self._Oid)
        self._Data = netsnmp.snmpwalk(var, Version=self._Version, DestHost=self._Host, Community=self._Community)
        # generate output if retrieved data is empty. Does not exit the helper.
        if not self._Data:
            err_msg = 'Did not receive data from OID %s. %s' % (self._Oid, self._Error_text)
        return self._Data, err_msg
    # get the amount of variables which _Data contains
    def get_len(self):
        return len(self._Data)
    # get the value at a specific position
    def valueAt(self,x):
        return self._Data[x]