#!/usr/bin/env python

# check_snmp_janitza.py - Monitor the Janitza 604 via SNMP.

#    Copyright (C) 2016 Retakfual <https://github.com/Retakfual>
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


basicoid = '.1.3.6.1.4.1.34278.'
output =[]

oid = ['1.1.0', '1.2.0', '1.3.0', '1.7.0', '1.8.0', '1.9.0', '1.10.0', '1.11.0', '1.12.0', '1.13.0', '1.14.0', '1.15.0', '1.16.0', '1.17.0', '1.18.0',
  '1.19.0', '1.20.0', '1.21.0', '1.22.0', '1.23.0', '1.24.0', '2.1.0', '2.2.0', '2.3.0', '1.4.0', '1.5.0', '1.6.0']

names = [ 'uL1', 'uL2', 'uL3', 'iL1', 'iL2', 'iL3', 'iL4', 'iL5', 'iL6', 'pL1', 'pL2', 'pL3', 'qL1', 'qL2', 'qL3',  
  'sL1', 'sL2', 'sL3', 'cosPL1', 'cosPL2', 'cosPL3', 'p3', 'q3', 's3', 'uL1L2', 'uL2L3', 'uL3L1']


descriptions=['Voltage Phase L1 in 100mV','Voltage Phase L2 in 100mV','Voltage Phase L3 in 100mV','Current Phase L1 in 1mA','Current Phase L2 in 1mA',
  'Current Phase L3 in 1mA','Current Phase L4 in 1mA','Current Phase L5 in 1mA','Current Phase L6 in 1mA','Real Power L1 in Watt','Real Power L2 in Watt','Real Power L3 in Watt',
  'Reaktiv Power L1 in VAr','Reaktiv Power L2 in VAr','Reaktiv Power L3 in VAr','Power L1 in VA','Power L2 in VA','Power L3 in VA','Cos(Phi) L1 * 0.001',
  'Cos(Phi) L2 * 0.001','Cos(Phi) L3 * 0.001','Real Power Summe L1..L3 in Watt','Reaktiv Power Summe L1..L3 in Watt','Power Summe L1..L3 in Watt',
  'Voltage L1-L2','Voltage L2-L3','Voltage L3-L1']


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
  value = get_data(sess, basicoid+oid[ind],helper)
  
  # metric compares
  helper.add_metric(label='type', value = value, uom =' '+descriptions[ind]+' ')
  helper.check_all_metrics()
  
  # programm end
  helper.exit()
