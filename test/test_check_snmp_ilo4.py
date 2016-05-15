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
configure(agent_address = "localhost:1234",
    rocommunity='public', rwcommunity='private')

#####################################
# run the test for the old firmware #
#####################################

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
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 1''') # power supply status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.2 = INTEGER: 2''') # power supply redundancy

    start_server()

def get_system_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = str(f.readline().split()[0])
        uptime_seconds = uptime_seconds.replace(".", "")
        return str(uptime_seconds)

def test_get(capsys):
    with pytest.raises(SystemExit):
        get_data("1.2.3.4", 2, "public", ".1")
    out, err = capsys.readouterr()    
    assert "Unknown - \n SNMP connection to device failed" in out
    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert get_data("localhost", 2, "public", ".1.3.6.1.2.1.25.1.1.0")[:-2] == get_system_uptime()[:-2]


def test_walk_data():
    """
    test of the walk_data function
    """
    # run a walk on a not existing host
    #assert walk_data("1.2.3.4", 2, "public", ".1") == ()

    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert walk_data("localhost", 2, "public", ".1.3.6.1.2.1.25.1.1")[0][:-3] == get_system_uptime()[:-3]


# integration test
def test_system_test_ilo4(capsys):
    # without options
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py", shell=True, stdout=subprocess.PIPE)
    assert "Unknown - Hostname must be specified" in p.stdout.read()

    # NEEDS TO BE FIXED
    ## with -H 1.2.3.4 --scan (unknown host)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H 1.2.3.4 --scan", shell=True, stdout=subprocess.PIPE)
    assert "Unknown - snmpget failed - no data for OID- maybe wrong MIB version selected or snmp is disabled" in p.stdout.read()

    # NEEDS TO BE FIXED
    ## with -H 127.0.0.1:1234 --scan (known host)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H 127.0.0.1:1234 --scan", shell=True, stdout=subprocess.PIPE)
    assert "Unknown - snmpget failed - no data for OID- maybe wrong MIB version selected or snmp is disabled" in p.stdout.read()


    # with --help
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py --help", shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()

def test_with_host_ok():
    # everything ok (2 drives, 1 power supply running, 1 fan running)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=1 --drives=2 --fan=1", shell=True, stdout=subprocess.PIPE)
    assert "OK - ProLiant DL380 Gen9 - Serial number:CZJ1234567\nGlobal storage status: ok \n\nGlobal system status: ok \n\nGloba" in p.stdout.read()

def test_with_less_fans():
    # 2 fans configured (2 drives, 1 power supply running, 1 fan running)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=1 --drives=2 --fan=2", shell=True, stdout=subprocess.PIPE)
    assert "Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567. 2 fan(s) expected - 3 fan(s) slot(s) detected - 1 fan" in p.stdout.read()

def test_with_less_ps():
    # 2 power supplies configured (2 drives, 1 power supply running, 1 fan running)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=2 --drives=2 --fan=1", shell=True, stdout=subprocess.PIPE)
    assert "Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567. 2 power supply/supplies expected - 2 power supply/supplies" in p.stdout.read()

def test_with_less_drives():
    # 4 drives configured (2 drives, 1 power supply running, 1 fan running)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=1 --drives=4 --fan=1", shell=True, stdout=subprocess.PIPE)
    assert "Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567. 4 physical drive(s) expected - 2 physical drive(s) in ok" in p.stdout.read()

def test_with_drives_disabled():
    # no drives configured (2 drives, 1 power supply running, 1 fan running)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=1 --drives=0 --fan=1", shell=True, stdout=subprocess.PIPE)
    assert "OK - ProLiant DL380 Gen9 - Serial number:CZJ1234567\nGlobal storage status: ok \n\nGlobal system status: ok" in p.stdout.read()

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

    p=subprocess.Popen("health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=1 --drives=2 --fan=1", shell=True, stdout=subprocess.PIPE)
    assert "Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567. Global storage status: other. Global system status: other. Global power supply status: other. Server power status: unknown. Overall thermal environment status: other. Temperature sensors status: other. Fan(s) status: other. Memory status: other." in p.stdout.read()



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

    p=subprocess.Popen("health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=1 --drives=2 --fan=1", shell=True, stdout=subprocess.PIPE)
    assert "Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567. Physical drive temperature 1 above threshold (75 / 60). Temperature at sensor 1 above threshold (55 / 42)" in p.stdout.read()

def test_smart_broken():
    # NEEDS TO BE FIXED
    
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
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 1''') # power supply status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.2 = INTEGER: 2''') # power supply redundancy

    p=subprocess.Popen("health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=1 --drives=2 --fan=1", shell=True, stdout=subprocess.PIPE)
    assert "Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567." in p.stdout.read()

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
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 1''') # power supply status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.2 = INTEGER: 2''') # power supply redundancy

    p=subprocess.Popen("health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=1 --drives=2 --fan=1", shell=True, stdout=subprocess.PIPE)
    assert "Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567." in p.stdout.read()

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
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 1''') # power supply status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.2 = INTEGER: 2''') # power supply redundancy

    p=subprocess.Popen("health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=1 --drives=2 --fan=1", shell=True, stdout=subprocess.PIPE)
    assert "Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567." in p.stdout.read()

def test_redundancy_broken():
    
    # NEEDS TO BE FIXED

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
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 2''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 1''') # power supply status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.1 = INTEGER: 3''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.2 = INTEGER: 3''') # power supply redundancy

    p=subprocess.Popen("health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=1 --drives=2 --fan=1", shell=True, stdout=subprocess.PIPE)
    assert "Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567." in p.stdout.read()

def test_ps_broken():
    
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
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.1 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.2 = INTEGER: 1''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.6.7.1.9.0.3 = INTEGER: 2''') # fan status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.1 = INTEGER: 3''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.4.0.2 = INTEGER: 1''') # power supply status
    
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.1 = INTEGER: 3''')
    register_snmpwalk_ouput('''iso.3.6.1.4.1.232.6.2.9.3.1.9.0.2 = INTEGER: 3''') # power supply redundancy

    p=subprocess.Popen("health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py -H localhost:1234 --ps=1 --drives=2 --fan=1", shell=True, stdout=subprocess.PIPE)
    assert "Critical - ProLiant DL380 Gen9 - Serial number:CZJ1234567." in p.stdout.read()

def test_stop():
    # stop the testagent
    stop_server()