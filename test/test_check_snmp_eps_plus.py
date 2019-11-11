#!/usr/bin/python
import context
import netsnmp
import subprocess
from testagent import *

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address="localhost:1234",
          rocommunity='public', rwcommunity='private')

# create netsnmp Sessions for test_walk_data, test_check_udp, test_check_tcp
session = netsnmp.Session(Version=2, DestHost='localhost', Community='public')
failSession = netsnmp.Session(Version=2, DestHost='1.2.3.4', Community='public')
test_session = netsnmp.Session(Version=2, DestHost='localhost:1234', Community='public')


def test_start():
    # start the testagent (port 22 (TCP) is esablished and 161 is open)    
    walk = '''
    .1.3.6.1.4.1.24734.16.2.1.1.3.0 = STRING: "Master"
    .1.3.6.1.4.1.24734.16.2.1.1.3.1 = STRING: "Slave"
    .1.3.6.1.4.1.24734.16.2.1.1.3.18 = STRING: "Slave2"
    .1.3.6.1.4.1.24734.16.8.1.1.4.0.0 = STRING: "Outlet 1x"
    .1.3.6.1.4.1.24734.16.8.1.1.4.0.1 = STRING: "Outlet 2x"
    .1.3.6.1.4.1.24734.16.8.1.1.4.0.2 = STRING: "Outlet 3x"
    .1.3.6.1.4.1.24734.16.8.1.1.4.0.3 = STRING: "Outlet 4x"
    .1.3.6.1.4.1.24734.16.8.1.1.4.1.0 = STRING: "Outlet 1x 1x"
    .1.3.6.1.4.1.24734.16.8.1.1.4.1.1 = STRING: "Outlet 1x 2x"
    .1.3.6.1.4.1.24734.16.8.1.1.5.0.0 = STRING: "On"
    .1.3.6.1.4.1.24734.16.8.1.1.5.0.1 = STRING: "On"
    .1.3.6.1.4.1.24734.16.8.1.1.5.0.2 = STRING: "On"
    .1.3.6.1.4.1.24734.16.8.1.1.5.0.3 = STRING: "On"
    .1.3.6.1.4.1.24734.16.8.1.1.5.1.1 = STRING: "Off"
    
    .1.3.6.1.4.1.24734.16.5.1.1.3.1.0 = STRING: "IA"
    .1.3.6.1.4.1.24734.16.5.1.1.3.1.1 = STRING: "IB"
    .1.3.6.1.4.1.24734.16.5.1.1.3.18.0 = STRING: "T1"
    .1.3.6.1.4.1.24734.16.5.1.1.3.18.1 = STRING: "H2"
    
    .1.3.6.1.4.1.24734.16.5.1.1.4.1.0 = STRING: "POWER INPUT A - FUSE BOX F7"
    .1.3.6.1.4.1.24734.16.5.1.1.4.1.1 = STRING: "POWER INPUT B - FUSE BOX F8"
    .1.3.6.1.4.1.24734.16.5.1.1.4.18.0 = STRING: "TEMPERATURE SENSOR"
    .1.3.6.1.4.1.24734.16.5.1.1.4.18.1 = STRING: "HUMIDITY SENSOR"
    
    .1.3.6.1.4.1.24734.16.5.1.1.6.1.0 = INTEGER: 0
    .1.3.6.1.4.1.24734.16.5.1.1.6.1.1 = INTEGER: 0
    .1.3.6.1.4.1.24734.16.5.1.1.6.18.0 = INTEGER: 23
    .1.3.6.1.4.1.24734.16.5.1.1.6.18.1 = INTEGER: 27    
    '''
    register_snmpwalk_ouput(walk)
    start_server()

# integration test
def test_system_call(capsys):
    # without options
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_eps_plus/check_snmp_eps_plus.py", shell=True,
                         stderr=subprocess.PIPE)
    assert "Hostname must be specified\n" in p.stderr.read()

    # with --help
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_eps_plus/check_snmp_eps_plus.py --help",
                         shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()

    # without check type
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_eps_plus/check_snmp_eps_plus.py -H 127.0.0.1",
        shell=True, stdout=subprocess.PIPE)
    assert "Please select --" in p.stdout.read()


def test_snmpv3(capsys):
    """not reachable"""

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_eps_plus/check_snmp_eps_plus.py' + " -H 1.2.3.4 -V 3 "
                                                                         "-U nothinguseful -L authNoPriv -a MD5 "
                                                                         "-A nothinguseful -x DES -X nothinguseful --sensor T1 --snmptimeout 3",
        shell=True, stdout=subprocess.PIPE)
    output = p.stdout.read() 
    assert "No response from device for Sensor IDs" in output or "Unknown - Plugin timeout exceeded after" in output


def test_plugin_timeout(capsys):
    """snmptimeout higher than plugin timeout"""
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_eps_plus/check_snmp_eps_plus.py -H localhost:1235 --device 0 --outlet 0 --timeout 10 --snmptimeout 15",
        shell=True, stdout=subprocess.PIPE)
    assert "Unknown - Plugin timeout exceeded after" in p.stdout.read()

def test_snmp_timeout(capsys):
    """snmptimeout higher than plugin timeout"""
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_eps_plus/check_snmp_eps_plus.py -H localhost:1235 --device 0 --outlet 0 --timeout 15 --snmptimeout 2",
        shell=True, stdout=subprocess.PIPE)
    assert "Unknown - No response from device for oid" in p.stdout.read()

def test_snmp_retries(capsys):
    """snmp restries -> timeout = 15 + snmp_timeout = 5 + retries = 5 ---> plugin timeout"""
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_eps_plus/check_snmp_eps_plus.py -H localhost:1235 --device 0 --outlet 0 --timeout 15 --snmptimeout 2 --retries 5",
        shell=True, stdout=subprocess.PIPE)
    assert "Unknown - Plugin timeout exceeded after" in p.stdout.read()

def test_outlet_on(capsys):
    """outlet is on"""
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_eps_plus/check_snmp_eps_plus.py -H localhost:1234 --device 0 --outlet 0",
        shell=True, stdout=subprocess.PIPE)
    assert "OK - Master - Outlet 1x: On" in p.stdout.read()


def test_outlet_off(capsys):
    """outlet is off"""
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_eps_plus/check_snmp_eps_plus.py -H localhost:1234 --device 1 --outlet 1",
        shell=True, stdout=subprocess.PIPE)
    assert "Critical - Slave - Outlet 1x 2x: Off" in p.stdout.read()


def test_sensor_not_available(capsys):
    """sensor not available"""
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_eps_plus/check_snmp_eps_plus.py -H localhost:1234 --sensor H99",
        shell=True, stdout=subprocess.PIPE)
    result = p.stdout.read()
    print result
    assert "Unknown - Sensor not found" in result


def test_sensor_ok(capsys):
    """sensor warning"""
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_eps_plus/check_snmp_eps_plus.py -H localhost:1234 --sensor T1 --threshold metric='TEMPERATURE SENSOR (in deg. C)',warning=:20,critical=:30",
        shell=True, stdout=subprocess.PIPE)
    result = p.stdout.read()
    print result
    assert "Warning - temperature sensor: 23 deg. C. Warning on temperature sensor (in deg. c)" in result

def test_stop():
    # stop the testagent
    stop_server()
