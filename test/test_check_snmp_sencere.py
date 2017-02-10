#!/usr/bin/python

# test_check_snmp_sencere.py

# Copyright (C) 2017 rsmuc rsmuc@mailbox.org
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
# along test_check_snmp_sencere.py.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_sencere'))
from check_snmp_sencere import *

import pytest
import subprocess
from testagent import *

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address = "localhost:1234", rocommunity='public', rwcommunity='private')

# create netsnmp Session for test_get, test_walk ant test_attempt_walk
session = netsnmp.Session(Version=2, DestHost='localhost', Community='public')
failSession = netsnmp.Session(Version=2, DestHost='1.2.3.4', Community='public')

def test_start_ok():
    # start the testagent
    walk =  '''.1.3.6.1.4.1.2566.127.5.315.1.1.1.0  = STRING: "running"
            .1.3.6.1.4.1.2566.127.5.315.1.2.1.0  = STRING: "running"
            .1.3.6.1.4.1.2566.127.5.315.1.3.1.0  = STRING: "running"
            .1.3.6.1.4.1.2566.127.5.315.1.4.1.0  = STRING: "running"
            .1.3.6.1.4.1.2566.127.5.315.1.5.1.0  = STRING: "running"
            .1.3.6.1.4.1.2566.127.5.315.1.6.1.0  = STRING: "running"
            .1.3.6.1.4.1.2566.127.5.315.1.7.1.0  = STRING: "running"
            .1.3.6.1.4.1.2566.127.5.315.1.8.1.0  = STRING: "running"
            .1.3.6.1.4.1.2566.127.5.315.1.9.1.0  = STRING: "running"
            .1.3.6.1.4.1.2566.127.5.315.1.10.1.0  = STRING: "running"
            .1.3.6.1.4.1.2566.127.5.315.1.11.1.0  = STRING: "running"
            .1.3.6.1.4.1.2566.127.5.315.1.12.1.0  = STRING: "running"
            .1.3.6.1.4.1.2566.127.5.315.1.13.1.0  = STRING: "running"
            .1.3.6.1.4.1.2566.127.5.315.1.14.1.0  = STRING: "running"
            .1.3.6.1.4.1.2566.127.5.315.1.15.1.0  = STRING: "running"
            .1.3.6.1.4.1.2566.127.5.300.1.2.9.0 = Counter64: 5
            .1.3.6.1.4.1.2566.127.5.300.1.2.10.0 = Counter64: 5
            '''   
    register_snmpwalk_ouput(walk)
    start_server()
  
def test_sencere_basics():
  #without options
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_sencere/check_snmp_sencere.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  myout =  p.stdout.read()
  print "--------------------"
  print "got"
  print myout
  print "expected"
  print "Unknown - Hostname must be specified"
  print "--------------------"
  assert "Unknown - Hostname must be specified" in myout
  # with  unknown host (-H 1.2.3.4)
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_sencere/check_snmp_sencere.py -H 1.2.3.4", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  assert "Unknown - snmpget failed - no data for host 1.2.3.4 OID: .1.3.6.1.4.1.2566.127.5.315.1.1.1.0\n" in p.stdout.read()

# test start with wrong service flag
def test_wrong_service_flag():
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_sencere/check_snmp_sencere.py -H 127.0.0.1:1234 -s kaputti", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  myout =  p.stdout.read()
  print "--------------------"
  print "got"
  print myout
  print "expected"
  print "Unknown - Wrong service specified\n"
  print "--------------------"
  assert "Unknown - Wrong service specified\n" in myout

  
# test if "running" results in "OK" status (backend)
def test_ok_outputs():
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_sencere/check_snmp_sencere.py -H 127.0.0.1:1234 -s IPProcessing", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  myout =  p.stdout.read()
  print "--------------------"
  print "got"
  print myout
  print "expected"
  print "OK - IPProcessing status is: running"
  print "--------------------"
  assert "OK - IPProcessing status is: running" in myout

 # test if "5" results in "OK" handoverdevice
def test_ok_outputs():
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_sencere/check_snmp_sencere.py -H 127.0.0.1:1234 -s HandoverConnectionsIn", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  myout =  p.stdout.read()
  print "--------------------"
  print "got"
  print myout
  print "expected"
  print "OK - Currently 5 HandoverConnectionsIn"
  print "--------------------"
  assert "OK - Currently 5 HandoverConnectionsIn" in myout

  
def test_start_critical():
    unregister_all()
    walk =  '''.1.3.6.1.4.1.2566.127.5.315.1.1.1.0  = STRING: "error"
            .1.3.6.1.4.1.2566.127.5.315.1.2.1.0  = STRING: "error"
            .1.3.6.1.4.1.2566.127.5.315.1.3.1.0  = STRING: "error"
            .1.3.6.1.4.1.2566.127.5.315.1.4.1.0  = STRING: "error"
            .1.3.6.1.4.1.2566.127.5.315.1.5.1.0  = STRING: "error"
            .1.3.6.1.4.1.2566.127.5.315.1.6.1.0  = STRING: "error"
            .1.3.6.1.4.1.2566.127.5.315.1.7.1.0  = STRING: "error"
            .1.3.6.1.4.1.2566.127.5.315.1.8.1.0  = STRING: "error"
            .1.3.6.1.4.1.2566.127.5.315.1.9.1.0  = STRING: "error"
            .1.3.6.1.4.1.2566.127.5.315.1.10.1.0  = STRING: "error"
            .1.3.6.1.4.1.2566.127.5.315.1.11.1.0  = STRING: "error"
            .1.3.6.1.4.1.2566.127.5.315.1.12.1.0  = STRING: "error"
            .1.3.6.1.4.1.2566.127.5.315.1.13.1.0  = STRING: "error"
            .1.3.6.1.4.1.2566.127.5.315.1.14.1.0  = STRING: "error"
            .1.3.6.1.4.1.2566.127.5.315.1.15.1.0  = STRING: "error"
            .1.3.6.1.4.1.2566.127.5.300.1.2.9.0 = Counter64: 0
            .1.3.6.1.4.1.2566.127.5.300.1.2.10.0 = Counter64: 0
            '''   
    
    register_snmpwalk_ouput(walk)
  
# test if "error" results in "CRITICAL" status
def test_critical_outputs():
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_sencere/check_snmp_sencere.py -H 127.0.0.1:1234 -s RuleStore", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  myout =  p.stdout.read()
  print "--------------------"
  print "got"
  print myout
  print "expected"
  print "Critical - RuleStore status is: error"
  print "--------------------"
  assert "Critical - RuleStore status is: error" in myout  

def test_start_warning():
    unregister_all()
    walk =  '''.1.3.6.1.4.1.2566.127.5.315.1.1.1.0  = STRING: "stopping"
            .1.3.6.1.4.1.2566.127.5.315.1.2.1.0  = STRING: "stopping"
            .1.3.6.1.4.1.2566.127.5.315.1.3.1.0  = STRING: "stopping"
            .1.3.6.1.4.1.2566.127.5.315.1.4.1.0  = STRING: "stopping"
            .1.3.6.1.4.1.2566.127.5.315.1.5.1.0  = STRING: "stopping"
            .1.3.6.1.4.1.2566.127.5.315.1.6.1.0  = STRING: "stopping"
            .1.3.6.1.4.1.2566.127.5.315.1.7.1.0  = STRING: "stopping"
            .1.3.6.1.4.1.2566.127.5.315.1.8.1.0  = STRING: "stopping"
            .1.3.6.1.4.1.2566.127.5.315.1.9.1.0  = STRING: "stopping"
            .1.3.6.1.4.1.2566.127.5.315.1.10.1.0  = STRING: "stopping"
            .1.3.6.1.4.1.2566.127.5.315.1.11.1.0  = STRING: "stopping"
            .1.3.6.1.4.1.2566.127.5.315.1.12.1.0  = STRING: "stopping"
            .1.3.6.1.4.1.2566.127.5.315.1.13.1.0  = STRING: "stopping"
            .1.3.6.1.4.1.2566.127.5.315.1.14.1.0  = STRING: "stopping"
            .1.3.6.1.4.1.2566.127.5.315.1.15.1.0  = STRING: "stopping"
            .1.3.6.1.4.1.2566.127.5.300.1.2.9.0 = Counter64: 0
            .1.3.6.1.4.1.2566.127.5.300.1.2.10.0 = Counter64: 0
            '''   
    
    register_snmpwalk_ouput(walk)
  
# test if "stopping" results in "WARNING" status
def test_warning_outputs():
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_sencere/check_snmp_sencere.py -H 127.0.0.1:1234 -s ContentReader", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  myout =  p.stdout.read()
  print "--------------------"
  print "got"
  print myout
  print "expected"
  print "Warning - ContentReader status is: stopping"
  print "--------------------"
  assert "Warning - ContentReader status is: stopping" in myout  

# test if "0" results in "WARNING" handoverdevice
def test_ok_outputs():
  p = subprocess.Popen("health_monitoring_plugins/check_snmp_sencere/check_snmp_sencere.py -H 127.0.0.1:1234 -s HandoverConnectionsIn", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  myout =  p.stdout.read()
  print "--------------------"
  print "got"
  print myout
  print "expected"
  print "Warning - Currently 0 HandoverConnectionsIn"
  print "--------------------"
  assert "Warning - Currently 0 HandoverConnectionsIn" in myout


def test_stop_final():
    # stop the testagent
    stop_server()
