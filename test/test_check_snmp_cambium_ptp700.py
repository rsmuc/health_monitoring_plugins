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
                iso.3.6.1.4.1.17713.9.12.16.0 = INTEGER: 0
    '''
    register_snmpwalk_ouput(walk)
    start_server()


# integration test
def test_system_call(capsys):
    # without options
    p = subprocess.Popen(
        "python health_monitoring_plugins/check_snmp_cambium_ptp700/check_snmp_cambium_ptp700.py", shell=True,
        stderr=subprocess.PIPE)
    assert "Hostname must be specified\n" in p.stderr.read()

    # with --help
    p = subprocess.Popen("python health_monitoring_plugins/check_snmp_cambium_ptp700/check_snmp_cambium_ptp700"
                         ".py --help", shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()


def test_snmpv3(capsys):
    # not reachable

    p = subprocess.Popen(
        'python health_monitoring_plugins/check_snmp_cambium_ptp700/check_snmp_cambium_ptp700.py' + " -H 1.2.3.4 -V 3 "
                                                                                        "-U nothinguseful -L authNoPriv -a MD5 "
                                                                                        "-A nothinguseful -x DES -X nothinguseful --snmptimeout 3",
        shell=True, stdout=subprocess.PIPE)
    assert "Unknown - No response from device for oid .1.3.6.1.4.1.17713.9.12.16.0" in p.stdout.read()


def test_ok(capsys):
    p = subprocess.Popen(
        "python health_monitoring_plugins/check_snmp_cambium_ptp700/check_snmp_cambium_ptp700.py -H localhost:1234",
        shell=True, stdout=subprocess.PIPE)
    assert "OK - Radio is registering / connected" in p.stdout.read()


def test_start_critical():
    # sensors bad
    unregister_all()
    walk = '''
                iso.3.6.1.4.1.17713.9.12.16.0 = INTEGER: 1
    '''

    register_snmpwalk_ouput(walk)


def test_critical(capsys):
    p = subprocess.Popen(
        "python health_monitoring_plugins/check_snmp_cambium_ptp700/check_snmp_cambium_ptp700.py -H localhost:1234",
        shell=True, stdout=subprocess.PIPE)
    assert "Critical - Radio is searching / not connected" in p.stdout.read()




def test_start_bad2():
    unregister_all()
    walk = '''
                iso.3.6.1.4.1.17713.9.12.16.0 = INTEGER: 2
    '''
    register_snmpwalk_ouput(walk)

def test_bad2(capsys):
    p = subprocess.Popen(
        "python health_monitoring_plugins/check_snmp_cambium_ptp700/check_snmp_cambium_ptp700.py -H localhost:1234",
        shell=True, stdout=subprocess.PIPE)
    assert "Critical - Radio is acquiring / connecting" in p.stdout.read()




def test_start_invalid():
    unregister_all()
    walk = '''
                iso.3.6.1.4.1.17713.9.12.16.0 = INTEGER: 4
    '''
    register_snmpwalk_ouput(walk)


def test_invalid(capsys):
    p = subprocess.Popen(
        "python health_monitoring_plugins/check_snmp_cambium_ptp700/check_snmp_cambium_ptp700.py -H localhost:1234",
        shell=True, stdout=subprocess.PIPE)
    assert "Critical - Radio is N/A" in p.stdout.read()


def test_stop():
    # stop the testagent
    stop_server()
