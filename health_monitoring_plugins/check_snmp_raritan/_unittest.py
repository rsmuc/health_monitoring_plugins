#!/usr/bin/python
from check_snmp_raritan import *
import pytest
import subprocess

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
    assert get_data("localhost", 2, "public", ".1.3.6.1.2.1.25.1.1.0")[:-1] == get_system_uptime()[:-1]

def test_walk_data_raritan(capsys):
    with pytest.raises(SystemExit):
        walk_data("1.2.3.4", 2, "public", ".1")
    out, err = capsys.readouterr()    
    assert "Unknown - SNMP connection to device failed" in out
    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert walk_data("localhost", 2, "public", ".1.3.6.1.2.1.25.1.1")[0][:-1] == get_system_uptime()[:-1]

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
