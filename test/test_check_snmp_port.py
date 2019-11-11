#!/usr/bin/python
import context
import netsnmp
import subprocess
from health_monitoring_plugins.ipport import *
from testagent import *

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address = "localhost:1234",
    rocommunity='public', rwcommunity='private')

# create netsnmp Sessions for test_walk_data, test_check_udp, test_check_tcp
session = netsnmp.Session(Version=2, DestHost='localhost', Community='public')
failSession = netsnmp.Session(Version=2, DestHost='1.2.3.4', Community='public')
test_session = netsnmp.Session(Version=2, DestHost='localhost:1234', Community='public')


def test_start():
    # start the testagent (port 22 (TCP) is esablished and 161 is open)    
    walk =  '''iso.3.6.1.2.1.6.13.1.3.0.0.0.0.22.0.0.0.0.0 = INTEGER: 22
               iso.3.6.1.2.1.6.13.1.1.0.0.0.0.22.0.0.0.0.0 = INTEGER: 2
               iso.3.6.1.2.1.7.5.1.2.0.0.0.0.161 = INTEGER: 161'''   
    register_snmpwalk_ouput(walk)
    start_server()

# def test_check_typ(capsys):
#     """
#     test of the check_typ function ... not really interessting.
#     the function just to verify that a correct value is set via -ty parameter
#     """
#     with pytest.raises(SystemExit):
#         # "test" is an invalid argument
#         check_typ(helper, "test")
#     out, err = capsys.readouterr()
#     assert out == "Unknown - Type (-t) must be udp or tcp.\n"
#
#     assert check_typ(helper, "tcp") == None
#     assert check_typ(helper, "udp") == None
#
# def test_check_port(capsys):
#     """
#     test of the check_port function
#     the function is only to verify that a correct value is set via -p option
#     """
#     with pytest.raises(SystemExit):
#         # "test" is an invalid argument
#         check_port(helper, "test")
#     out, err = capsys.readouterr()
#     assert out == "Unknown - Port (-p) must be a integer value.\n"
#
#     assert check_port(helper, "22") == None
#
# def test_check_udp(capsys):
#     """ test the check_udp function """
#     # check udp port "161" (open)
#     assert check_udp(helper, "127.0.0.1:1234", "161", test_session) == "Current status for UDP port 161 is: OPEN"
#
#     # check udp port "164" (closed)
#     assert check_udp(helper, "127.0.0.1:1234", "164", test_session) == "Current status for UDP port 164 is: CLOSED"
#
#     # check udp port "test"
#     assert check_udp(helper, "127.0.0.1:1234", "test", test_session) == "Current status for UDP port test is: CLOSED"
#
# def test_check_tcp(capsys):
#     # check "22" (listen)
#     assert check_tcp(helper, "127.0.0.1:1234", "22", "closed", "closed", test_session) == "Current status for TCP port 22 is: listen"
#
#     # check "22" (listen), but listen is a warning status
#     assert check_tcp(helper, "127.0.0.1:1234", "22", "listen", "listen", test_session) == "Current status for TCP port 22 is: listen"
#
#     # check "164" (closed / not a UDP port)
#     assert check_tcp(helper, "127.0.0.1:1234", "164", "closed", "closed", test_session) == "Current status for TCP port 164 is: CLOSED"
#
#     # check "test"
#     assert check_tcp(helper, "127.0.0.1:1234", "test", "closed", "closed", test_session) == "Current status for TCP port test is: CLOSED"

#integration test
def test_system_call(capsys):
    # without options
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_port/check_snmp_port.py", shell=True, stderr=subprocess.PIPE)
    assert "Hostname must be specified\n" in p.stderr.read()

    # with --help
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_port/check_snmp_port.py --help", shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()


def test_snmpv3(capsys):
    # not reachable

    p = subprocess.Popen('health_monitoring_plugins/check_snmp_port/check_snmp_port.py' + " -H 1.2.3.4 -V 3 "
                                                     "-U nothinguseful -L authNoPriv -a MD5 "
                                                     "-A nothinguseful -x DES -X nothinguseful -p 161 --snmptimeout 3",
                         shell=True, stdout=subprocess.PIPE)
    assert "Unknown - No response from device for Open UDP Ports" in p.stdout.read()


def test_tcp_scan(capsys):
    # with --type=TCP
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_port/check_snmp_port.py -H localhost:1234 --type=TCP -s", shell=True, stdout=subprocess.PIPE)
    assert "TCP:" in p.stdout.read()

def test_tcp_port161(capsys):
    # with --type=TCP --port=161 (closed)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_port/check_snmp_port.py -H localhost:1234 --type=TCP --port=161", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Current status for TCP port 161 is: CLOSED" in p.stdout.read()

def test_tcp_port22(capsys):
    #with --type=TCP --port=22 (open)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_port/check_snmp_port.py -H localhost:1234 --type=TCP --port=22", shell=True, stdout=subprocess.PIPE)
    assert "OK - Current status for TCP port 22 is: listen" in p.stdout.read()

def test_tcp_port22_warning(capsys):
    #with --type=TCP --port=22 (open) --warning listen
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_port/check_snmp_port.py -H localhost:1234 --type=TCP --port=22 -w listen", shell=True, stdout=subprocess.PIPE)
    assert "Warning - Current status for TCP port 22 is: listen" in p.stdout.read()

def test_udp_open(capsys):
    # with --type=UDP --port=161 (open)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_port/check_snmp_port.py -H localhost:1234 --type=UDP --port=161", shell=True, stdout=subprocess.PIPE)
    assert "OK - Current status for UDP port 161 is: OPEN" in p.stdout.read()

def test_udp_closed(capsys):    
    #with --type=UDP --port=1235678 (closed)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_port/check_snmp_port.py -H localhost:1234 --type=UDP --port=1235678", shell=True, stdout=subprocess.PIPE)
    assert "Critical - Current status for UDP port 1235678 is: CLOSED" in p.stdout.read()
    
def test_stop():
    # stop the testagent
    stop_server()
