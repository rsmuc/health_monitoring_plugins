#!/usr/bin/python

# test_check_snmp_janitza.py - test for Monitor the Janitza 604 via SNMP.

# Copyright (C) 2016 Retakfual <https://github.com/Retakfual>, rsmuc
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
# along with test_check_snmp_janitza.py.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_janitza'))
from check_snmp_janitza import *

import pytest
import subprocess
from testagent import *

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address = "localhost:1234", rocommunity='public', rwcommunity='private')

# create netsnmp Session for test_get, test_walk ant test_attempt_walk
session = netsnmp.Session(Version=2, DestHost='localhost', Community='public')
failSession = netsnmp.Session(Version=2, DestHost='1.2.3.4', Community='public')

base_oid= basicoid = 'iso.3.6.1.4.1.34278.'


oid = ['1.1.0', '1.2.0', '1.3.0', '1.7.0', '1.8.0', '1.9.0', '1.10.0', '1.11.0', '1.12.0', '1.13.0', '1.14.0', '1.15.0', '1.16.0', '1.17.0', '1.18.0',
  '1.19.0', '1.20.0', '1.21.0', '1.22.0', '1.23.0', '1.24.0', '2.1.0', '2.2.0', '2.3.0', '1.4.0', '1.5.0', '1.6.0']

names = [ 'uL1', 'uL2', 'uL3', 'iL1', 'iL2', 'iL3', 'iL4', 'iL5', 'iL6', 'pL1', 'pL2', 'pL3', 'qL1', 'qL2', 'qL3',  
  'sL1', 'sL2', 'sL3', 'cosPL1', 'cosPL2', 'cosPL3', 'p3', 'q3', 's3', 'uL1L2', 'uL2L3', 'uL3L1']


descriptions=['Voltage Phase L1 in 100mV','Voltage Phase L2 in 100mV','Voltage Phase L3 in 100mV','Current Phase L1 in 1mA','Current Phase L2 in 1mA',
  'Current Phase L3 in 1mA','Current Phase L4 in 1mA','Current Phase L5 in 1mA','Current Phase L6 in 1mA','Real Power L1 in Watt','Real Power L2 in Watt','Real Power L3 in Watt',
  'Reaktiv Power L1 in VAr','Reaktiv Power L2 in VAr','Reaktiv Power L3 in VAr','Power L1 in VA','Power L2 in VA','Power L3 in VA','Cos(Phi) L1 * 0.001',
  'Cos(Phi) L2 * 0.001','Cos(Phi) L3 * 0.001','Real Power Summe L1..L3 in Watt','Reaktiv Power Summe L1..L3 in Watt','Power Summe L1..L3 in Watt',
  'Voltage L1-L2','Voltage L2-L3','Voltage L3-L1']

vals_test=["0","1","1","1","256980","270097","258532","185239","1","-5","-3","-4","0","0","0","-4","24","29","29","22","1000","-10","0","83","1","1","1"]





def test_start_ok_walk():
  # starts the testagent and fills the oid with values
  walk_var =''''''
  for o,v in zip(oid,vals_test):
    walk_var += base_oid+ o + " = INTEGER: "+v+"\n" 
  
  register_snmpwalk_ouput(walk_var)
  start_server()


#tests the real basic stuff 
def test_janitza_basics():
  
  #without options
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_janitza/check_snmp_janitza.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  myout =  p.stdout.read()
  print "--------------------"
  print myout
  print "Unknown - Hostname must be specified"
  print "--------------------"
  assert "Unknown - Hostname must be specified" in myout
  
  # with host and no -t(does not depend if host is valid or not atm)
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_janitza/check_snmp_janitza.py -H 1.2.3.4", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  assert "Unknown - Argument -t is missing or false!" in p.stdout.read()
  
   # with  unknown host (-H 1.2.3.4) and -t qL1  snmp_
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_janitza/check_snmp_janitza.py -H 1.2.3.4 -t qL1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  assert "Unknown - snmpget failed - no data for host 1.2.3.4 OID: .1.3.6.1.4.1.34278.1.16.0" in p.stdout.read()


# tests the list if the listflag ist set
def test_list_flag():
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_janitza/check_snmp_janitza.py -l", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  list_output =""
  for n,d in zip(names,descriptions):
    list_output += n +" = "+d+"\n"
  list_output += "Unknown - This is just a list and not a check!"
  assert list_output in p.stdout.read()


# tests the function of every type with a ok check
def test_ok_janiza_outputs():
  for n,d,v in zip(names,descriptions,vals_test):
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_janitza/check_snmp_janitza.py -H 127.0.0.1:1234 -t "+n +" --th metric=type,warning=-30:,critical=-40:", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert "OK -  | \'type\'="+v+" "+d+" ;-30:;-40:;;" in p.stdout.read()

    
def test_start_critical_walk():
  unregister_all()
  # starts the testagent and fills the oid with values
  walk_var =''''''
  for o,v in zip(oid,vals_test):
    walk_var += base_oid+ o + " = INTEGER: "+v+"\n" 
  
  register_snmpwalk_ouput(walk_var)
  
    # tests the function of every type with a critical check
def test_critical_janiza_outputs():
  for n,d,v in zip(names,descriptions,vals_test):
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_janitza/check_snmp_janitza.py -H 127.0.0.1:1234 -t "+n +" --th metric=type,warning=3:4,critical=2:5", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    myoutput = p.stdout.read()
    print myoutput
    print  "Critical - Critical on type | \'type\'="+v+" "+d+" ;3:4;2:5;;"
    
    assert "Critical - Critical on type | \'type\'="+v+" "+d+" ;3:4;2:5;;" in myoutput


def test_start_warning_walk():
  unregister_all()
  # starts the testagent and fills the oid with values
  walk_var =''''''
  for o,v in zip(oid,vals_test):
    walk_var += base_oid+ o + " = INTEGER: "+v+"\n" 
  
  register_snmpwalk_ouput(walk_var)
  
  
  
    # tests the function of every type with a warning check
def test_warning_janiza_outputs():
  for n,d,v in zip(names,descriptions,vals_test):
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_janitza/check_snmp_janitza.py -H 127.0.0.1:1234 -t "+n +" --th metric=type,warning=2:5,critical=-40:280000", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    myoutput = p.stdout.read()
    print myoutput
    print  "Warning - Warning on type | \'type\'="+v+" "+d+" ;2:5;-40:280000;;"
    
    assert "Warning - Warning on type | \'type\'="+v+" "+d+" ;2:5;-40:280000;;" in myoutput
    
    
def test_stop_final():
    # stop the testagent
    stop_server()
