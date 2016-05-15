#!/usr/bin/python
import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_time2'))
 
from check_snmp_time2 import *

import pytest
import subprocess
from testagent import *
from types import MethodType

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address = "localhost:1234",
    rocommunity='public', rwcommunity='private')

def test_start():
    # Time Stamp of Linux system  
    walk =  '''.1.3.6.1.2.1.25.1.2.0 = STRING: \x07\xe0\x05\x0e\x13\x04\x1d\x10+\x02\x02
            .1.3.6.1.2.1.1.1.0 = STRING: Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64
            '''   
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

def test_get(capsys):
    """
    test of the get_data function
    """
    # try to get data from a not existing host
    with pytest.raises(SystemExit):
        get_data("1.2.3.4", 2, "public", ".1")
    out, err = capsys.readouterr()    
    assert "Unknown - SNMP connection to device failed " in out
    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert get_data("localhost", 2, "public", ".1.3.6.1.2.1.25.1.1.0")[:-3] == get_system_uptime()[:-3]

def test_without_options(capsys):
    # without options
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py", shell=True, stdout=subprocess.PIPE)
    assert "Unknown - Hostname must be specified\n" in p.stdout.read()

def test_help():
    # with --help
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py --help", shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()

def test_linux_no_threshold():    
    # high offset, but no threshold is set
     p=subprocess.Popen("health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H 127.0.0.1:1234", shell=True, stdout=subprocess.PIPE)
     assert "OK - Remote UTC: 17:2:29. Offset = " in p.stdout.read()

def test_linux_with_threshold():    
     # high offset, but threshold => critical
     p=subprocess.Popen("health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H 127.0.0.1:1234 --th metric=offset,warning=-5:5,critical=-15:15", shell=True, stdout=subprocess.PIPE)
     assert "Critical - Critical on offset. Remote UTC: 17:2:29. Offset =" in p.stdout.read()

def test_linux_with_threshold_localhost():    
     # no offset, set threshold => OK
     p=subprocess.Popen("health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H 127.0.0.1 --th metric=offset,warning=-5:5,critical=-15:15", shell=True, stdout=subprocess.PIPE)
     assert "Offset = 0 s | 'offset'=0.0s;-5:5;-15:15;;\n" in p.stdout.read()

#def test_kaputti():    
#     # with service scan
#     var = netsnmp.Varbind(".1.3.6.1.2.1.1.1.0")
#     data = netsnmp.snmpget(var, Version=2, DestHost="192.168.2.193", Community="public")
#     print data
#     var = netsnmp.Varbind(".1.3.6.1.2.1.25.1.2.0")
#     data = netsnmp.snmpget(var, Version=2, DestHost="192.168.2.193", Community="public")
#     print data 
#     p=subprocess.Popen("health_monitoring_plugins/check_snmp_service/check_snmpj_service.py -H 127.0.0.1:1234 -s scan", shell=True, stdout=subprocess.PIPE)
#     assert "Running services at host '127.0.0.1:1234':\n\nPower\nServer\nThemes\nIP Helper\n" in p.stdout.read()
 

def test_windows():
    # Time Stamp of Windows system  
    unregister_all()
    walk =  '''.1.3.6.1.2.1.25.1.2.0 = STRING: \x07\xe0\x05\x0e\x13\x04\x1d\x10
            .1.3.6.1.2.1.1.1.0 = STRING: Hardware: Intel64 Family 6 Model 23 Stepping 10 AT/AT COMPATIBLE - Software: Windows Version 6.3 (Build 10586 Multiprocessor Free)
            '''   
    register_snmpwalk_ouput(walk)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H 127.0.0.1:1234 --th metric=offset,warning=-5:5,critical=-15:15", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Critical on offset. Local-Remote Time: 19:4:29. Offset = " in p.stdout.read()


def test_stop():
    # stop the testagent
    stop_server()