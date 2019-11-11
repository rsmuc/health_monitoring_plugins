#!/usr/bin/python
import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_idrac'))

import context
import netsnmp
#from check_snmp_idrac import *
import health_monitoring_plugins.idrac
from health_monitoring_plugins.idrac import *

import pytest

import subprocess
from testagent import *

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address = "localhost:1234", rocommunity='public', rwcommunity='private')

# create netsnmp Sessions for test_get and test_walk
session = netsnmp.Session(Version=2, DestHost='localhost', Community='public')
failSession = netsnmp.Session(Version=2, DestHost='1.2.3.4', Community='public')


def test_start():
    start_server()

def test_everything_ok():
 # start the testagent
    # Gauge32 are not working - So I replaced them by INTEGER
    # Dell PowerEdge R420xr.1

    register_snmpwalk_ouput('''iso.3.6.1.2.1.1.5.0 = STRING: "iDRAC NAME"''')  # name of the device

    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.2.1 = STRING: "Physical Disk 0:1:0"''')  # device name
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.4.1 = STRING: "3"''')  ## device status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.31.1 = STRING: "0"''')  ## predictive status


    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.7.1 = STRING: "Main System Chassis"''')# user assigned name of the system chassis
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.9.1 = STRING: "PowerEdge R420xr"''')# system model type of the system chassis
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.300.10.1.11.1 = STRING: "ABCD123"''')# service tag name of the chassis
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.1.0 = INTEGER: 3''')# overall rollup status of all components
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.2.0 = INTEGER: 3''')# system status as it is reflected by the LCD front panel
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.3.0 = INTEGER: 3''')# overall storage status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.2.4.0 = INTEGER: 4''')# power state of the system


    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.12.1.5.1.1 = INTEGER: 3''')  # power  unit status 1
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.12.1.5.1.2 = INTEGER: 3''') # power unit status 2

    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.12.1.8.1.1 = STRING: PS1 Status''')  # power unit location 1
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.12.1.8.1.2 = STRING: PS2 Status''')  # power unit location 2

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



    # with -H 1.2.3.4 (unknown host)
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_idrac/check_snmp_idrac.py -H 1.2.3.4', shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print 'With unknown host:\n' + cmd_output
    assert 'Unknown - No response from device for oid .1.3.6.1.2.1.1.5.0' in cmd_output
    
    # with -H 127.0.0.1:1234 (known host)
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_idrac/check_snmp_idrac.py -H localhost:1234', shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print 'With known host:\n' + cmd_output
    assert 'OK - Name: iDRAC NAME - Typ: PowerEdge R420xr - Service tag: ABCD123' in cmd_output
    
    #with --help
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_idrac/check_snmp_idrac.py -H localhost:1234 --help', shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print '--help:\n' + cmd_output
    assert 'Options:\n  -h, --help' in cmd_output


def test_snmpv3(capsys):
    # not reachable

    p = subprocess.Popen('health_monitoring_plugins/check_snmp_idrac/check_snmp_idrac.py' + " -H 1.2.3.4 -V 3 "
                                                     "-U nothinguseful -L authNoPriv -a MD5 "
                                                     "-A nothinguseful -x DES -X nothinguseful --snmptimeout 3",
                         shell=True, stdout=subprocess.PIPE)
    assert "Unknown - No response from device for oid .1.3.6.1.2.1.1.5.0" in p.stdout.read()



def test_everything_not_ok():
    """
    every status is not ok
    """


    unregister_all()

    register_snmpwalk_ouput('''iso.3.6.1.2.1.1.5.0 = STRING: "iDRAC NAME"''')  # name of the device
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.2.1 = STRING: "Physical Disk 0:1:0"''')  # device name
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.4.1 = STRING: "7"''')  ## device status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.31.1 = STRING: "1"''')  ## predictive status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.12.1.5.1.1 = INTEGER: 5''')  # power  unit status 1
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.12.1.5.1.2 = INTEGER: 5''')  # power unit status 2
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.12.1.8.1.1 = STRING: PS1 Status''')  # power unit location 1
    register_snmpwalk_ouput('''iso.3.6.1.4.1.674.10892.5.4.600.12.1.8.1.2 = STRING: PS2 Status''')  # power unit location 2

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
    stop_server()
    assert "Critical - Name: iDRAC NAME - Typ: PowerEdge R420xr - Service tag: ABCD123. Device status 'global': critical. System power status: 'off'. Storage status 'global': critical. LCD status 'global': critical. Drive 'Physical Disk 0:1:0': failed. Predictve Drive Status 'Physical Disk 0:1:0': predictive failure - replace drive. Power unit 'PS1 Status': critical. Power unit 'PS2 Status': critical. Power unit 'PS1 Status' redundancy: lost. Chassis intrusion sensor 'System Board Intrusion': critical. Cooling unit 'System Board Fan Redundancy': critical. Temperature sensor 'System Board Inlet Temp': criticalUpper. Temperature sensor 'CPU 1': criticalUpper. Temperature sensor 'Inlet Temperature': criticalUpper | 'System Board Inlet Temp -Celsius-'=27.0;;;;" in cmd_output


# Unittests
def test_normal_check():
    assert normal_check("Test123", "1", "Testdevice") == (2, "Testdevice 'Test123': other")

def test_normal_check_warning():
    assert normal_check("Test123", "4", "Testdevice") == (1, "Testdevice 'Test123': warning")

def test_probe_check():
    assert probe_check("Test123", "1", "Testdevice") == (2, "Testdevice 'Test123': other")

def test_check_drives():
    idrac = health_monitoring_plugins.idrac.Idrac(None)
    assert idrac.check_drives("123", "2") == (0, "Drive '123': ready")



#
# def test_power_unit_critical():
#     """
#     power unit redundancy status is: lost
#     """
#
#     power_unit_summary, power_unit_long = power_unit_check([3], ['power unit'],[5])
#
#     print 'summary: %s' % power_unit_summary
#     print 'long: %s' % power_unit_long
#
#     assert 'Power unit "power unit": critical' in power_unit_summary
#     assert 'Power unit "power unit": critical. Power redundancy status: full' in power_unit_long
#
# def test_redundancy_lost():
#     """
#     power unit redundancy status is: lost
#     """
#
#     power_unit_summary, power_unit_long = power_unit_check([5], ['power unit'],[3])
#
#     print 'summary: %s' % power_unit_summary
#     print 'long: %s' % power_unit_long
#
#     assert 'Power redundancy status: lost' in power_unit_summary
#     assert 'Power unit "power unit": ok. Power redundancy status: lost' in power_unit_long
#
# def test_chassis_critical():
#     """
#     chassis intrusion status is critical
#     """
#
#     chassis_summary, chassis_long = chassis_intrusion_check([5], ['Board Intrusion'])
#
#     print 'summary: %s' % chassis_summary
#     print 'long: %s' % chassis_long
#
#     assert 'Chassis intrusion sensor "Board Intrusion" is critical' in chassis_summary
#     assert 'Chassis intrusion sensor "Board Intrusion" is critical' in chassis_long
#
# def test_cooling_unit_critical():
#     """
#     cooling unit status critical
#     """
#
#     cooling_summary, cooling_long = cooling_unit_check(['System Board Fan'], [5])
#
#     print 'summary: %s' % cooling_summary
#     print 'long: %s' % cooling_long
#
#     assert 'Cooling unit "System Board Fan" status: critical' in cooling_summary
#     assert 'Cooling unit "System Board Fan" status: critical' in cooling_long

def test_stop():
    stop_server()