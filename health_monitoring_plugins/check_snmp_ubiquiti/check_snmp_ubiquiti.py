#!/usr/bin/env python

# check_snmp_ubiquiti.py - Monitor a Ubiquity airMax.

#    Copyright (C) 2016 Retakfual
#                  2016-2019 rsmuc <rsmuc@sec-dev.de>

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
 
# Imports
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown
import commands, sys, argparse, math
import netsnmp
import os
import datetime
sys.path.insert(1, os.path.join(sys.path[0], os.pardir))
from snmpSessionBaseClass import add_common_options, get_common_options, verify_host, get_data

# Create an instance of PluginHelper()
helper = PluginHelper()

# Define the command line options
add_common_options(helper)
helper.parser.add_option('-t', '--type', dest='power_Status', help='Select a Type, for a list of all possible Types use the argument -l') 
helper.parser.add_option('-l', '--list', dest='listFlag', default='False', action='store_true', help='Lists all output possibilities')
helper.parse_arguments()

status = helper.options.power_Status
flag_list = helper.options.listFlag
host, version, community = get_common_options(helper)


names = ["up", "signal", "cpu1m", "cpu5m", "cpu15m", "totalmem", "freemem", "tx", "rx"]

descriptions=["Uptime", "Signal Strength", "CPU usage (1 Minute Average)", "CPU usage (5 Minute Average)", 
"CPU usage (15 Minute Average)", "Total memory", "Free memory", "Tx Rate", "Rx Rate" ]

oids=[".1.3.6.1.2.1.1.3.0", ".1.3.6.1.4.1.14988.1.1.1.1.1.4", ".1.3.6.1.4.1.10002.1.1.1.4.2.1.3.1",
".1.3.6.1.4.1.10002.1.1.1.4.2.1.3.2",".1.3.6.1.4.1.10002.1.1.1.4.2.1.3.3",".1.3.6.1.4.1.10002.1.1.1.1.1.0",
".1.3.6.1.4.1.10002.1.1.1.1.2.0",".1.3.6.1.4.1.14988.1.1.1.1.1.2",".1.3.6.1.4.1.14988.1.1.1.1.1.3"]

units =['', '', '', '%', '%', '%', '', 'Byte', '', '' ]


##############
##   Main   ##
###############
if __name__ == '__main__':    
# The default return value should be always OK
  helper.status(ok)
  
  # shows the list of possible types if the flag is set
  if flag_list == True:
    for w,v in zip(names, descriptions):
      print w + ' = ' + v
    helper.status(unknown)
    helper.exit(summary='This is just a list and not a check!')
  
  # verify that a hostname is set
  verify_host(host, helper)
  
  # open session after validated host
  sess = netsnmp.Session(Version=version, DestHost=host, Community=community)
  
  # verify, that status(/type) parameter is not empty
  if (status == None) or (status not in names):
    helper.status(unknown)
    helper.exit(summary='Argument -t is missing or false!')
  
  # snmp gets for all oids in type-list
  ind = names.index(status)
  value = get_data(sess, oids[ind],helper)
  
  if names.index(status) == 0:
    value = str(datetime.timedelta(seconds=int(value)))
    helper.exit(summary='Uptime = %s'%value)
  
  # metric compares
  helper.add_metric(label='type', value = value, uom =' '+units[ind]+' ')
  helper.check_all_metrics()
  
  # programm end
  helper.exit()
