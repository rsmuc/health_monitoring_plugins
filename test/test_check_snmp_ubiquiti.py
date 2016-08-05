#!/usr/bin/python

# test_check_snmp_ubiquiti.py - test for Monitor a Ubiquity airMax.

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
# along with test_check_ubiquiti.py.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_ubiquiti'))
from check_snmp_ubiquiti import *

import pytest
import subprocess
from testagent import *

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address = "localhost:1234", rocommunity='public', rwcommunity='private')

# create netsnmp Session for test_get, test_walk ant test_attempt_walk
session = netsnmp.Session(Version=2, DestHost='localhost', Community='public')
failSession = netsnmp.Session(Version=2, DestHost='1.2.3.4', Community='public')


names = ["signal", "cpu1m", "cpu5m", "cpu15m", "totalmem", "freemem", "tx", "rx"]
descriptions=["Signal Strength", "CPU usage (1 Minute Average)", "CPU usage (5 Minute Average)", 
"CPU usage (15 Minute Average)", "Total memory", "Free memory", "Tx Rate", "Rx Rate" ]

oids=["iso.3.6.1.4.1.14988.1.1.1.1.1.4", "iso.3.6.1.4.1.10002.1.1.1.4.2.1.3.1",
"iso.3.6.1.4.1.10002.1.1.1.4.2.1.3.2","iso.3.6.1.4.1.10002.1.1.1.4.2.1.3.3","iso.3.6.1.4.1.10002.1.1.1.1.1.0",
"iso.3.6.1.4.1.10002.1.1.1.1.2.0","iso.3.6.1.4.1.14988.1.1.1.1.1.2","iso.3.6.1.4.1.14988.1.1.1.1.1.3"]

units =['', '', '%', '%', '%', '', 'Byte', '', '' ]

def test_start_ok_walk():
  # starts the testagent and fills the oid with values
  walk_var =''''''
  for o in oids:
    walk_var +=  o + " = INTEGER: 4\n" 
  register_snmpwalk_ouput(walk_var)
  start_server()
    
  
# tests the list if the listflag is set
def test_list_flag():
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_ubiquiti/check_snmp_ubiquiti.py -l", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  list_output =""
  for n,d in zip(names,descriptions):
    list_output += n +" = "+d+"\n"
  list_output += "Unknown - This is just a list and not a check!"
  assert list_output in p.stdout.read()
  
  

def test_ubiquiti_basics1():
  
  #without options
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_ubiquiti/check_snmp_ubiquiti.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  myout =  p.stdout.read()
  print "--------------------"
  print myout
  print "Unknown - Hostname must be specified"
  print "--------------------"
  assert "Unknown - Hostname must be specified" in myout
  
  # with host and no -t(does not depend if host is valid or not atm)
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_ubiquiti/check_snmp_ubiquiti.py -H 1.2.3.4", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  assert "Unknown - Argument -t is missing or false!" in p.stdout.read()
  
  # with  unknown host (-H 1.2.3.4) and -t qL1  
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_ubiquiti/check_snmp_ubiquiti.py -H 1.2.3.4 -t up", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  assert "Unknown - snmpget failed - no data for host 1.2.3.4 OID: .1.3.6.1.2.1.1.3.0" in p.stdout.read()


# tests all the ubiquiti status
def test_ubiquiti_ok_outputs():
  for n,u in zip(names,units):
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_ubiquiti/check_snmp_ubiquiti.py -H 127.0.0.1:1234 -t "+n +" --th metric=type,warning=:10,critical=:20", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert "OK -  | \'type\'=4 "+u+" ;:10;:20;;" in p.stdout.read()

    
def test_start_critical_walk():
  unregister_all()
  # starts the testagent and fills the oid with values
  walk_var =''''''
  for o in oids:
    walk_var += o + " = INTEGER: 22\n" 
  
  register_snmpwalk_ouput(walk_var)
  

# tests all the 
def test_critical_ubiquiti_outputs():
  for n,u in zip(names,units):
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_ubiquiti/check_snmp_ubiquiti.py -H 127.0.0.1:1234 -t "+n +" --th metric=type,warning=:10,critical=:20", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    myoutput = p.stdout.read()
    print myoutput
    print  "Critical - Critical on type | \'type\'=22 "+u+" ;:10;:20;;"
    
    assert "Critical - Critical on type | \'type\'=22 "+u+" ;:10;:20;;" in myoutput


def test_start_warning_walk():
  unregister_all()
  # starts the testagent and fills the oid with values
  walk_var =''''''
  for o in oids:
    walk_var += o + " = INTEGER: 19\n" 
  
  register_snmpwalk_ouput(walk_var)
  

# tests all the 
def test_warning_ubiquiti_outputs():
  for n,u in zip(names,units):
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_ubiquiti/check_snmp_ubiquiti.py -H 127.0.0.1:1234 -t "+n +" --th metric=type,warning=:10,critical=:20", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    myoutput = p.stdout.read()
    print myoutput
    print  "Warning - Warning on type | \'type\'=19 "+u+" ;:10;:20;;"
    
    assert "Warning - Warning on type | \'type\'=19 "+u+" ;:10;:20;;" in myoutput
    
def test_uptime():
  unregister_all()
  # starts the testagent and fills the oid with values
  walk_var="iso.3.6.1.2.1.1.3.0 = INTEGER: 4242424242\n" 
  register_snmpwalk_ouput(walk_var)
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_ubiquiti/check_snmp_ubiquiti.py -H 127.0.0.1:1234 -t \"up\" --th metric=type,warning=:10,critical=:20", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  
  myoutput = p.stdout.read()
  print myoutput
  print "OK - Uptime = 49102 days, 3:10:42"
  
  assert "OK - Uptime = 49102 days, 3:10:42" in myoutput

def test_stop_final():
    # stop the testagent
    stop_server()