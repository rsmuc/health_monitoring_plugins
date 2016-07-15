#!/usr/bin/python
import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_idrac'))

from check_snmp_idrac import *

import pytest
import subprocess
from testagent import *

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address = "localhost:1234", rocommunity='public', rwcommunity='private')

# create netsnmp Sessions for test_get and test_walk
session = netsnmp.Session(Version=2, DestHost='localhost', Community='public')
failSession = netsnmp.Session(Version=2, DestHost='1.2.3.4', Community='public')

def get_system_uptime():
    """
    just a helper to get the system uptime in seconds
    """
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = str(f.readline().split()[0])
        uptime_seconds = uptime_seconds.replace('.', '')
        return str(uptime_seconds)

def test_get(capsys):
    """
    test of the get_data function
    """
    # run a get on a not existing host
    with pytest.raises(SystemExit):
        get_data(failSession, '.1', helper)
    out, err = capsys.readouterr()    
    assert 'Unknown - snmpget failed - no data for host' in out
    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert get_data(session, '.1.3.6.1.2.1.25.1.1.0', helper)[:-2] == get_system_uptime()[:-2]

def test_walk(capsys):
    """
    test of the walk_data function
    """
    # run a walk on a not existing host
    with pytest.raises(SystemExit):
        assert walk_data(failSession, '.1', helper)
    out, err = capsys.readouterr()
    assert 'Unknown - snmpwalk failed - no data for host' in out
    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert walk_data(session, '.1.3.6.1.2.1.25.1.1', helper)[0][0][:-3] == get_system_uptime()[:-3]

def test_start():
 # start the testagent
    # Gauge32 are not working - So I replaced them by INTEGER
    # Dell PowerEdge R420xr
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.7.1 = STRING: "Main System Chassis"''')# user assigned name of the system chassis
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.9.1 = STRING: "PowerEdge R420xr"''')# system model type of the system chassis
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.11.1 = STRING: "ABCD123"''')# service tag name of the chassis
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.1.0 = INTEGER: 3''')# overall rollup status of all components
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.2.0 = INTEGER: 3''')# system status as it is reflected by the LCD front panel
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.3.0 = INTEGER: 3''')# overall storage status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.4.0 = INTEGER: 4''')# power state of the system
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.10.1.5.1 = INTEGER: 3''')# redundancy status of the power unit
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.10.1.7.1 = STRING: "System Board PS Redundancy"''')# name of the power unit
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.10.1.8.1 = INTEGER: 3''')# status of the power unit
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.70.1.5.1 = INTEGER: 3''')# status of the intrusion sensor
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.70.1.8.1 = STRING: "System Board Intrusion"''')# location of the intrusion sensor
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.10.1.7.1 = STRING: "System Board Fan Redundancy"''')# name of the cooling unit
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.10.1.8.1 = INTEGER: 3''')# status of the cooling unit
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.5.1.1 = INTEGER: 3''')# status of the temperature probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.8.1.1 = STRING: "System Board Inlet Temp"''')# location name of the temperature probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.5.1.2 = INTEGER: 3''')# status of the temperature probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.8.1.2 = STRING: "CPU 1"''')# location name of the temperature probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.5.1.3 = INTEGER: 3''')# status of the temperature probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.6.1.3 = INTEGER: 270''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.8.1.3 = STRING: "Inlet Temperature"''')# location name of the temperature probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.5.1.1 = INTEGER: 3''')# status of the voltage probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.6.1.1 = INTEGER: 228000''')# voltage probe reading
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.8.1.1 = STRING: "PS 1 Voltage"''')# location name of the voltage probe
    
    start_server()

def test_system_test_idrac():
    # with -H 1.2.3.4 (unknown host)
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_idrac/check_snmp_idrac.py -H 1.2.3.4', shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print 'With unknown host:\n' + cmd_output
    assert 'Unknown - snmpget failed - no data for host 1.2.3.4' in cmd_output
    
    # with -H 127.0.0.1:1234 (known host)
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_idrac/check_snmp_idrac.py -H localhost:1234', shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print 'With known host:\n' + cmd_output
    assert 'OK - User assigned name: Main System Chassis - Typ: PowerEdge R420xr - Service tag: ABCD123' in cmd_output
    
    #with --help
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_idrac/check_snmp_idrac.py -H localhost:1234 --help', shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print '--help:\n' + cmd_output
    assert 'Options:\n  -h, --help' in cmd_output
    
def test_everything_not_ok():
    """
    every status is not ok
    """
    
    unregister_all()
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.7.1 = STRING: "Main System Chassis"''')# user assigned name of the system chassis
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.9.1 = STRING: "PowerEdge R420xr"''')# system model type of the system chassis
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.11.1 = STRING: "ABCD123"''')# service tag name of the chassis
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.1.0 = INTEGER: 5''')# overall rollup status of all components
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.2.0 = INTEGER: 5''')# system status as it is reflected by the LCD front panel
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.3.0 = INTEGER: 5''')# overall storage status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.4.0 = INTEGER: 3''')# power state of the system
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.10.1.5.1 = INTEGER: 5''')# redundancy status of the power unit
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.10.1.7.1 = STRING: "System Board PS Redundancy"''')# name of the power unit
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.10.1.8.1 = INTEGER: 5''')# status of the power unit
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.70.1.5.1 = INTEGER: 5''')# status of the intrusion sensor
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.70.1.8.1 = STRING: "System Board Intrusion"''')# location of the intrusion sensor
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.10.1.7.1 = STRING: "System Board Fan Redundancy"''')# name of the cooling unit
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.10.1.8.1 = INTEGER: 5''')# status of the cooling unit
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.5.1.1 = INTEGER: 5''')# status of the temperature probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.8.1.1 = STRING: "System Board Inlet Temp"''')# location name of the temperature probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.5.1.2 = INTEGER: 5''')# status of the temperature probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.8.1.2 = STRING: "CPU 1"''')# location name of the temperature probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.5.1.3 = INTEGER: 5''')# status of the temperature probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.6.1.3 = INTEGER: 270''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.8.1.3 = STRING: "Inlet Temperature"''')# location name of the temperature probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.5.1.1 = INTEGER: 5''')# status of the voltage probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.6.1.1 = INTEGER: 228000''')# voltage probe reading
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.8.1.1 = STRING: "PS 1 Voltage"''')# location name of the voltage probe
    
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_idrac/check_snmp_idrac.py -H localhost:1234', shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Critical - User assigned name: Main System Chassis - Typ: PowerEdge R420xr - Service tag: ABCD123. Global System status:\
 critical. System LCD status: critical. Global Storage status: critical. System Power status: off. Power unit "System Board PS\
 Redundancy" status: critical. Redundancy: lost. Chassis intrusion sensor "System Board Intrusion" is critical.\
 Cooling unit "System Board Fan Redundancy" status: critical. Temperature probe at "inlet temperature" is\
 criticalUpper. Voltage probe at "ps 1 voltage" is criticalUpper' in cmd_output
    
def test_overall_state_critical():
    """
    overall states are critical. overall rollup status, LCD system status, overall storage status, power state
    """
    
    unregister_all()
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.7.1 = STRING: "Main System Chassis"''')# user assigned name of the system chassis
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.9.1 = STRING: "PowerEdge R420xr"''')# system model type of the system chassis
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.11.1 = STRING: "ABCD123"''')# service tag name of the chassis
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.1.0 = INTEGER: 5''')# overall rollup status of all components
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.2.0 = INTEGER: 5''')# system status as it is reflected by the LCD front panel
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.3.0 = INTEGER: 5''')# overall storage status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.4.0 = INTEGER: 3''')# power state of the system
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.10.1.5.1 = INTEGER: 3''')# redundancy status of the power unit
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.10.1.7.1 = STRING: "System Board PS Redundancy"''')# name of the power unit
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.10.1.8.1 = INTEGER: 3''')# status of the power unit
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.70.1.5.1 = INTEGER: 3''')# status of the intrusion sensor
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.70.1.8.1 = STRING: "System Board Intrusion"''')# location of the intrusion sensor
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.10.1.7.1 = STRING: "System Board Fan Redundancy"''')# name of the cooling unit
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.10.1.8.1 = INTEGER: 3''')# status of the cooling unit
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.5.1.1 = INTEGER: 3''')# status of the temperature probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.8.1.1 = STRING: "System Board Inlet Temp"''')# location name of the temperature probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.5.1.2 = INTEGER: 3''')# status of the temperature probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.8.1.2 = STRING: "CPU 1"''')# location name of the temperature probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.5.1.3 = INTEGER: 3''')# status of the temperature probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.6.1.3 = INTEGER: 270''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.8.1.3 = STRING: "Inlet Temperature"''')# location name of the temperature probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.5.1.1 = INTEGER: 3''')# status of the voltage probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.6.1.1 = INTEGER: 228000''')# voltage probe reading
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.8.1.1 = STRING: "PS 1 Voltage"''')# location name of the voltage probe
    
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_idrac/check_snmp_idrac.py -H localhost:1234', shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Critical - User assigned name: Main System Chassis - Typ: PowerEdge R420xr - Service tag: ABCD123. Global System status:\
 critical. System LCD status: critical. Global Storage status: critical. System Power status: off' in cmd_output
    
def test_power_unit_critical():
    """
    power unit redundancy status is: lost
    """
    
    power_unit_summary, power_unit_long = power_unit_check([3], ['power unit'],[5])
    
    print 'summary: %s' % power_unit_summary
    print 'long: %s' % power_unit_long
    
    assert 'Power unit "power unit" status: critical. Redundancy: full' in power_unit_summary
    assert 'Power unit "power unit" status: critical. Redundancy: full' in power_unit_long
    
def test_redundancy_lost():
    """
    power unit redundancy status is: lost
    """
    
    power_unit_summary, power_unit_long = power_unit_check([5], ['power unit'],[3])
    
    print 'summary: %s' % power_unit_summary
    print 'long: %s' % power_unit_long
    
    assert 'Power unit "power unit" status: ok. Redundancy: lost' in power_unit_summary
    assert 'Power unit "power unit" status: ok. Redundancy: lost' in power_unit_long
    
def test_chassis_critical():
    """
    chassis intrusion status is critical
    """
    
    chassis_summary, chassis_long = chassis_intrusion_check([5], ['Board Intrusion'])
    
    print 'summary: %s' % chassis_summary
    print 'long: %s' % chassis_long
    
    assert 'Chassis intrusion sensor "Board Intrusion" is critical' in chassis_summary
    assert 'Chassis intrusion sensor "Board Intrusion" is critical' in chassis_long
    
def test_cooling_unit_critical():
    """
    cooling unit status critical
    """
    
    cooling_summary, cooling_long = cooling_unit_check(['System Board Fan'], [5])
    
    print 'summary: %s' % cooling_summary
    print 'long: %s' % cooling_long
    
    assert 'Cooling unit "System Board Fan" status: critical' in cooling_summary
    assert 'Cooling unit "System Board Fan" status: critical' in cooling_long
    
def test_temperature_probe_critical():
    """
    temperature probe 'inlet temperature' status criticalUpper
    """
    
    unregister_all()
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.7.1 = STRING: "Main System Chassis"''')# user assigned name of the system chassis
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.9.1 = STRING: "PowerEdge R420xr"''')# system model type of the system chassis
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.11.1 = STRING: "ABCD123"''')# service tag name of the chassis
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.1.0 = INTEGER: 3''')# overall rollup status of all components
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.2.0 = INTEGER: 3''')# system status as it is reflected by the LCD front panel
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.3.0 = INTEGER: 3''')# overall storage status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.4.0 = INTEGER: 4''')# power state of the system
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.10.1.5.1 = INTEGER: 3''')# redundancy status of the power unit
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.10.1.7.1 = STRING: "System Board PS Redundancy"''')# name of the power unit
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.10.1.8.1 = INTEGER: 3''')# status of the power unit
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.70.1.5.1 = INTEGER: 3''')# status of the intrusion sensor
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.70.1.8.1 = STRING: "System Board Intrusion"''')# location of the intrusion sensor
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.10.1.7.1 = STRING: "System Board Fan Redundancy"''')# name of the cooling unit
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.10.1.8.1 = INTEGER: 3''')# status of the cooling unit
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.5.1.1 = INTEGER: 3''')# status of the temperature probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.6.1.1 = INTEGER: 270''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.8.1.1 = STRING: "System Board Inlet Temp"''')# location name of the temperature probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.5.1.2 = INTEGER: 3''')# status of the temperature probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.8.1.2 = STRING: "CPU 1"''')# location name of the temperature probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.5.1.3 = INTEGER: 5''')# status of the temperature probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.6.1.3 = INTEGER: 270''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.8.1.3 = STRING: "Inlet Temperature"''')# location name of the temperature probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.5.1.1 = INTEGER: 5''')# status of the voltage probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.6.1.1 = INTEGER: 228000''')# voltage probe reading
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.8.1.1 = STRING: "PS 1 Voltage"''')# location name of the voltage probe
    
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_idrac/check_snmp_idrac.py -H localhost:1234', shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Temperature probe at "inlet temperature" is criticalUpper. ' in cmd_output
    
def test_voltage_probe_ciritcal():
    """
    voltage probe 'ps 2 voltage' status criticalUpper
    """
    
    unregister_all()
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.7.1 = STRING: "Main System Chassis"''')# user assigned name of the system chassis
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.9.1 = STRING: "PowerEdge R420xr"''')# system model type of the system chassis
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.11.1 = STRING: "ABCD123"''')# service tag name of the chassis
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.1.0 = INTEGER: 3''')# overall rollup status of all components
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.2.0 = INTEGER: 3''')# system status as it is reflected by the LCD front panel
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.3.0 = INTEGER: 3''')# overall storage status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.4.0 = INTEGER: 4''')# power state of the system
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.10.1.5.1 = INTEGER: 3''')# redundancy status of the power unit
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.10.1.7.1 = STRING: "System Board PS Redundancy"''')# name of the power unit
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.10.1.8.1 = INTEGER: 3''')# status of the power unit
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.70.1.5.1 = INTEGER: 3''')# status of the intrusion sensor
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.70.1.8.1 = STRING: "System Board Intrusion"''')# location of the intrusion sensor
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.10.1.7.1 = STRING: "System Board Fan Redundancy"''')# name of the cooling unit
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.10.1.8.1 = INTEGER: 3''')# status of the cooling unit
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.5.1.1 = INTEGER: 3''')# status of the temperature probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.8.1.1 = STRING: "System Board Inlet Temp"''')# location name of the temperature probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.5.1.2 = INTEGER: 3''')# status of the temperature probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.8.1.2 = STRING: "CPU 1"''')# location name of the temperature probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.5.1.3 = INTEGER: 3''')# status of the temperature probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.6.1.3 = INTEGER: 270''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.700.20.1.8.1.3 = STRING: "Inlet Temperature"''')# location name of the temperature probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.5.1.1 = INTEGER: 3''')# status of the voltage probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.6.1.1 = INTEGER: 228000''')# voltage probe reading
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.8.1.1 = STRING: "PS 1 Voltage"''')# location name of the voltage probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.5.1.2 = INTEGER: 5''')# status of the voltage probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.6.1.2 = INTEGER: 241000''')# voltage probe reading
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.8.1.2 = STRING: "PS 2 Voltage"''')# location name of the voltage probe
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.5.1.3 = INTEGER: 3''')# status of the voltage probe
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.20.1.8.1.3 = STRING: "PS 3 Voltage"''')# location name of the voltage probe
    
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_idrac/check_snmp_idrac.py -H localhost:1234', shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Voltage probe at "ps 2 voltage" is criticalUpper' in cmd_output
    assert 'Critical on ps 2 voltage'
    
def test_stop():
    # stop the testagent
    stop_server()
