#!/usr/bin/python
# check_snmp_time2.py - Check


# Copyright (C) 2016 Retakfual, rsmuc <rsmuc@mailbox.org>
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
# along with check_snmp_time2.py.  If not, see <http://www.gnu.org/licenses/>.

import time
import netsnmp
import datetime
import math
import struct
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown

# function for snmpget
def get_data(host, version, community, oid):
    try:
        var = netsnmp.Varbind(oid)
        data = netsnmp.snmpget(var, Version=version, DestHost=host, Community=community)
        value = data[0]
    except:
        helper.exit(summary="SNMP connection to device failed " + oid, exit_code=unknown, perfdata='')
    if not value:
        helper.exit(summary="SNMP connection to device failed " + oid, exit_code=unknown, perfdata='')
    return value

#Create an instance of PluginHelper()
helper = PluginHelper()

#Define the command line options
helper.parser.add_option('-H',                  dest  = 'hostname',                                               help      = 'Hostname or ip address')
helper.parser.add_option('-C', '--community',   dest  = 'community', default   = 'public',                        help      = 'SNMP community of the SNMP service on target host.')
helper.parser.add_option('-V', '--snmpversion', dest  = 'version',   default   = 2,        type   = 'int',        help      = 'SNMP version. (1 or 2)')
helper.parser.add_option('-o', '--tzoffset',    dest  = 'tzoffset',  default   = 0,        type   = 'int',        help      = 'the local systems utc offset to the servers utc, in minutes (use only if your remote device is in a different timezone)')
helper.parser.add_option('-l', '--localtime',   dest  = 'time_flag', default   = False,    action = "store_true", help      = 'force to use local time (only recommended if you have a non Windows OS remote device, that returns localtime and not utc)')
helper.parse_arguments()

#Get the options
host                        = helper.options.hostname
version                     = helper.options.version
community                   = helper.options.community
o_tzoff                     = helper.options.tzoffset
use_local                   = helper.options.time_flag

if __name__ == "__main__":
    
    #Verify that there is a hostname set
    if  host                    == '' or           host  == None:
        helper.exit(summary     = 'Hostname must be specified',          exit_code = unknown,  perfdata  = '')
    
    
    #The default return value should be always OK
    helper.status(ok)
    
    # get the remote time
    remote_time                 = get_data(host, version, community, '.1.3.6.1.2.1.25.1.2.0')
    # get the description (operating system)
    descr                       = get_data(host, version, community, '.1.3.6.1.2.1.1.1.0')
    
    # check if we are on a windows system
    windows = False
    if str(descr).find('Windows') != -1:
        windows = True
    
    #Extracting the remote time data from the OID
    #Value can be either 8 or 11 octets long 
    #The first try is for the length of eleven, the second for eight octets
    try:
        #unpack returns: year(first octet)|year(second octet)|month|day|hour|minute|second|deci-seconds|direction from UTC|hours from UTC|minutes from UTC 
        #e.g.: 07|224|04|09|13|04|43|00|+|02|00 
        #you have to convert the first two octets to get the year e.g.: 0x07|0xE0 => 0x07=7, 0xE0=224 => 07*256=1792, 1762+224=2016
        remote_time         = struct.unpack('BBBBBBBBcBB',  remote_time)
    except struct.error:
        #unpack returns: year|year|month|day|hour|minute|second|deci-seconds
        #e.g.:07|224|04|09|13|04|43|00
        #you have to convert the first two octets to get the year e.g.: 0x07|0xE0 => 0x07=7, 0xE0=224 => 07*256=1792, 1762+224=2016
        remote_time         = struct.unpack('BBBBBBBB', remote_time)
    
    remote_time_year            = (remote_time[0] * 256) + remote_time[1] # year
    remote_time_month           = remote_time[2] #month
    remote_time_day             = remote_time[3] #day
    remote_time_hours           = remote_time[4] #hours
    remote_time_minutes         = remote_time[5] #minutes
    remote_time_seconds         = remote_time[6] #seconds
    
    
    if len(remote_time) == 11:
        # in case we receive 11 values from unpack (depending on the remote device), we must calculate the UTC time with the offset
        remote_time_utc_dir         = remote_time[8]  # + or -
        remote_time_hours_offset    = remote_time[9]  # offset to UTC hours
        remote_time_minutes_offset  = remote_time[10] # offset to UTC minutes
        #Claculate UTC-time from local-time
        if remote_time_utc_dir      == '+':
            remote_time_hours   -= remote_time_hours_offset
            remote_time_minutes -= remote_time_minutes_offset
        elif remote_time_utc_dir     == '-':
            remote_time_hours   += remote_time_hours_offset[9]
            remote_time_minutes += remote_time_minutes_offset[10]
        
    try:
        #Format remote_time into timestamp
        remote_timestamp        = datetime.datetime(remote_time_year, remote_time_month, remote_time_day, remote_time_hours, remote_time_minutes, remote_time_seconds)
        
        # Windows will return the local time (not UTC), so we need to use the local time to compare
        # Force this this if '-l' or '--localtime' is set in commandline
        if windows or use_local :
            local_timestamp     = datetime.datetime.now()
            time_type = 'Local-Remote Time'
        else:
            # usually the we need the UTC time
            local_timestamp     = datetime.datetime.utcnow()
            time_type = 'Remote UTC'
    
        #Calculate the offset between local and remote time
        offset                  = time.mktime(local_timestamp.timetuple()) - time.mktime(remote_timestamp.timetuple()) + 60 * o_tzoff 
    
        helper.add_metric(label = 'offset', value = offset, uom = 's')
        helper.check_all_metrics()
    
    except IndexError:
        helper.exit(summary = 'remote device does not return a time value', exit_code = unknown, perfdata = '')
    
    
    #Print out plugin information and exit nagios-style
    helper.add_summary('%s: %s:%s:%s' % (time_type, remote_time_hours, remote_time_minutes, remote_time_seconds))
    helper.add_summary('Offset = %d s' % offset)
    helper.exit()
