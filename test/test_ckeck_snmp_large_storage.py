#!/usr/bin/python
import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_large_storage'))
 
from check_snmp_large_storage import *

import pytest
import subprocess
from testagent import *
from types import MethodType

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address = "localhost:1234",
    rocommunity='public', rwcommunity='private')

def test_start():
    # linux host  
    walk =  '''.1.3.6.1.2.1.25.2.3.1.1.10 = INTEGER: 10
            .1.3.6.1.2.1.25.2.3.1.1.31 = INTEGER: 31
            .1.3.6.1.2.1.25.2.3.1.3.10 = STRING: Swap space
            .1.3.6.1.2.1.25.2.3.1.3.31 = STRING: /
            .1.3.6.1.2.1.25.2.3.1.4.10 = INTEGER: 1024
            .1.3.6.1.2.1.25.2.3.1.4.31 = INTEGER: 4096
            .1.3.6.1.2.1.25.2.3.1.5.10 = INTEGER: 1324028
            .1.3.6.1.2.1.25.2.3.1.5.31 = INTEGER: 7381523
            .1.3.6.1.2.1.25.2.3.1.6.10 = INTEGER: 12504
            .1.3.6.1.2.1.25.2.3.1.6.31 = INTEGER: 628056'''   
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
    #assert walk_data("1.2.3.4", 2, "public", ".1") == ()

    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert walk_data("localhost", 2, "public", ".1.3.6.1.2.1.25.1.1")[0][:-3] == get_system_uptime()[:-3]

def test_calculate_real_size():
    """
    test calculate_real_size
    """
    assert calculate_real_size(5) == 5
    assert calculate_real_size(-5) == 2147483652

def test_without_options(capsys):
    # without options
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_large_storage/check_snmp_large_storage.py", shell=True, stdout=subprocess.PIPE)
    assert "All available disks at: localhost" in p.stdout.read()

def test_help():
    # with --help
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_large_storage/check_snmp_large_storage.py --help", shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()

def test_scan():
    # scan
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_large_storage/check_snmp_large_storage.py -H 127.0.0.1:1234", shell=True, stdout=subprocess.PIPE)
    assert "All available disks at: 127.0.0.1:1234\nDisk: \t'Swap space'" in p.stdout.read()

def test_root_partition():
    # root partition
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_large_storage/check_snmp_large_storage.py -H 127.0.0.1:1234 -p /", shell=True, stdout=subprocess.PIPE)
    assert "OK - 8.51% used (2.4GB of 28.16GB) at / | 'percent used'=8.51%;;;0;100" in p.stdout.read()

def test_root_partition_warning():
    # root partition in warning
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_large_storage/check_snmp_large_storage.py -H 127.0.0.1:1234 -p / --threshold metric='percent used',warning=5..inf,critical=95..inf", shell=True, stdout=subprocess.PIPE)
    assert "Warning - 8.51% used (2.4GB of 28.16GB) at /. Warning on percent used | 'percent used'=8.51%;~:5;~:95;0;100\n" in p.stdout.read()

def test_root_partition_in_TB():
    # root partition in TB
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_large_storage/check_snmp_large_storage.py -H 127.0.0.1:1234 -p / -u TB", shell=True, stdout=subprocess.PIPE)
    assert "OK - 8.51% used (0.0TB of 0.03TB) at / | 'percent used'=8.51%;;;0;100\n" in p.stdout.read()

def test_root_partition_in_MB():
    # root partition in TB
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_large_storage/check_snmp_large_storage.py -H 127.0.0.1:1234 -p / -u MB", shell=True, stdout=subprocess.PIPE)
    assert "OK - 8.51% used (2453.34MB of 28834.07MB) at / | 'percent used'=8.51%;;;0;100\n" in p.stdout.read()
  
  
def test_stop():
    # stop the testagent
    stop_server()