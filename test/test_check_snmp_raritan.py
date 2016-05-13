#!/usr/bin/python
import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_raritan'))
 
from check_snmp_raritan import *

import pytest
import subprocess
from testagent import *
from types import MethodType

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address = "localhost:1234",
    rocommunity='public', rwcommunity='private')

def test_start_raritan():
    # start the testagent (Raritan walk)
    # Gauge32 are not working - So I replaced them by INTEGER
    # some of the values are not from a walk - I modified them to have the return values I need (critical etc.)
    walk =  '''iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.1 = INTEGER: 61
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.4 = INTEGER: 230
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.5 = INTEGER: 1357
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.6 = INTEGER: 1400
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.7 = INTEGER: 97
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.8 = INTEGER: 8574135
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.1 = INTEGER: 2
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.4 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.5 = INTEGER: 3
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.6 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.7 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.8 = INTEGER: 5
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.1 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.7 = INTEGER: 2
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.1 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.4 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.5 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.6 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.7 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.8 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.1 = INTEGER: 104
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.4 = INTEGER: 247
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.7 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.1 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.4 = INTEGER: 188
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.7 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.1 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.4 = INTEGER: 194
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.7 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.1 = INTEGER: 128
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.4 = INTEGER: 254
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.7 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.1 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.2 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.3 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.4 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.5 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.6 = STRING: "Switch Test 1"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.7 = STRING: "Switch Test 2"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.8 = STRING: "Switch Test 3"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.9 = STRING: "Switch Test 4"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.10 = STRING: "Switch Test 5"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.11 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.12 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.13 = STRING: "Switch C1"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.14 = STRING: "Switch C2"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.15 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.16 = STRING: "Switch 1"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.17 = STRING: "Switch 2"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.18 = STRING: "Switch 1"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.19 = STRING: "Switch 2"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.20 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.21 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.22 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.23 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.24 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.1.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.2.14 = INTEGER: 8
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.3.14 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.4.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.5.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.6.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.7.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.8.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.9.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.10.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.11.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.12.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.13.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.14.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.15.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.16.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.17.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.18.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.19.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.20.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.21.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.22.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.23.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.24.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.2 = STRING: "Tuerkontakt"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.3 = STRING: "External Sensor 3"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.4 = STRING: "On/Off 1"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.5 = STRING: "Temperature Rack 3"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.6 = STRING: "Humidity 1"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.7 = STRING: "Temperature 2"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.8 = STRING: "Air Pressure 1"
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.2 = INTEGER: 11
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.3 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.4 = INTEGER: 11
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.5 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.6 = INTEGER: 6
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.7 = INTEGER: 3
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.8 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.2 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.3 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.4 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.5 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.6 = INTEGER: 9
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.7 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.8 = INTEGER: 11
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.5 = INTEGER: 215
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.6 = INTEGER: 45
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.7 = INTEGER: 221
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.8 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.5 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.7 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.8 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.2 = INTEGER: 14
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.3 = INTEGER: 14
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.4 = INTEGER: 14
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.5 = INTEGER: 10
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.6 = INTEGER: 11
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.7 = INTEGER: 10
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.8 = INTEGER: 13
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.5 = INTEGER: 150
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.6 = INTEGER: 10
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.7 = INTEGER: 150
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.5 = INTEGER: 180
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.6 = INTEGER: 15
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.7 = INTEGER: 200
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.5 = INTEGER: 310
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.6 = INTEGER: 80
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.7 = INTEGER: 320
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.8 = INTEGER: 1000
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.5 = INTEGER: 270
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.6 = INTEGER: 70
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.7 = INTEGER: 280
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.8 = INTEGER: 800'''   
    register_snmpwalk_ouput(walk)
    start_server()

def get_system_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = str(f.readline().split()[0])
        uptime_seconds = uptime_seconds.replace(".", "")
        return str(uptime_seconds)

def test_get_raritan(capsys):
    with pytest.raises(SystemExit):
        get_data("1.2.3.4", 2, "public", ".1")
    out, err = capsys.readouterr()    
    assert "Unknown - SNMP connection to device failed" in out
    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert get_data("localhost", 2, "public", ".1.3.6.1.2.1.25.1.1.0")[:-2] == get_system_uptime()[:-2]

def test_walk_data_raritan(capsys):
    with pytest.raises(SystemExit):
        walk_data("1.2.3.4", 2, "public", ".1")
    out, err = capsys.readouterr()    
    assert "Unknown - SNMP connection to device failed" in out
    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert walk_data("localhost", 2, "public", ".1.3.6.1.2.1.25.1.1")[0][:-2] == get_system_uptime()[:-2]

def test_real_value_raritan(capsys):
    assert real_value(100, 2) == "1.0"

# integration test
def test_system_call_raritan(capsys):
    # without options
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py", shell=True, stdout=subprocess.PIPE)
    assert "Unknown - Hostname must be specified" in p.stdout.read()

    # without -H 1.2.3.4 (unknown host)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 1.2.3.4", shell=True, stdout=subprocess.PIPE)
    assert "Unknown - SNMP connection to device failed" in p.stdout.read()

    # with --help
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py --help", shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()
 
def test_outlet1_on():
    # Outlet 1 ON
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t outlet -i 1", shell=True, stdout=subprocess.PIPE)
    assert "OK - Outlet 1 - 'frei' is: ON" in p.stdout.read()

def test_outlet2_off():
    # Outlet 2 OFF
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t outlet -i 2", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Outlet 2 - 'Switch' is: OFF" in p.stdout.read()

def test_outlet3_unavailable():
    # Outlet 3 in unavailable state (-1)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t outlet -i 3", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Outlet 3 - 'frei' is: UNAVAILABLE" in p.stdout.read()

def test_sensor_alarmed():    
    # Sensor 2 - Door contact - alarmed
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t sensor -i 2", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Sensor 2 - 'Tuerkontakt'  is: alarmed\n" in p.stdout.read()

def test_sensor_normal():    
    # Sensor 3 - external Sensor - normal
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t sensor -i 3", shell=True, stdout=subprocess.PIPE)
    assert "OK - Sensor 3 - 'External Sensor 3'  is: normal" in p.stdout.read()

def test_sensor_temp_normal():    
    # Sensor 5 - Temperature - normal
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t sensor -i 5", shell=True, stdout=subprocess.PIPE)
    assert "OK - Sensor 5 - 'Temperature Rack 3' 21.5C is: normal" in p.stdout.read()

def test_sensor_humid_above():     
    # Sensor 6 - Humidity - aboveupperCritical
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t sensor -i 6", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Sensor 6 - 'Humidity 1' 45.0% is: aboveUpperCritical | 'Humidity 1'=45.0%;15.0:70.0;10.0:80.0;;\n" in p.stdout.read()

def test_sensor_temp_below():     
    # Sensor 7 - Temperature - belowLowerCritical
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t sensor -i 7", shell=True, stdout=subprocess.PIPE)
    assert "Warning - Sensor 7 - 'Temperature 2' 22.1C is: belowLowerWarning | 'Temperature 2'=22.1C;20.0:28.0;15.0:32.0;;\n" in p.stdout.read()

def test_inlet_ok():    
    # Inlet all OK
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t inlet", shell=True, stdout=subprocess.PIPE)
    assert "OK - Inlet. 6.1 A. 230.0 V. 1357.0 W. 1400.0 VA. 0.97. 8574135.0 Wh | 'Sensor 0'=6.1A;0.0:10.4;0.0:12.8;;" in p.stdout.read()

def test_inlet_critical():    
    # For a Critical Inlet, we need to change the values of the corresponding OIDs
    unregister_all()
    walk =  '''iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.1 = INTEGER: 61
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.4 = INTEGER: 230
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.5 = INTEGER: 1357
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.6 = INTEGER: 1400
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.7 = INTEGER: 97
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.8 = INTEGER: 8574135
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.1 = INTEGER: 2
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.4 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.5 = INTEGER: 3
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.6 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.7 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.8 = INTEGER: 5
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.1 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.7 = INTEGER: 2
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.1 = INTEGER: 2
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.4 = INTEGER: 3
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.5 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.6 = INTEGER: 5
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.7 = INTEGER: 6
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.8 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.1 = INTEGER: 104
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.4 = INTEGER: 247
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.7 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.1 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.4 = INTEGER: 188
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.7 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.1 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.4 = INTEGER: 194
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.7 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.1 = INTEGER: 128
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.4 = INTEGER: 254
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.7 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.1 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.2 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.3 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.4 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.5 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.6 = STRING: "Switch Test 1"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.7 = STRING: "Switch Test 2"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.8 = STRING: "Switch Test 3"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.9 = STRING: "Switch Test 4"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.10 = STRING: "Switch Test 5"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.11 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.12 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.13 = STRING: "Switch C1"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.14 = STRING: "Switch C2"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.15 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.16 = STRING: "Switch 1"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.17 = STRING: "Switch 2"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.18 = STRING: "Switch 1"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.19 = STRING: "Switch 2"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.20 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.21 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.22 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.23 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.24 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.1.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.2.14 = INTEGER: 8
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.3.14 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.4.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.5.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.6.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.7.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.8.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.9.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.10.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.11.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.12.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.13.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.14.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.15.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.16.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.17.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.18.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.19.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.20.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.21.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.22.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.23.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.24.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.2 = STRING: "Tuerkontakt"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.3 = STRING: "External Sensor 3"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.4 = STRING: "On/Off 1"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.5 = STRING: "Temperature Rack 3"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.6 = STRING: "Humidity 1"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.7 = STRING: "Temperature 2"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.8 = STRING: "Air Pressure 1"
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.2 = INTEGER: 11
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.3 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.4 = INTEGER: 11
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.5 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.6 = INTEGER: 6
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.7 = INTEGER: 3
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.8 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.2 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.3 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.4 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.5 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.6 = INTEGER: 9
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.7 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.8 = INTEGER: 11
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.5 = INTEGER: 215
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.6 = INTEGER: 45
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.7 = INTEGER: 221
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.8 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.5 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.7 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.8 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.2 = INTEGER: 14
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.3 = INTEGER: 14
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.4 = INTEGER: 14
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.5 = INTEGER: 10
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.6 = INTEGER: 11
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.7 = INTEGER: 10
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.8 = INTEGER: 13
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.5 = INTEGER: 150
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.6 = INTEGER: 10
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.7 = INTEGER: 150
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.5 = INTEGER: 180
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.6 = INTEGER: 15
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.7 = INTEGER: 200
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.5 = INTEGER: 310
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.6 = INTEGER: 80
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.7 = INTEGER: 320
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.8 = INTEGER: 1000
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.5 = INTEGER: 270
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.6 = INTEGER: 70
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.7 = INTEGER: 280
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.8 = INTEGER: 800'''
    register_snmpwalk_ouput(walk)
    
    # Inlet Critical
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t inlet", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Inlet. 6.1 A is belowLowerCritical. 6.1 A. 230.0 V is belowLowerWarning. 230.0 V. 1357.0 W. 1400.0 VA is" in p.stdout.read()
    
    
def test_stop():
    # stop the testagent
    stop_server()