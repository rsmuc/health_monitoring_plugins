#!/usr/bin/python

# test_check_snmp_s650.py - test Monitor a L-band redundancy controller via SNMP.

# Copyright (C) 2017 rsmuc rsmuc@sec-dev.de
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
# along test_check_snmp_s650.py.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_s650'))
from check_snmp_s650 import *

import pytest
import subprocess
from testagent import *

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address = "localhost:1234", rocommunity='public', rwcommunity='private')

# create netsnmp Session for test_get, test_walk ant test_attempt_walk
session = netsnmp.Session(Version=2, DestHost='localhost', Community='public')
failSession = netsnmp.Session(Version=2, DestHost='1.2.3.4', Community='public')

base_oid= 'iso.3.6.1.4.1.31210.52.1.'
walk_var = ""

def test_start():
    # start the testagent
    walk =  '''iso.1.3.6.1.4.1.31210.52.1.9.0 = INTEGER: 0            
            iso.1.3.6.1.4.1.31210.52.1.13.0 = INTEGER: 0'''   
    register_snmpwalk_ouput(walk)
    start_server()
  
def test_Lband_basics():
  #without options
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_s650/check_snmp_s650.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  myout =  p.stdout.read()
  print "--------------------"
  print "got"
  print myout
  print "expected"
  print "Unknown - Hostname must be specified"
  print "--------------------"
  assert "Unknown - Hostname must be specified" in myout
  # with  unknown host (-H 1.2.3.4)
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_s650/check_snmp_s650.py -H 1.2.3.4 -U 1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  assert "Unknown - snmpget failed - no data for host 1.2.3.4 OID: iso.1.3.6.1.4.1.31210.52.1.9.0\n" in p.stdout.read()
  
# test if result without -U switch is correct  
def test_ok_outputs():
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_s650/check_snmp_s650.py -H 127.0.0.1:1234", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  myout =  p.stdout.read()
  print "--------------------"
  print "got"
  print myout
  print "expected"
  print "OK - Unit status is: Online"
  print "--------------------"
  assert "OK - Unit status is: Online" in myout

# test if -U switch is working
def test_ok():
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_s650/check_snmp_s650.py -H 127.0.0.1:1234 -U 1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  assert "OK - Unit status is: Online" in p.stdout.read()
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_s650/check_snmp_s650.py -H 127.0.0.1:1234 -U 2", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  assert "OK - Unit status is: Online" in p.stdout.read()
  
def test_start_critical():
    unregister_all()
    walk =  '''iso.1.3.6.1.4.1.31210.52.1.9.0 = INTEGER: 2            
            iso.1.3.6.1.4.1.31210.52.1.13.0 = INTEGER: 2'''  
    
    register_snmpwalk_ouput(walk)
  
def test_critical_output():
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_s650/check_snmp_s650.py -H 127.0.0.1:1234", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  myout =  p.stdout.read()
  
  print "--------------------"
  print "got"
  print myout
  print "expected"
  print "Critical - Unit status is: Alarmed"
  print "--------------------"
  assert "Critical - Unit status is: Alarmed" in myout
    
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_s650/check_snmp_s650.py -H 127.0.0.1:1234 -U 1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  assert "Critical - Unit status is: Alarmed" in p.stdout.read()
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_s650/check_snmp_s650.py -H 127.0.0.1:1234 -U 2", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  assert "Critical - Unit status is: Alarmed" in p.stdout.read()
  

def test_stop_final():
    # stop the testagent
    stop_server()
