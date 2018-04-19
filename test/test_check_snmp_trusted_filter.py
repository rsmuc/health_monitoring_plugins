#!/usr/bin/python
import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_trusted_filter'))
 
from check_snmp_trusted_filter import *

import pytest
import subprocess
from testagent import *

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address = "localhost:1234",
    rocommunity='public', rwcommunity='private')

# create netsnmp Sessions for test_walk_data, test_check_udp, test_check_tcp
session = netsnmp.Session(Version=2, DestHost='localhost', Community='public')
failSession = netsnmp.Session(Version=2, DestHost='1.2.3.4', Community='public')
test_session = netsnmp.Session(Version=2, DestHost='localhost:1234', Community='public')

def test_start():
    # everything ok
    walk =  '''
    .1.3.6.1.4.1.2566.107.41.1.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.1.0 = INTEGER: 80
    .1.3.6.1.4.1.2566.107.31.2.2.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.3.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.4.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.5.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.7.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.8.0 = INTEGER: 1
    ''' 
    register_snmpwalk_ouput(walk)
    start_server()

#integration test
def test_system_call(capsys):
    # without options
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_trusted_filter/check_snmp_trusted_filter.py", shell=True, stdout=subprocess.PIPE)
    assert "Unknown - Hostname must be specified\n" in p.stdout.read()

    # with --help
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_trusted_filter/check_snmp_trusted_filter.py --help", shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()

def test_tf(capsys):    
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_trusted_filter/check_snmp_trusted_filter.py -H localhost:1234", shell=True, stdout=subprocess.PIPE)
    assert "OK - Filter Status" in p.stdout.read()

    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_trusted_filter/check_snmp_trusted_filter.py -H localhost:1234 -s localhost:1234", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Filter Status" in p.stdout.read()
    
def test_stop():
    # stop the testagent
    stop_server()
