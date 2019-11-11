#!/usr/bin/env python

#    Copyright (C) 2016-2019 rsmuc <rsmuc@sec-dev.de>

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

import pynag

import netsnmp
import os
import sys

dev_null = os.open(os.devnull, os.O_WRONLY)
tmp_stdout = os.dup(sys.stdout.fileno())


def dev_null_wrapper(func, *a, **kwargs):
    """
    Temporarily swap stdout with /dev/null, and execute given function while stdout goes to /dev/null.
    This is useful because netsnmp writes to stdout and disturbes Icinga result in some cases.
    """
    os.dup2(dev_null, sys.stdout.fileno())
    return_object = func(*a, **kwargs)
    sys.stdout.flush()
    os.dup2(tmp_stdout, sys.stdout.fileno())
    return return_object


def add_common_options(helper):
    # Define the common command line parameters
    helper.parser.add_option('-H', help="Hostname or ip address", dest="hostname")
    helper.parser.add_option('-C', '--community', dest='community', help='SNMP community of the SNMP service on target host.', default='public')
    helper.parser.add_option('-V', '--snmpversion', dest='version', help='SNMP version. (1, 2 or 3)', default=2, type='int')


def get_common_options(helper):
    # get the common options
    host = helper.options.hostname
    version = helper.options.version
    community = helper.options.community
    return host, version, community


def add_snmpv3_options(helper):
    # Define the common command line parameters
    helper.parser.add_option('-U', '--securityname', help="SNMPv3: security name (e.g. bert)", dest="secname")
    helper.parser.add_option('-L', '--securitylevel', help="SNMPv3: security level (noAuthNoPriv, authNoPriv, authPriv)", dest="seclevel")
    helper.parser.add_option('-a', '--authprotocol', help="SNMPv3: authentication protocol (MD5|SHA)", dest="authproto")
    helper.parser.add_option('-A', '--authpass', help="SNMPv3: authentication protocol pass phrase", dest="authpass")
    helper.parser.add_option('-x', '--privproto', help="SNMPv3: privacy protocol (DES|AES)", dest="privproto")
    helper.parser.add_option('-X', '--privpass',  help="SNMPv3: privacy protocol pass phrase", dest="privpass")


def verify_host(host, helper):
    if host == "" or host is None:
        helper.exit(summary="Hostname must be specified"
                    , exit_code=pynag.Plugins.unknown
                    , perfdata='')

    netsnmp_session = dev_null_wrapper(netsnmp.Session, 
                        DestHost=helper.options.hostname,
                        Community=helper.options.community,
                        Version=helper.options.version)

    try:
        # Works around lacking error handling in netsnmp package.
        if netsnmp_session.sess_ptr == 0:
            helper.exit(summary="SNMP connection failed"
                        , exit_code=pynag.Plugins.unknown
                        , perfdata='')
    
    except ValueError as error:
        helper.exit(summary=str(error)
                    , exit_code=pynag.Plugins.unknown
                    , perfdata='')
           

def verify_seclevel(seclevel, helper):
    if seclevel != "authPriv" and seclevel != "noAuthNoPriv" and seclevel != "authNoPriv" and seclevel != "" and seclevel != None:
        helper.exit(summary="security level is incorrect: %s. Check -l parameter." % (seclevel)
                        , exit_code=pynag.Plugins.unknown
                        , perfdata='')


# make a snmp get, if it fails (or returns nothing) exit the plugin
def get_data(session, oid, helper, empty_allowed=False):
    var = netsnmp.Varbind(oid)
    varl = netsnmp.VarList(var)
    data = session.get(varl)
    
    value = data[0]
    if value is None:
        helper.exit(summary="snmpget failed - no data for host "
                    + session.DestHost + " OID: " +oid
                    , exit_code=pynag.Plugins.unknown
                    , perfdata='')
         
    if not empty_allowed and not value:
            helper.exit(summary="snmpget failed - no data for host "
                        + session.DestHost + " OID: " +oid
                        , exit_code=pynag.Plugins.unknown
                        , perfdata='')
    return value

# make a snmp get, but do not exit the plugin, if it returns nothing
# be careful! This funciton does not exit the plugin, if snmp get fails!
def attempt_get_data(session, oid):
    var = netsnmp.Varbind(oid)
    varl = netsnmp.VarList(var)
    data = session.get(varl)
    value = data[0]
    return value

# make a snmp walk, if it fails (or returns nothing) exit the plugin
def walk_data(session, oid, helper):
    tag = []
    var = netsnmp.Varbind(oid)
    varl = netsnmp.VarList(var)
    data = list(session.walk(varl))

    if len(data) == 0:
        helper.exit(summary="snmpwalk failed - no data for host " + session.DestHost
                    + " OID: " +oid
                    , exit_code=pynag.Plugins.unknown
                    , perfdata='')
    for x in range(0, len(data)):
        tag.append(varl[x].tag)
    return data, tag

# make a snmp walk, but do not exit the plugin, if it returns nothing
# be careful! This function does not exit the plugin, if snmp walk fails!
def attempt_walk_data(session, oid):
    tag = []
    var = netsnmp.Varbind(oid)
    varl = netsnmp.VarList(var)
    data = list(session.walk(varl))
    for x in range(0, len(data)):
        tag.append(varl[x].tag)
    return data, tag

def state_summary(value, name, state_list, helper, ok_value = 'ok', info = None):
    """
    Always add the status to the long output, and if the status is not ok (or ok_value), 
    we show it in the summary and set the status to critical
    """
    # translate the value (integer) we receive to a human readable value (e.g. ok, critical etc.) with the given state_list
    state_value = state_list[int(value)]    
    summary_output = ''
    long_output = ''
    if not info:
        info = ''
    if state_value != ok_value:
        summary_output += ('%s status: %s %s ' % (name, state_value, info))
        helper.status(pynag.Plugins.critical)
    long_output += ('%s status: %s %s\n' % (name, state_value, info))
    return (summary_output, long_output)

def add_output(summary_output, long_output, helper):
    """
    if the summary output is empty, we don't add it as summary, otherwise we would have empty spaces (e.g.: '. . . . .') in our summary report
    """
    if summary_output != '':
        helper.add_summary(summary_output)
    helper.add_long_output(long_output)
