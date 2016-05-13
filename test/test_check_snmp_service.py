#!/usr/bin/python
import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_service'))
 
from check_snmp_service import *

import pytest
import subprocess
from testagent import *
from types import MethodType


# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address = "localhost:1234",
    rocommunity='public', rwcommunity='private')

def test_start():
    # some open Windows services   
    walk =  '''.1.3.6.1.4.1.77.1.2.3.1.1.5.80.111.119.101.114 = STRING: "Power"
            .1.3.6.1.4.1.77.1.2.3.1.1.6.83.101.114.118.101.114 = STRING: "Server"
            .1.3.6.1.4.1.77.1.2.3.1.1.6.84.104.101.109.101.115 = STRING: "Themes"
            .1.3.6.1.4.1.77.1.2.3.1.1.9.73.80.32.72.101.108.112.101.114 = STRING: "IP Helper"'''   
    register_snmpwalk_ouput(walk)
    start_server()

def get_system_uptime():
    """
    just a helper to get the system uptime in seconds
    """
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = str(f.readline().split()[0])
        uptime_seconds = uptime_seconds.replace(".", "")
        return str(uptime_seconds)

def test_get():
    """
    test of the get_data function
    """
    # try to get data from a not existing host
    assert get_data("1.2.3.4", 2, "public", ".1") == None
    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert get_data("localhost", 2, "public", ".1.3.6.1.2.1.25.1.1.0")[:-3] == get_system_uptime()[:-3]

def test_walk_data():
    """
    test of the walk_data function
    """
    # run a walk on a not existing host
    assert walk_data("1.2.3.4", 2, "public", ".1") == ()

    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert walk_data("localhost", 2, "public", ".1.3.6.1.2.1.25.1.1")[0][:-3] == get_system_uptime()[:-3]

def test_oid_conversion():
    """
    test convert_in_oid
    """
    assert convert_in_oid("IP Helper") == ".1.3.6.1.4.1.77.1.2.3.1.1.9.73.80.32.72.101.108.112.101.114"

def test_without_options(capsys):
    # without options
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_service/check_snmp_service.py", shell=True, stdout=subprocess.PIPE)
    assert "Running services at host 'localhost':" in p.stdout.read()

def test_help():
    # with --help
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_service/check_snmp_service.py --help", shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()

def test_scan():    
    # with service scan
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_service/check_snmp_service.py -H 127.0.0.1:1234 -s scan", shell=True, stdout=subprocess.PIPE)
    assert "Running services at host '127.0.0.1:1234':\n\nPower\nServer\nThemes\nIP Helper\n" in p.stdout.read()

def test_service_available():    
    # with service "IP Helper" available
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_service/check_snmp_service.py -H 127.0.0.1:1234 -s 'IP Helper'", shell=True, stdout=subprocess.PIPE)
    assert "OK - Status of Service 'IP Helper' is: RUNNING\n" in p.stdout.read()
    
    # with service "Test" not available
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_service/check_snmp_service.py -H 127.0.0.1:1234 -s 'Test'", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Status of Service 'Test' is: NOT RUNNING\n" in p.stdout.read()
  

def test_stop():
    # stop the testagent
    stop_server()