#!/usr/bin/python
import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_meinberg_ntp'))
 
from check_meinberg_ntp import *

import pytest
import subprocess
from testagent import *

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address = "localhost:1234",
    rocommunity='public', rwcommunity='private')

# create netsnmp Sessions for test_get
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

#####################################
# run the test for the old firmware #
#####################################

def test_start():
    # start the testagent
    # Gauge32 are not working - So I replaced them by INTEGER
    # Old Firmware # Everything ok
    walk =  '''
            iso.3.6.1.4.1.5597.3.1.2.0 = INTEGER: 4
            iso.3.6.1.4.1.5597.3.2.7.0 = STRING: "GPS Position: 48.1276 11.6124 619m"
            iso.3.6.1.4.1.5597.3.2.9.0 = INTEGER: 7
            iso.3.6.1.4.1.5597.3.2.16.0 = INTEGER: 1
            '''   
    register_snmpwalk_ouput(walk)
    start_server()

# integration test
def test_system_test_meinberg(capsys):
    # without options
    p=subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py", shell=True, stdout=subprocess.PIPE)
    assert "Unknown - Hostname must be specified" in p.stdout.read()

    # without -H 1.2.3.4 (unknown host)
    p=subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H 1.2.3.4", shell=True, stdout=subprocess.PIPE)
    assert "Unknown - snmpget failed - no data" in p.stdout.read()

    # with --help
    p=subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py --help", shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()

def test_with_host_ok():
    # everything ok
    p=subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234", shell=True, stdout=subprocess.PIPE)
    assert "OK - GPS Position: 48.1276 11.6124 619m. Good satellites: 7 | 'satellites'=7;;;;\n" in p.stdout.read()

def test_less_satellites_warning():
    # warning threshold 8 satellites
    p=subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234 --threshold metric=satellites,warning=8:,critical=2:", shell=True, stdout=subprocess.PIPE)
    assert "Warning - GPS Position: 48.1276 11.6124 619m. Good satellites: 7. Warning on satellites | 'satellites'=7;8:;2:;;\n" in p.stdout.read()

def test_less_satellites_critical():
    # critical threhold 8 satellites
    p=subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234 --threshold metric=satellites,warning=9:,critical=8:", shell=True, stdout=subprocess.PIPE)
    assert "Critical - GPS Position: 48.1276 11.6124 619m. Good satellites: 7. Critical on satellites | 'satellites'=7;9:;8:;;\n" in p.stdout.read()

def test_with_host_ok_old_firmware_flag():
    # everything ok
    p=subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234 -m 1", shell=True, stdout=subprocess.PIPE)
    assert "OK - GPS Position: 48.1276 11.6124 619m. Good satellites: 7 | 'satellites'=7;;;;\n" in p.stdout.read()

def test_old_firmware_ntp_status():
    # start the testagent
    # Old Firmware # NTP not ok and gps not ok
    unregister_all()
    walk =  '''
            iso.3.6.1.4.1.5597.3.1.2.0 = INTEGER: 0
            iso.3.6.1.4.1.5597.3.2.7.0 = STRING: "GPS Position: 48.1276 11.6124 619m"
            iso.3.6.1.4.1.5597.3.2.9.0 = INTEGER: 7
            iso.3.6.1.4.1.5597.3.2.16.0 = INTEGER: 0
            '''
    
    register_snmpwalk_ouput(walk)

    p=subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234 -m 1", shell=True, stdout=subprocess.PIPE)
    assert "Critical - GPS Position: 48.1276 11.6124 619m. NTP status: notSynchronized. GPS status: notavailable. Good satellites: 7 | 'satellites'=7;;;;\n" in p.stdout.read()

#######################################
# run the tests with the new firmware #
#######################################

def test_start_ng():
    # start simulation of new firmware
    # everything is ok
    unregister_all()
    walk =  '''
            iso.3.6.1.4.1.5597.30.0.2.1.0 = INTEGER: 2
            iso.3.6.1.4.1.5597.30.0.1.5.0 = STRING: "GPS Position: 48.1276 11.6124 619m"
            iso.3.6.1.4.1.5597.30.0.1.2.1.6.1 = INTEGER: 7
            iso.3.6.1.4.1.5597.30.0.1.2.1.5.1 = INTEGER: 1
            '''    
    register_snmpwalk_ouput(walk)

def test_with_host_ok_ng():
    # everything ok
    p=subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234 -m NG", shell=True, stdout=subprocess.PIPE)
    assert "OK - GPS Position: 48.1276 11.6124 619m. Good satellites: 7 | 'satellites'=7;;;;\n" in p.stdout.read()

def test_less_satellites_warning_ng():
    # warning threhold 8 satellites
    p=subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234 -m NG --threshold metric=satellites,warning=8:,critical=2:", shell=True, stdout=subprocess.PIPE)
    assert "Warning - GPS Position: 48.1276 11.6124 619m. Good satellites: 7. Warning on satellites | 'satellites'=7;8:;2:;;\n" in p.stdout.read()

def test_less_satellites_critical_ng():
    # critical threhold 8 satellites
    p=subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234 -m NG --threshold metric=satellites,warning=9:,critical=8:", shell=True, stdout=subprocess.PIPE)
    assert "Critical - GPS Position: 48.1276 11.6124 619m. Good satellites: 7. Critical on satellites | 'satellites'=7;9:;8:;;\n" in p.stdout.read()

def test_ntp_status_ng():
    # start the testagent
    # Old Firmware # NTP not ok and gps not ok
    unregister_all()
    walk =  '''
            iso.3.6.1.4.1.5597.30.0.2.1.0 = INTEGER: 1
            iso.3.6.1.4.1.5597.30.0.1.5.0 = STRING: "GPS Position: 48.1276 11.6124 619m"
            iso.3.6.1.4.1.5597.30.0.1.2.1.6.1 = INTEGER: 7
            iso.3.6.1.4.1.5597.30.0.1.2.1.5.1 = INTEGER: 0
            '''
    register_snmpwalk_ouput(walk)

    p=subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234 -m NG", shell=True, stdout=subprocess.PIPE)
    assert "Critical - GPS Position: 48.1276 11.6124 619m. NTP status: notSynchronized. GPS status: notAvailable. Good satellites: 7 | 'satellites'=7;;;;\n" in p.stdout.read()

    
def test_stop():
    # stop the testagent
    stop_server()
