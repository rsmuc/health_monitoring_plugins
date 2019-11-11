#!/usr/bin/python
import context
import netsnmp
import subprocess
from health_monitoring_plugins.windowsservice import *
from testagent import *

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address="localhost:1234",
          rocommunity='public', rwcommunity='private')

# create netsnmp Session  for test_attempt_get and test_walk
session = netsnmp.Session(Version=2, DestHost='localhost', Community='public')
failSession = netsnmp.Session(Version=2, DestHost='1.2.3.4', Community='public')


def test_start():
    # some open Windows services   
    walk = '''.1.3.6.1.4.1.77.1.2.3.1.1.5.80.111.119.101.114 = STRING: "Power"
            .1.3.6.1.4.1.77.1.2.3.1.1.6.83.101.114.118.101.114 = STRING: "Server"
            .1.3.6.1.4.1.77.1.2.3.1.1.6.84.104.101.109.101.115 = STRING: "Themes"
            .1.3.6.1.4.1.77.1.2.3.1.1.9.73.80.32.72.101.108.112.101.114 = STRING: "IP Helper"'''
    register_snmpwalk_ouput(walk)
    start_server()


def test_oid_conversion():
    """
    test convert_in_oid
    """
    assert convert_in_oid(
        "IP Helper") == ".1.3.6.1.4.1.77.1.2.3.1.1.9.73.80.32.72.101.108.112.101.114"


def test_without_options(capsys):
    # without options
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_service/check_snmp_service.py",
                         shell=True, stderr=subprocess.PIPE)
    assert "Hostname must be specified\n" in p.stderr.read()


def test_help():
    # with --help
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_service/check_snmp_service.py --help", shell=True,
        stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()


def test_scan():
    # with service scan
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_service/check_snmp_service.py -H 127.0.0.1:1234 -S",
        shell=True, stdout=subprocess.PIPE)
    assert "Running services at host: 127.0.0.1:1234\nService: \t'Power'\nService: \t'Server'\nService: \t'Themes" in p.stdout.read()


def test_service_available():
    # with service "IP Helper" available
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_service/check_snmp_service.py -H 127.0.0.1:1234 -s 'IP Helper'",
        shell=True, stdout=subprocess.PIPE)
    assert "OK - Status of Service 'IP Helper' is: RUNNING\n" in p.stdout.read()

    # with service "Test" not available
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_service/check_snmp_service.py -H 127.0.0.1:1234 -s 'Test'",
        shell=True, stdout=subprocess.PIPE)
    assert "Critical - Status of Service 'Test' is: NOT RUNNING\n" in p.stdout.read()


def test_stop():
    # stop the testagent
    stop_server()
