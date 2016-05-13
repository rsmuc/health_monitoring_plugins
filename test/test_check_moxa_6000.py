#!/usr/bin/python
import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_moxa_6000'))
 
from check_moxa_6000 import *

import pytest
import subprocess
from testagent import *
from types import MethodType

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address = "localhost:1234",
    rocommunity='public', rwcommunity='private')

#####################################
# run the test for the old firmware #
#####################################

def test_start():
    # start the testagent
    # CTS
    # DSR
    # DTR
    # Error Count Frame
    walk =  '''iso.3.6.1.4.1.8691.2.8.1.6.2.1.1.8.1 = INTEGER: 1
            iso.3.6.1.4.1.8691.2.8.1.6.2.1.1.5.1 = INTEGER: 1
            iso.3.6.1.4.1.8691.2.8.1.6.2.1.1.6.1 = INTEGER: 1
            iso.3.6.1.4.1.8691.2.8.1.6.3.1.1.1.1 = INTEGER: 0
            iso.3.6.1.4.1.8691.2.8.1.6.3.1.1.4.1 = INTEGER: 0
            iso.3.6.1.4.1.8691.2.8.1.6.3.1.1.3.1 = INTEGER: 0
            iso.3.6.1.4.1.8691.2.8.1.6.3.1.1.2.1 = INTEGER: 0'''   
    register_snmpwalk_ouput(walk)
    start_server()

def test_get_state():
    """
    get_state(value, warning_threshold, critical_threshold):
    """    
    assert get_state(10, 50, 100) == ok
    assert get_state(60, 50, 100) == warning
    assert get_state(200, 50, 100) == critical

# integration test
def test_system_test_moxa(capsys):
    # without options
    p=subprocess.Popen("health_monitoring_plugins/check_moxa_6000/check_moxa_6000.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert "Usage: check_moxa_6000.py [options]" in p.stdout.read()

    # without -H 1.2.3.4 (unknown host)
    p=subprocess.Popen("health_monitoring_plugins/check_moxa_6000/check_moxa_6000.py -H 1.2.3.4", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert "Usage: check_moxa_6000.py [options]\n\ncheck_moxa_6000.py: error: You must specifiy moxa rs232 port in order to run this plugin." in p.stdout.read()

    # without -H 1.2.3.4 (unknown host) -p 1
    p=subprocess.Popen("health_monitoring_plugins/check_moxa_6000/check_moxa_6000.py -H 1.2.3.4 -p 1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert "Unknown - Can't connect to SNMP agent at application server or RS232 port does not exist." in p.stdout.read()
    
    # with --help
    p=subprocess.Popen("health_monitoring_plugins/check_moxa_6000/check_moxa_6000.py --help", shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()

def test_with_host_ok():
    # everything ok    
    p=subprocess.Popen("health_monitoring_plugins/check_moxa_6000/check_moxa_6000.py -H 127.0.0.1:1234 -p 1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert "OK - CTS OK. DSR OK. DTR OK. ErrorCountFrame=0. ErrorCountBreak=0. ErrorCountOverrun=0. ErrorCountParity=0" in p.stdout.read()
    
def test_with_host_ok_dsr_only():
    # everything ok -t DSR    
    p=subprocess.Popen("health_monitoring_plugins/check_moxa_6000/check_moxa_6000.py -H 127.0.0.1:1234 -p 1 -t DSR", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert "OK - DSR OK\nDSR (Data Set Ready) ready\n" in p.stdout.read()

def test_all_nok():
    # start the testagent
    # Old Firmware # NTP not ok and gps not ok
    unregister_all()
    walk =  '''iso.3.6.1.4.1.8691.2.8.1.6.2.1.1.8.1 = INTEGER: 0
            iso.3.6.1.4.1.8691.2.8.1.6.2.1.1.5.1 = INTEGER: 0
            iso.3.6.1.4.1.8691.2.8.1.6.2.1.1.6.1 = INTEGER: 0
            iso.3.6.1.4.1.8691.2.8.1.6.3.1.1.1.1 = INTEGER: 123
            iso.3.6.1.4.1.8691.2.8.1.6.3.1.1.4.1 = INTEGER: 456
            iso.3.6.1.4.1.8691.2.8.1.6.3.1.1.3.1 = INTEGER: 789
            iso.3.6.1.4.1.8691.2.8.1.6.3.1.1.2.1 = INTEGER: 101112''' 
    
    register_snmpwalk_ouput(walk)

    p=subprocess.Popen("health_monitoring_plugins/check_moxa_6000/check_moxa_6000.py -H 127.0.0.1:1234 -p 1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert "Critical - CTS NOK. DSR NOK. DTR NOK. ErrorCountFrame=123. ErrorCountBreak=456. ErrorCountOverrun=789. ErrorCountPari" in p.stdout.read()
 
def test_with_host_nok_dsr_only():    
    p=subprocess.Popen("health_monitoring_plugins/check_moxa_6000/check_moxa_6000.py -H 127.0.0.1:1234 -p 1 -t DSR", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert "Critical - DSR NOK\nDSR (Data Set Ready) not ready\n" in p.stdout.read()
    
def test_with_host_nok_dsr_only():    
    p=subprocess.Popen("health_monitoring_plugins/check_moxa_6000/check_moxa_6000.py -H 127.0.0.1:1234 -p 1 -t DSR", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert "Critical - DSR NOK\nDSR (Data Set Ready) not ready\n" in p.stdout.read()
 
def test_with_host_nok_error_count_only():    
    p=subprocess.Popen("health_monitoring_plugins/check_moxa_6000/check_moxa_6000.py -H 127.0.0.1:1234 -p 1 -t ErrorCount", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert "Warning - ErrorCountFrame=123. ErrorCountBreak=456. ErrorCountOverrun=789. ErrorCountParity=101112\nError Count Frame" in p.stdout.read()

def test_stop():
    # stop the testagent
    stop_server()