#!/usr/bin/python
import context
import netsnmp
import subprocess
from health_monitoring_plugins.procurve import *
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
    # everything ok
    walk = '''
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.1.1 = INTEGER: 1
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.1.2 = INTEGER: 2
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.2.1 = OID: iso.3.6.1.4.1.11.2.3.7.8.3.1
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.2.2 = OID: iso.3.6.1.4.1.11.2.3.7.8.3.2
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.3.1 = INTEGER: 1
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.3.2 = INTEGER: 1
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.4.1 = INTEGER: 4
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.4.2 = INTEGER: 4
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.5.1 = INTEGER: 0
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.5.2 = INTEGER: 0
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.6.1 = INTEGER: 0
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.6.2 = INTEGER: 0
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.7.1 = STRING: "Power Supply Sensor"
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.7.2 = STRING: "Fan Sensor"
    '''
    register_snmpwalk_ouput(walk)
    start_server()


# integration test
def test_system_call(capsys):
    # without options
    p = subprocess.Popen(
        "python health_monitoring_plugins/check_snmp_procurve/check_snmp_procurve.py", shell=True,
        stderr=subprocess.PIPE)
    assert "Hostname must be specified\n" in p.stderr.read()

    # with --help
    p = subprocess.Popen("python health_monitoring_plugins/check_snmp_procurve/check_snmp_procurve"
                         ".py --help", shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()


def test_snmpv3(capsys):
    # not reachable

    p = subprocess.Popen(
        'python health_monitoring_plugins/check_snmp_procurve/check_snmp_procurve.py' + " -H 1.2.3.4 -V 3 "
                                                                                        "-U nothinguseful -L authNoPriv -a MD5 "
                                                                                        "-A nothinguseful -x DES -X nothinguseful --snmptimeout 3",
        shell=True, stdout=subprocess.PIPE)
    assert "Unknown - No response from device for Sensors" in p.stdout.read()


def test_ok(capsys):
    p = subprocess.Popen(
        "python health_monitoring_plugins/check_snmp_procurve/check_snmp_procurve.py -H localhost:1234",
        shell=True, stdout=subprocess.PIPE)
    assert "OK - Power Supply Sensor: good. Fan Sensor: good" in p.stdout.read()


def test_start_critical():
    # sensors bad
    unregister_all()
    walk = '''
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.1.1 = INTEGER: 1
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.1.2 = INTEGER: 2
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.2.1 = OID: iso.3.6.1.4.1.11.2.3.7.8.3.1
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.2.2 = OID: iso.3.6.1.4.1.11.2.3.7.8.3.2
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.3.1 = INTEGER: 1
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.3.2 = INTEGER: 1
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.4.1 = INTEGER: 2
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.4.2 = INTEGER: 2
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.5.1 = INTEGER: 0
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.5.2 = INTEGER: 0
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.6.1 = INTEGER: 0
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.6.2 = INTEGER: 0
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.7.1 = STRING: "Power Supply Sensor"
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.7.2 = STRING: "Fan Sensor"
    '''

    register_snmpwalk_ouput(walk)


def test_critical(capsys):
    p = subprocess.Popen(
        "python health_monitoring_plugins/check_snmp_procurve/check_snmp_procurve.py -H localhost:1234",
        shell=True, stdout=subprocess.PIPE)
    assert "Critical - Power Supply Sensor: bad. Fan Sensor: bad" in p.stdout.read()


def test_start_invalid():
    unregister_all()
    walk = '''
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.1.1 = INTEGER: 1
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.1.2 = INTEGER: 2
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.2.1 = OID: iso.3.6.1.4.1.11.2.3.7.8.3.1
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.2.2 = OID: iso.3.6.1.4.1.11.2.3.7.8.3.2
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.3.1 = INTEGER: 1
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.3.2 = INTEGER: 1
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.4.1 = INTEGER: -1
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.4.2 = INTEGER: -1
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.5.1 = INTEGER: 0
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.5.2 = INTEGER: 0
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.6.1 = INTEGER: 0
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.6.2 = INTEGER: 0
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.7.1 = STRING: "Power Supply Sensor"
                iso.3.6.1.4.1.11.2.14.11.1.2.6.1.7.2 = STRING: "Fan Sensor"
    '''
    register_snmpwalk_ouput(walk)


def test_invalid(capsys):
    p = subprocess.Popen(
        "python health_monitoring_plugins/check_snmp_procurve/check_snmp_procurve.py -H localhost:1234",
        shell=True, stdout=subprocess.PIPE)
    assert "Unknown - received an undefined value from device: -1" in p.stdout.read()


def test_stop():
    # stop the testagent
    stop_server()
