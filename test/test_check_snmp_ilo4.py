#!/usr/bin/python
import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_ilo4'))

from check_snmp_ilo4 import *

import pytest
import subprocess
from testagent import *
from types import MethodType

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address = "localhost:1234", rocommunity='public', rwcommunity='private')

def test_start():
 # start the testagent
    # Gauge32 are not working - So I replaced them by INTEGER
    # HP DL380 Gen 9 iLo 4 
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.4.2.0 = STRING: "ProLiant DL380 Gen9"''') # product name
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.2.1.0 = STRING: "CZJ1234567"''') # serial number
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.1.3.0 = INTEGER: 2''') # global storage status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.1.3.0 = INTEGER: 2''') # global system status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.1.0 = INTEGER: 2''') # global power supply status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.9.2.2.32.0 = INTEGER: 3''') # power status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.1.0 = INTEGER: 2''') # global temp status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.3.0 = INTEGER: 2''') # global temp sensor
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.4.0 = INTEGER: 2''') # global fan status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.14.4.0 = INTEGER: 2''') # global memory status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.2.1.1.6.0 = INTEGER: 2''') # global controller status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.1 = INTEGER: 2''') # physical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.1 = INTEGER: 2''') # drive smart status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.0 = INTEGER: 52''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.1 = INTEGER: 60''') # drive temperature
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.0 = INTEGER: 60''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.1 = INTEGER: 60''') # drive temperature threshold
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.3.1.1.4.0.1 = INTEGER: 2''') # logical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.1 = INTEGER: 20''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.2 = INTEGER: 40''') # environment temperatures
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.1 = INTEGER: 42''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.2 = INTEGER: 70''') # environment temperatures thresholds
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 2''') # fan status ok
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 2''') # fan status ok 
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status ok
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 2''') # power supply status ok
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 2''') # power supply status ok
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.1 = INTEGER: 3''') # power supply redundancy: redundant
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.2 = INTEGER: 3''') # power supply redundancy: redundant

    start_server()

def test_system_test_ilo4():
    # without options
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py', shell=True, stdout=subprocess.PIPE)
    assert 'Unknown - Hostname must be specified' in p.stdout.read()

    ## with -H 1.2.3.4 --scan (unknown host)
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H 1.2.3.4 --scan', shell=True, stdout=subprocess.PIPE)
    #snmpget failed - no data for OID- maybe wrong MIB version selected or snmp is disabled
    assert 'Unknown - snmpwalk failed - no data for host 1.2.3.4 ' in p.stdout.read()

    ## with -H 127.0.0.1:1234 --scan (known host)
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H 127.0.0.1:1234 --scan', shell=True, stdout=subprocess.PIPE)
    assert 'OK - \nAvailable devices:\n\nPhysical drive 1: ok\nPhysical drive 2: ok' in p.stdout.read()

    ## with -H 127.0.0.1:1234 --scan (check scan priority)
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=1 --drives=2 --fan=1 --scan', shell=True, stdout=subprocess.PIPE)
    assert 'OK - \nAvailable devices:\n\nPhysical drive 1: ok\nPhysical drive 2: ok' in p.stdout.read()

    # with --help
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py --help', shell=True, stdout=subprocess.PIPE)
    assert 'Options:\n  -h, --help' in p.stdout.read()

def test_with_host_ok():
    # everything ok (2 drives, 2 power supply running, 3 fan running)
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=2 --drives=2 --fan=3', shell=True, stdout=subprocess.PIPE)
    assert 'OK - ProLiant DL380 Gen9 - Serial number:CZJ1234567 | \'Environment Temperature\'=20Celsius;;:42;;\nGlobal storage status: ok \n\nGlobal system status: ok \n\nGloba' in p.stdout.read()

def test_with_everything_disabled():
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=0 --drives=0 --fan=0 --noStorage --noSystem --noPowerSupply --noPowerState --noTemp --noTempSens --noDriveTemp --noFan --noMemory --noController --noPowerRedundancy', shell=True, stdout=subprocess.PIPE)
    assert 'OK - ProLiant DL380 Gen9 - Serial number:CZJ1234567 | \'Environment Temperature\'=20Celsius;;:42;;\nTemperatu' in p.stdout.read()

def test_with_no_input():
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234', shell=True, stdout=subprocess.PIPE)
    assert 'Amount of physical drives must be specified (--drives)' in p.stdout.read()

def test_state_summary_ok():
    summary_output, long_output = state_summary(2, 'summary output', normal_state)
    assert 'status: ok' in long_output

def test_state_summary_failed():
    summary_output, long_output = state_summary(4, 'summary output', normal_state)
    assert 'status: failed' in long_output
    assert 'status: failed' in summary_output


##################
# FAN tests
##################

def test_with_less_fans():
    # 4 fans configured (2 drives, 2 power supply running, 3 fan running)
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=0 --drives=0 --fan=4', shell=True, stdout=subprocess.PIPE)
    assert "Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567. 4 fan(s) expected - 3 fan(s) ok." in p.stdout.read()
    

def test_one_fan_broken():
    """ 
    2 Fans ok; 1 Fan broken
    """
    
    unregister_all()
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.4.2.0 = STRING: "ProLiant DL380 Gen9"''') # product name
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.2.1.0 = STRING: "CZJ1234567"''') # serial number
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.1.3.0 = INTEGER: 2''') # global storage status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.1.3.0 = INTEGER: 2''') # global system status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.1.0 = INTEGER: 2''') # global power supply status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.9.2.2.32.0 = INTEGER: 3''') # power status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.1.0 = INTEGER: 2''') # global temp status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.3.0 = INTEGER: 2''') # global temp sensor
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.4.0 = INTEGER: 2''') # global fan status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.14.4.0 = INTEGER: 2''') # global memory status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.2.1.1.6.0 = INTEGER: 2''') # global controller status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.1 = INTEGER: 2''') # physical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.1 = INTEGER: 2''') # drive smart status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.0 = INTEGER: 52''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.1 = INTEGER: 60''') # drive temperature
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.0 = INTEGER: 60''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.1 = INTEGER: 60''') # drive temperature threshold
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.3.1.1.4.0.1 = INTEGER: 2''') # logical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.1 = INTEGER: 20''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.2 = INTEGER: 40''') # environment temperatures
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.1 = INTEGER: 42''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.2 = INTEGER: 70''') # environment temperatures thresholds
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 2''') # fan status ok
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 3''') # fan status not ok
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status ok
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 2''') # power supply status ok
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 2''') # power supply status ok
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.1 = INTEGER: 3''') # power supply redundancy: redundant
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.2 = INTEGER: 3''') # power supply redundancy: redundant

    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=0 --drives=0 --fan=3', shell=True, stdout=subprocess.PIPE)
    assert 'Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567. 3 fan(s) expected - 2 fan(s) ok.' in p.stdout.read()


####################
# Power Supply Tests
####################

def test_with_less_power_supplies():
    # 4 power supplies configured, 2 power supplies running    
    unregister_all()
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.4.2.0 = STRING: "ProLiant DL380 Gen9"''') # product name
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.2.1.0 = STRING: "CZJ1234567"''') # serial number
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.1.3.0 = INTEGER: 2''') # global storage status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.1.3.0 = INTEGER: 2''') # global system status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.1.0 = INTEGER: 2''') # global power supply status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.9.2.2.32.0 = INTEGER: 3''') # power status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.1.0 = INTEGER: 2''') # global temp status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.3.0 = INTEGER: 2''') # global temp sensor
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.4.0 = INTEGER: 2''') # global fan status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.14.4.0 = INTEGER: 2''') # global memory status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.2.1.1.6.0 = INTEGER: 2''') # global controller status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.1 = INTEGER: 2''') # physical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.1 = INTEGER: 2''') # drive smart status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.0 = INTEGER: 52''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.1 = INTEGER: 60''') # drive temperature
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.0 = INTEGER: 60''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.1 = INTEGER: 60''') # drive temperature threshold
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.3.1.1.4.0.1 = INTEGER: 2''') # logical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.1 = INTEGER: 20''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.2 = INTEGER: 40''') # environment temperatures
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.1 = INTEGER: 42''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.2 = INTEGER: 70''') # environment temperatures thresholds
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 2''') # fan status ok
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 3''') # fan status not ok
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status ok
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 2''') # power supply status ok
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 2''') # power supply status ok
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.1 = INTEGER: 2''') # power supply redundancy: not redundant
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.2 = INTEGER: 2''') # power supply redundancy: not redundant

    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=4 --drives=0 --fan=0', shell=True, stdout=subprocess.PIPE)
    assert "Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567. 4 power supplies expected - 2 power supplies ok" in p.stdout.read()

def test_with_power_supplies_not_redundant():
    # 2 power supplies configured, 2 power supplies running, not redundant, but not chek disabled
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=2 --drives=0 --fan=0', shell=True, stdout=subprocess.PIPE)
    assert "Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567. Power supply 1: notRedundant. Power supply 2: notRedundant" in p.stdout.read()

def test_power_suppply_redundancy_check_disabled():
    # 2 power supplies configured, 2 power supplies running, not redundant, but not chek disabled
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=2 --drives=0 --fan=0 --noPowerRedundancy', shell=True, stdout=subprocess.PIPE)
    assert "OK - ProLiant DL380 Gen9 - Serial number:CZJ1234567" in p.stdout.read()

def test_power_supply_brolen():
    # 2 power supplies configured, 1 power suppliy running, 1 degraded
    unregister_all()
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.4.2.0 = STRING: "ProLiant DL380 Gen9"''') # product name
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.2.1.0 = STRING: "CZJ1234567"''') # serial number
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.1.3.0 = INTEGER: 2''') # global storage status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.1.3.0 = INTEGER: 2''') # global system status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.1.0 = INTEGER: 2''') # global power supply status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.9.2.2.32.0 = INTEGER: 3''') # power status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.1.0 = INTEGER: 2''') # global temp status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.3.0 = INTEGER: 2''') # global temp sensor
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.4.0 = INTEGER: 2''') # global fan status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.14.4.0 = INTEGER: 2''') # global memory status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.2.1.1.6.0 = INTEGER: 2''') # global controller status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.1 = INTEGER: 2''') # physical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.1 = INTEGER: 2''') # drive smart status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.0 = INTEGER: 52''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.1 = INTEGER: 60''') # drive temperature
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.0 = INTEGER: 60''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.1 = INTEGER: 60''') # drive temperature threshold
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.3.1.1.4.0.1 = INTEGER: 2''') # logical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.1 = INTEGER: 20''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.2 = INTEGER: 40''') # environment temperatures
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.1 = INTEGER: 42''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.2 = INTEGER: 70''') # environment temperatures thresholds
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 2''') # fan status ok
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 3''') # fan status not ok
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status ok
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 2''') # power supply status not ok
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 3''') # power supply status not ok   

    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.1 = INTEGER: 2''') # power supply redundancy: not redundant
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.2 = INTEGER: 2''') # power supply redundancy: not redundant

    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=2 --drives=0 --fan=0 --noPowerRedundancy', shell=True, stdout=subprocess.PIPE)
    assert "Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567. Power supply status 2: degraded." in p.stdout.read()

####################
# DRIVE Tests
####################


def test_with_less_drives():
    # 4 drives configured (2 drives, 1 power supply running, 1 fan running)
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=0 --drives=4 --fan=0 --noPowerRedundancy', shell=True, stdout=subprocess.PIPE)
    output = p.stdout.read()
    assert '4 physical drive(s) expected - 2 physical drive(s) in ok' in output

def test_with_drives_disabled():
    # no drives configured (2 drives, 1 power supply running, 1 fan running)
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=0 --drives=0 --fan=0 --noPowerRedundancy', shell=True, stdout=subprocess.PIPE)
    output = p.stdout.read()
    assert 'OK - ProLiant DL380 Gen9 - Serial number:CZJ1234567 | \'Environment Temperature\'=20Celsius;;:42;;\nGlobal storage status: ok \n\nGlobal system status: ok' in output

def test_smart_broken():
    
    unregister_all()
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.4.2.0 = STRING: "ProLiant DL380 Gen9"''') # product name
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.2.1.0 = STRING: "CZJ1234567"''') # serial number
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.1.3.0 = INTEGER: 2''') # global storage status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.1.3.0 = INTEGER: 2''') # global system status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.1.0 = INTEGER: 2''') # global power supply status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.9.2.2.32.0 = INTEGER: 3''') # power status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.1.0 = INTEGER: 2''') # global temp status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.3.0 = INTEGER: 2''') # global temp sensor
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.4.0 = INTEGER: 2''') # global fan status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.14.4.0 = INTEGER: 2''') # global memory status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.2.1.1.6.0 = INTEGER: 2''') # global controller status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.1 = INTEGER: 2''') # physical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.1 = INTEGER: 3''') # drive smart status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.0 = INTEGER: 52''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.1 = INTEGER: 60''') # drive temperature
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.0 = INTEGER: 60''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.1 = INTEGER: 60''') # drive temperature threshold
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.3.1.1.4.0.1 = INTEGER: 2''') # logical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.1 = INTEGER: 20''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.2 = INTEGER: 40''') # environment temperatures
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.1 = INTEGER: 42''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.2 = INTEGER: 70''') # environment temperatures thresholds
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 2''') # power supply status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.1 = INTEGER: 3''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.2 = INTEGER: 3''') # power supply redundancy

    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=0 --drives=2 --fan=0', shell=True, stdout=subprocess.PIPE)
    assert 'Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567. Physical drive 2 status: ok Physical drive 2 smart status' in p.stdout.read()

def test_drive_status_broken():
    
    unregister_all()
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.4.2.0 = STRING: "ProLiant DL380 Gen9"''') # product name
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.2.1.0 = STRING: "CZJ1234567"''') # serial number
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.1.3.0 = INTEGER: 2''') # global storage status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.1.3.0 = INTEGER: 2''') # global system status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.1.0 = INTEGER: 2''') # global power supply status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.9.2.2.32.0 = INTEGER: 3''') # power status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.1.0 = INTEGER: 2''') # global temp status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.3.0 = INTEGER: 2''') # global temp sensor
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.4.0 = INTEGER: 2''') # global fan status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.14.4.0 = INTEGER: 2''') # global memory status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.2.1.1.6.0 = INTEGER: 2''') # global controller status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.0 = INTEGER: 3''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.1 = INTEGER: 3''') # physical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.1 = INTEGER: 3''') # drive smart status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.0 = INTEGER: 52''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.1 = INTEGER: 60''') # drive temperature
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.0 = INTEGER: 60''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.1 = INTEGER: 60''') # drive temperature threshold
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.3.1.1.4.0.1 = INTEGER: 2''') # logical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.1 = INTEGER: 20''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.2 = INTEGER: 40''') # environment temperatures
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.1 = INTEGER: 42''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.2 = INTEGER: 70''') # environment temperatures thresholds
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 2''') # power supply status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.1 = INTEGER: 3''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.2 = INTEGER: 3''') # power supply redundancy

    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=0 --drives=2 --fan=0', shell=True, stdout=subprocess.PIPE)
    assert 'Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567. Physical drive 1 status: failed Physical drive 1 smart sta' in p.stdout.read()

def test_logical_drive_broken():    
    unregister_all()
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.4.2.0 = STRING: "ProLiant DL380 Gen9"''') # product name
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.2.1.0 = STRING: "CZJ1234567"''') # serial number
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.1.3.0 = INTEGER: 2''') # global storage status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.1.3.0 = INTEGER: 2''') # global system status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.1.0 = INTEGER: 2''') # global power supply status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.9.2.2.32.0 = INTEGER: 3''') # power status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.1.0 = INTEGER: 2''') # global temp status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.3.0 = INTEGER: 2''') # global temp sensor
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.4.0 = INTEGER: 2''') # global fan status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.14.4.0 = INTEGER: 2''') # global memory status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.2.1.1.6.0 = INTEGER: 2''') # global controller status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.1 = INTEGER: 2''') # physical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.1 = INTEGER: 2''') # drive smart status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.0 = INTEGER: 52''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.1 = INTEGER: 60''') # drive temperature
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.0 = INTEGER: 60''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.1 = INTEGER: 60''') # drive temperature threshold
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.3.1.1.4.0.1 = INTEGER: 3''') # logical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.1 = INTEGER: 20''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.2 = INTEGER: 40''') # environment temperatures
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.1 = INTEGER: 42''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.2 = INTEGER: 70''') # environment temperatures thresholds
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 2''') # power supply status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.1 = INTEGER: 3''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.2 = INTEGER: 3''') # power supply redundancy

    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=0 --drives=2 --fan=0', shell=True, stdout=subprocess.PIPE)
    assert 'Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567. Logical drive 1 status: failed' in p.stdout.read()


def test_zero_phy_drv():
    unregister_all()

    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.4.2.0 = STRING: "ProLiant DL380 Gen9"''') # product name
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.2.1.0 = STRING: "CZJ1234567"''') # serial number
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 1''') # power supply status
    
    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --scan', shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    assert 'No physical drives detected' in cmd_output    
    assert 'Available devices:' in cmd_output


######################
# Global Status Tests
######################

def test_all_global_status_broken():
    
    unregister_all()
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.4.2.0 = STRING: "ProLiant DL380 Gen9"''') # product name
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.2.1.0 = STRING: "CZJ1234567"''') # serial number
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.1.3.0 = INTEGER: 1''') # global storage status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.1.3.0 = INTEGER: 1''') # global system status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.1.0 = INTEGER: 1''') # global power supply status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.9.2.2.32.0 = INTEGER: 1''') # power status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.1.0 = INTEGER: 1''') # global temp status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.3.0 = INTEGER: 1''') # global temp sensor
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.4.0 = INTEGER: 1''') # global fan status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.14.4.0 = INTEGER: 1''') # global memory status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.2.1.1.6.0 = INTEGER: 1''') # global controller status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.1 = INTEGER: 2''') # physical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.1 = INTEGER: 2''') # drive smart status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.0 = INTEGER: 52''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.1 = INTEGER: 60''') # drive temperature
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.0 = INTEGER: 60''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.1 = INTEGER: 60''') # drive temperature threshold
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.3.1.1.4.0.1 = INTEGER: 2''') # logical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.1 = INTEGER: 20''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.2 = INTEGER: 40''') # environment temperatures
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.1 = INTEGER: 42''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.2 = INTEGER: 70''') # environment temperatures thresholds
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 1''') # power supply status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.2 = INTEGER: 2''') # power supply redundancy

    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=1 --drives=2 --fan=1', shell=True, stdout=subprocess.PIPE)
    assert 'Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567. Global storage status: other. Global system status: other. Global power supply status: other. Overall thermal environment status: other. Temperature sensors status: other. Fan(s) status: other. Memory status: other. Server power status: unknown.' in p.stdout.read()


######################
# Temperature Tests
######################

def test_temp_high():
    unregister_all()
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.4.2.0 = STRING: "ProLiant DL380 Gen9"''') # product name
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.2.1.0 = STRING: "CZJ1234567"''') # serial number
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.1.3.0 = INTEGER: 2''') # global storage status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.1.3.0 = INTEGER: 2''') # global system status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.1.0 = INTEGER: 2''') # global power supply status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.9.2.2.32.0 = INTEGER: 3''') # power status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.1.0 = INTEGER: 2''') # global temp status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.3.0 = INTEGER: 2''') # global temp sensor
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.4.0 = INTEGER: 2''') # global fan status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.14.4.0 = INTEGER: 2''') # global memory status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.2.1.1.6.0 = INTEGER: 2''') # global controller status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.1 = INTEGER: 2''') # physical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.1 = INTEGER: 2''') # drive smart status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.0 = INTEGER: 75''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.1 = INTEGER: 60''') # drive temperature
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.0 = INTEGER: 60''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.1 = INTEGER: 60''') # drive temperature threshold
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.3.1.1.4.0.1 = INTEGER: 2''') # logical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.1 = INTEGER: 55''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.2 = INTEGER: 40''') # environment temperatures
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.1 = INTEGER: 42''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.2 = INTEGER: 70''') # environment temperatures thresholds
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 1''') # power supply status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.2 = INTEGER: 2''') # power supply redundancy

    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=1 --drives=2 --fan=1', shell=True, stdout=subprocess.PIPE)
    assert 'Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567. Physical drive 1 temperature above threshold (75 / 60).' in p.stdout.read()

    
def test_server_poweroff():
    """ 
    test if a powered off server is found
    """
    
    unregister_all()
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.4.2.0 = STRING: "ProLiant DL380 Gen9"''') # product name
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.2.2.2.1.0 = STRING: "CZJ1234567"''') # serial number
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.1.3.0 = INTEGER: 2''') # global storage status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.1.3.0 = INTEGER: 2''') # global system status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.1.0 = INTEGER: 2''') # global power supply status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.9.2.2.32.0 = INTEGER: 2''') # power status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.1.0 = INTEGER: 2''') # global temp status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.3.0 = INTEGER: 2''') # global temp sensor
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.4.0 = INTEGER: 2''') # global fan status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.14.4.0 = INTEGER: 2''') # global memory status
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.2.1.1.6.0 = INTEGER: 2''') # global controller status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.6.0.1 = INTEGER: 2''') # physical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.0 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.57.0.1 = INTEGER: 2''') # drive smart status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.0 = INTEGER: 52''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.70.0.1 = INTEGER: 60''') # drive temperature
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.0 = INTEGER: 60''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.5.1.1.71.0.1 = INTEGER: 60''') # drive temperature threshold
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.3.2.3.1.1.4.0.1 = INTEGER: 2''') # logical drive status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.1 = INTEGER: 20''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.4.0.2 = INTEGER: 40''') # environment temperatures
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.1 = INTEGER: 42''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.8.1.5.0.2 = INTEGER: 70''') # environment temperatures thresholds
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 1''') # power supply status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.2 = INTEGER: 2''') # power supply redundancy

    p=subprocess.Popen('health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=1 --drives=2 --fan=1', shell=True, stdout=subprocess.PIPE)
    assert 'Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567. Server power status: poweredOff' in p.stdout.read()

def test_stop():
    # stop the testagent
    stop_server()