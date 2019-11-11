#!/usr/bin/python
import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_fortinet'))
 
from check_snmp_fortinet import *

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
                .1.3.6.1.4.1.15983.1.1.3.1.14.10.0 = INTEGER: 24
                .1.3.6.1.4.1.15983.1.1.3.1.14.13.0 = INTEGER: 23
                .1.3.6.1.4.1.15983.1.1.3.1.14.14.0 = INTEGER: 9
                .1.3.6.1.4.1.15983.1.1.3.1.14.16.0 = INTEGER: 22
                .1.3.6.1.4.1.15983.1.1.4.1.1.21.0 = INTEGER: 1
                .1.3.6.1.4.1.15983.1.1.4.1.1.22.0 = INTEGER: 3
                .1.3.6.1.4.1.15983.1.1.4.1.1.23.0 = INTEGER: 1
                .1.3.6.1.4.1.15983.1.1.4.2.1.1.2.1 = STRING: "AP-1"
                .1.3.6.1.4.1.15983.1.1.4.2.1.1.2.2 = STRING: "ApTest1"
                .1.3.6.1.4.1.15983.1.1.4.2.1.1.21.1 = INTEGER: 1
                .1.3.6.1.4.1.15983.1.1.4.2.1.1.21.2 = INTEGER: 1
                .1.3.6.1.4.1.15983.1.1.4.2.1.1.26.1 = INTEGER: 1
                .1.3.6.1.4.1.15983.1.1.4.2.1.1.26.2 = INTEGER: 1
                .1.3.6.1.4.1.15983.1.1.4.2.1.1.27.1 = INTEGER: 3
                .1.3.6.1.4.1.15983.1.1.4.2.1.1.27.2 = INTEGER: 3
    ''' 
    register_snmpwalk_ouput(walk)
    start_server()

#integration test
def test_system_call(capsys):
    # without options
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_fortinet/check_snmp_fortinet.py", shell=True, stdout=subprocess.PIPE)
    assert "Unknown - Hostname must be specified\n" in p.stdout.read()

    # with --help
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_fortinet/check_snmp_fortinet.py --help", shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()

def test_ok(capsys):    
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_fortinet/check_snmp_fortinet.py -H localhost:1234", shell=True, stdout=subprocess.PIPE)
    assert "OK - Controller Status" in p.stdout.read()


def test_ok_ressources(capsys):    
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_fortinet/check_snmp_fortinet.py -H localhost:1234 --type=ressources", shell=True, stdout=subprocess.PIPE)
    result = p.stdout.read()
    assert "OK - Controller Status" in result
    assert "Memory: 22" in result

def test_ok_controller(capsys):
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_fortinet/check_snmp_fortinet.py -H localhost:1234 --type=controller", shell=True, stdout=subprocess.PIPE)
    result = p.stdout.read()
    assert "OK - Controller Status" in result
    assert "Controller Operational State: enabled" in result

def test_ok_accesspoints(capsys):
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_fortinet/check_snmp_fortinet.py -H localhost:1234 --type=accesspoints", shell=True, stdout=subprocess.PIPE)
    result = p.stdout.read()
    assert "OK - Access Points Status" in result
    assert "AP-1 - Operational: enabled - Availabilty: online - Alarm: no alarm" in result

def test_start_critical():
    # sensors bad
    unregister_all()
    walk =  ''' .1.3.6.1.4.1.15983.1.1.3.1.14.10.0 = INTEGER: 99
                .1.3.6.1.4.1.15983.1.1.3.1.14.13.0 = INTEGER: 99
                .1.3.6.1.4.1.15983.1.1.3.1.14.14.0 = INTEGER: 99
                .1.3.6.1.4.1.15983.1.1.3.1.14.16.0 = INTEGER: 99
                .1.3.6.1.4.1.15983.1.1.4.1.1.21.0 = INTEGER: 2
                .1.3.6.1.4.1.15983.1.1.4.1.1.22.0 = INTEGER: 3
                .1.3.6.1.4.1.15983.1.1.4.1.1.23.0 = INTEGER: 1
                .1.3.6.1.4.1.15983.1.1.4.2.1.1.2.1 = STRING: "AP-1"
                .1.3.6.1.4.1.15983.1.1.4.2.1.1.2.2 = STRING: "ApTest1"
                .1.3.6.1.4.1.15983.1.1.4.2.1.1.21.1 = INTEGER: 1
                .1.3.6.1.4.1.15983.1.1.4.2.1.1.21.2 = INTEGER: 1
                .1.3.6.1.4.1.15983.1.1.4.2.1.1.26.1 = INTEGER: 1
                .1.3.6.1.4.1.15983.1.1.4.2.1.1.26.2 = INTEGER: 2
                .1.3.6.1.4.1.15983.1.1.4.2.1.1.27.1 = INTEGER: 3
                .1.3.6.1.4.1.15983.1.1.4.2.1.1.27.2 = INTEGER: 6
    ''' 
    
    register_snmpwalk_ouput(walk)


def test_bad(capsys):    
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_fortinet/check_snmp_fortinet.py -H localhost:1234", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Controller Status" in p.stdout.read()


def test_bad_ressources(capsys):    
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_fortinet/check_snmp_fortinet.py -H localhost:1234 --type=ressources", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Controller Status. Controller Ressources - CPU: 99" in p.stdout.read()

def test_bad_controller(capsys):
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_fortinet/check_snmp_fortinet.py -H localhost:1234 --type=controller", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Controller Status" in p.stdout.read()

def test_bad_accesspoints(capsys):
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_fortinet/check_snmp_fortinet.py -H localhost:1234 --type=accesspoints", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Access Points Status. ApTest1 Operational State: disabled. ApTest1 Availability State: not installed" in p.stdout.read()
    


def test_stop():
    # stop the testagent
    stop_server()
