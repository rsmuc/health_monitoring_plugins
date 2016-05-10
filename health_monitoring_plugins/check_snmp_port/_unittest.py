#!/usr/bin/python
from check_snmp_port import *
import pytest
import subprocess

def get_system_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = str(f.readline().split()[0])
        uptime_seconds = uptime_seconds.replace(".", "")
        return str(uptime_seconds)

def test_get():
    assert get_data("1.2.3.4", 2, "public", ".1") == None
    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert get_data("localhost", 2, "public", ".1.3.6.1.2.1.25.1.1.0")[:-1] == get_system_uptime()[:-1]

def test_walk_data():
    assert walk_data("1.2.3.4", 2, "public", ".1") == ()
    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert walk_data("localhost", 2, "public", ".1.3.6.1.2.1.25.1.1")[0][:-1] == get_system_uptime()[:-1]

def test_check_typ(capsys):
    with pytest.raises(SystemExit):
        # "test" is an invalid argument
        check_typ(helper, "test")
    out, err = capsys.readouterr()    
    assert out == "Unknown - Type (-t) must be udp or tcp.\n"
        
    assert check_typ(helper, "tcp") == None
    assert check_typ(helper, "udp") == None
    
def test_check_port(capsys):
    with pytest.raises(SystemExit):
        # "test" is an invalid argument
        check_port(helper, "test")
    out, err = capsys.readouterr()    
    assert out == "Unknown - Port (-p) must be a integer value or 'scan'.\n"
        
    assert check_port(helper, "22") == None
    assert check_port(helper, "scan") == None

def test_check_udp(capsys):
    # check "scan"
    with pytest.raises(SystemExit):
        check_udp(helper, "127.0.0.1", 2, "public", "scan")
    out, err = capsys.readouterr()    
    assert "UDP" in out
    
    # check "161" (open)
    assert check_udp(helper, "127.0.0.1", 2, "public", "161") == "Current status for UDP port 161 is: OPEN"
    
    # check "164" (closed)
    assert check_udp(helper, "127.0.0.1", 2, "public", "164") == "Current status for UDP port 164 is: CLOSED"

    # check "test"
    assert check_udp(helper, "127.0.0.1", 2, "public", "test") == "Current status for UDP port test is: CLOSED"

def test_check_tcp(capsys):    
    # check "scan"
    with pytest.raises(SystemExit):
        check_tcp(helper, "127.0.0.1", 2, "public", "scan", "closed", "closed")
    out, err = capsys.readouterr()    
    assert "TCP:" in out
    
    # check "22" (open) - will fail if port 22 is closed
    assert check_tcp(helper, "127.0.0.1", 2, "public", "22", "closed", "closed") == "Current status for TCP port 22 is: established"
    
    # check "164" (closed / not a UDP port)
    assert check_tcp(helper, "127.0.0.1", 2, "public", "164", "closed", "closed") == "Current status for TCP port 164 is: CLOSED"

    # check "test"
    assert check_tcp(helper, "127.0.0.1", 2, "public", "test", "closed", "closed") == "Current status for TCP port test is: CLOSED"

# integration test
def test_system_call(capsys):
    # without options
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_port/check_snmp_port.py", shell=True, stdout=subprocess.PIPE)
    assert "All open" in p.stdout.read()

    # with --help
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_port/check_snmp_port.py --help", shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()

    # with --type=TCP
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_port/check_snmp_port.py --type=TCP", shell=True, stdout=subprocess.PIPE)
    assert "TCP:" in p.stdout.read()
    
    # with --type=TCP --port=161 (closed)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_port/check_snmp_port.py --type=TCP --port=161", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Current status for TCP port 161 is: CLOSED" in p.stdout.read()
    
    # with --type=UDP --port=161 (open)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_port/check_snmp_port.py --type=UDP --port=161", shell=True, stdout=subprocess.PIPE)
    assert "OK - Current status for UDP port 161 is: OPEN" in p.stdout.read()
    
    #with --type=UDP --port=123 (closed)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_port/check_snmp_port.py --type=UDP --port=123", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Current status for UDP port 123 is: CLOSED" in p.stdout.read()
    
    #with --type=TCP --port=22 (open)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_port/check_snmp_port.py --type=TCP --port=22", shell=True, stdout=subprocess.PIPE)
    assert "OK - Current status for TCP port 22 is: established" in p.stdout.read()
