#!/usr/bin/python
import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_teledyne'))
 
#from check_snmp_teledyne import *

import pytest
import subprocess
from testagent import *

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address = "localhost:1234",
    rocommunity='public', rwcommunity='private')


def test_start():
    # start the testagent
    # Gauge32 are not working - So I replaced them by INTEGER
    # # Everything ok
    
    #Unit1FaultState
    #Unit2FaultState
    #Unit3FaultState
    #SummaryFaultState
    #PS12 FaultState
    #RFSwitch12State
        
    walk =  '''
            iso.3.6.1.4.1.20712.2.1.3.1.2.1  = INTEGER: 0
            iso.3.6.1.4.1.20712.2.1.3.1.2.2  = INTEGER: 0
            iso.3.6.1.4.1.20712.2.1.3.1.2.3  = INTEGER: 0
            iso.3.6.1.4.1.20712.2.1.3.1.2.4  = INTEGER: 0
            iso.3.6.1.4.1.20712.2.1.3.1.2.5  = INTEGER: 0
            iso.3.6.1.4.1.20712.2.1.3.1.2.6  = INTEGER: 0
            iso.3.6.1.4.1.20712.2.1.3.1.2.11  = INTEGER: 0
            iso.3.6.1.4.1.20712.2.1.3.1.2.12  = INTEGER: 0
            '''   
    register_snmpwalk_ouput(walk)
    start_server()

# integration test
def test_system_test_teledyne(capsys):
    # without options
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_teledyne/check_snmp_teledyne.py", shell=True, stdout=subprocess.PIPE)
    assert "Unknown - Hostname must be specified" in p.stdout.read()

    # without -H 1.2.3.4 (unknown host)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_teledyne/check_snmp_teledyne.py -H 1.2.3.4", shell=True, stdout=subprocess.PIPE)
    assert "Unknown - snmpget failed - no data" in p.stdout.read()

    # with --help
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_teledyne/check_snmp_teledyne.py --help", shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()

def test_with_host_ok():
    # everything ok
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_teledyne/check_snmp_teledyne.py -H localhost:1234", shell=True, stdout=subprocess.PIPE)
    assert "OK - Fault Summary: No Fault. Power Supply 1: No Fault. Power Supply 2: No Fault. RF Switch 1: No Fault. RF Switch 2: No Fault. Unit 1: No Fault. Unit 2: No Fault. Unit 3: No Fault" in p.stdout.read()
    

def test_with_all_nok():
    # start the testagent
    # Everything is CRITICAL
    unregister_all()
    walk =  '''
            iso.3.6.1.4.1.20712.2.1.3.1.2.1  = INTEGER: 1
            iso.3.6.1.4.1.20712.2.1.3.1.2.2  = INTEGER: 1
            iso.3.6.1.4.1.20712.2.1.3.1.2.3  = INTEGER: 1
            iso.3.6.1.4.1.20712.2.1.3.1.2.4  = INTEGER: 1
            iso.3.6.1.4.1.20712.2.1.3.1.2.5  = INTEGER: 1
            iso.3.6.1.4.1.20712.2.1.3.1.2.6  = INTEGER: 1
            iso.3.6.1.4.1.20712.2.1.3.1.2.11  = INTEGER: 1
            iso.3.6.1.4.1.20712.2.1.3.1.2.12  = INTEGER: 1
            '''   
    register_snmpwalk_ouput(walk)

    p=subprocess.Popen("health_monitoring_plugins/check_snmp_teledyne/check_snmp_teledyne.py -H localhost:1234", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Fault Summary: Fault. Power Supply 1: Fault. Power Supply 2: Fault. RF Switch 1: Fault. RF Switch 2: Fault. Unit 1: Fault. Unit 2: Fault. Unit 3: Fault" in p.stdout.read()

    
def test_stop():
    # stop the testagent
    stop_server()
