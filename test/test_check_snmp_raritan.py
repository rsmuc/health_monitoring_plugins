import context
import subprocess
import testagent
import health_monitoring_plugins.raritan


# unit tests
def test_raritan_real_value():
    assert health_monitoring_plugins.raritan.real_value(100, 2) == "1.0"


# integration tests

testagent.configure(agent_address = "localhost:1234",
    rocommunity='public', rwcommunity='private')


def test_start_snmp_simulation():
    # start the testagent (Raritan walk)
    # Gauge32 are not working - So I replaced them by INTEGER
    # some of the values are not from a walk - I modified them to have the return values I need (critical etc.)
    walk =  '''iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.1 = INTEGER: 61
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.4 = INTEGER: 230
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.5 = INTEGER: 1357
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.6 = INTEGER: 1400
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.7 = INTEGER: 97
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.8 = INTEGER: 8574135
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.1 = INTEGER: 2
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.4 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.5 = INTEGER: 3
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.6 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.7 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.8 = INTEGER: 5
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.1 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.7 = INTEGER: 2
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.1 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.4 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.5 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.6 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.7 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.8 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.1 = INTEGER: 104
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.4 = INTEGER: 247
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.7 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.1 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.4 = INTEGER: 188
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.7 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.1 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.4 = INTEGER: 194
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.7 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.1 = INTEGER: 128
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.4 = INTEGER: 254
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.7 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.1 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.2 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.3 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.4 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.5 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.6 = STRING: "Switch Test 1"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.7 = STRING: "Switch Test 2"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.8 = STRING: "Switch Test 3"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.9 = STRING: "Switch Test 4"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.10 = STRING: "Switch Test 5"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.11 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.12 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.13 = STRING: "Switch C1"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.14 = STRING: "Switch C2"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.15 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.16 = STRING: "Switch 1"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.17 = STRING: "Switch 2"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.18 = STRING: "Switch 1"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.19 = STRING: "Switch 2"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.20 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.21 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.22 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.23 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.24 = STRING: ""
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.1.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.2.14 = INTEGER: 8
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.3.14 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.4.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.5.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.6.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.7.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.8.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.9.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.10.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.11.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.12.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.13.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.14.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.15.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.16.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.17.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.18.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.19.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.20.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.21.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.22.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.23.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.24.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.2 = STRING: "Tuerkontakt"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.3 = STRING: "External Sensor 3"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.4 = STRING: "On/Off 1"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.5 = STRING: "Temperature Rack 3"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.6 = STRING: "Humidity 1"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.7 = STRING: "Temperature 2"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.8 = STRING: "Air Pressure 1"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.9 = STRING: "Broken"
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.2 = INTEGER: 11
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.3 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.4 = INTEGER: 11
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.5 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.6 = INTEGER: 6
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.7 = INTEGER: 3
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.8 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.9 = INTEGER: 999
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.2 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.3 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.4 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.5 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.6 = INTEGER: 9
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.7 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.8 = INTEGER: 11
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.5 = INTEGER: 215
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.6 = INTEGER: 45
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.7 = INTEGER: 221
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.8 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.5 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.7 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.8 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.2 = INTEGER: 14
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.3 = INTEGER: 14
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.4 = INTEGER: 14
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.5 = INTEGER: 10
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.6 = INTEGER: 11
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.7 = INTEGER: 10
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.8 = INTEGER: 13
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.9 = INTEGER: 991
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.5 = INTEGER: 150
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.6 = INTEGER: 10
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.7 = INTEGER: 150
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.5 = INTEGER: 180
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.6 = INTEGER: 15
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.7 = INTEGER: 200
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.5 = INTEGER: 310
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.6 = INTEGER: 80
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.7 = INTEGER: 320
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.8 = INTEGER: 1000
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.5 = INTEGER: 270
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.6 = INTEGER: 70
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.7 = INTEGER: 280
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.8 = INTEGER: 800'''
    testagent.register_snmpwalk_ouput(walk)
    testagent.start_server()


# def test_raritan_local():
#     # run test against a real Raritan device
#     p = subprocess.Popen('health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py ' +
#                          "-H 172.29.12.18 -t outlet -i 2 -V 3 "
#                          "-U snmpv3 -L authPriv -a MD5 "
#                          "-A snmpv3snmpv3 -x DES -X snmpv3snmpv3",
#                          shell=True, stdout=subprocess.PIPE)
#     assert "Critical - Outlet 2" in p.stdout.read()


def test_raritan_cmdline():
    # without options
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py",
                       shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=context.testenv)
    assert "error: Hostname must be specified" in p.stderr.read() 

    # without -H 1.2.3.4 (unknown host)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 1.2.3.4",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == "Unknown - SNMP walk response incomplete\n"

    # with --help
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py --help",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert "Options:" in p.stdout.read()


def test_snmpv3(capsys):
    # not reachable

    p = subprocess.Popen('health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py ' +
                         "-H 127.0.0.1:1234 -t outlet -i 1 -V 3 "
                         "-U nothinguseful -L authNoPriv -a MD5 "
                         "-A nothinguseful -x DES -X nothinguseful --timeout 3",
                         shell=True, stdout=subprocess.PIPE)
    assert "Unknown - No response" in p.stdout.read()


def test_outlet1_on():
    # Outlet 1 ON
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t outlet -i 1",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == "OK - Outlet 1 - 'frei' is: ON\n"


def test_outlet1_without_ID():
    # Outlet Check without ID option
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t outlet",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == "OK - Outlet 1 - 'frei' is: ON\n"


def test_outlet2_off():
    # Outlet 2 OFF
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t outlet -i 2",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == "Critical - Outlet 2 - 'Switch' is: OFF\n"


def test_outlet3_unavailable():
    # Outlet 3 in unavailable state (-1)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t outlet -i 3",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == "Critical - Outlet 3 - 'frei' is: UNAVAILABLE\n"


def test_outlet_without_name():
    # Outlet 3 in unavailable state (-1)
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t outlet -i 24",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == "OK - Outlet 24 - '' is: ON\n" 


def test_sensor_alarmed():    
    # Sensor 2 - Door contact - alarmed
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t sensor -i 2",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == "Critical - Sensor 2 - 'Tuerkontakt'  is: alarmed\n"


def test_sensor_invalid():
    # Sensor 3 - Door contact - invalid value
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t sensor -i 9",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == "Unknown - Invalid sensor response 999\n"


def test_sensor_normal():
    # Sensor 3 - external Sensor - normal
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t sensor -i 3",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == "OK - Sensor 3 - 'External Sensor 3'  is: normal\n"


def test_sensor_temp_normal():    
    # Sensor 5 - Temperature - normal
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t sensor -i 5",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == "OK - Sensor 5 - 'Temperature Rack 3' 21.5C is: normal | 'Temperature Rack 3 -C- '=21.5;18.0:27.0;15.0:31.0;;\n"


def test_sensor_humid_above():     
    # Sensor 6 - Humidity - aboveupperCritical
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t sensor -i 6",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == "Critical - Sensor 6 - 'Humidity 1' 45.0% is: aboveUpperCritical | 'Humidity 1 -%- '=45.0;15.0:70.0;10.0:80.0;;\n"


def test_sensor_temp_below():     
    # Sensor 7 - Temperature - belowLowerCritical
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t sensor -i 7",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == "Warning - Sensor 7 - 'Temperature 2' 22.1C is: belowLowerWarning | 'Temperature 2 -C- '=22.1;20.0:28.0;15.0:32.0;;\n"


def test_inlet_ok():    
    # Inlet all OK
    p=subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t inlet",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == (
        "OK - Inlet. 6.1 A. 230.0 V. 1357.0 W. 1400.0 VA. 0.97. 8574135.0 Wh | 'Sensor 0 -A-'=6.1;0.0:10.4;0.0:12.8;; 'Sensor 1 -V-'=230.0;194.0:247.0;188.0:254.0;; 'Sensor 2 -W-'=1357.0;0.0:0.0;0.0:0.0;; 'Sensor 3 -VA-'=1400.0;0.0:0.0;0.0:0.0;; 'Sensor 4 --'=0.97;0.0:0.0;0.0:0.0;; 'Sensor 5 -Wh-'=8574135.0;0.0:0.0;0.0:0.0;;\n"
        "6.1 A: normal\n"
        "230.0 V: normal\n"
        "1357.0 W: normal\n"
        "1400.0 VA: normal\n"
        "0.97 : normal\n"
        "8574135.0 Wh: normal\n")


def test_inlet_critical():    
    # For a Critical Inlet, we need to change the values of the corresponding OIDs
    testagent.unregister_all()
    walk =  '''iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.1 = INTEGER: 61
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.4 = INTEGER: 230
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.5 = INTEGER: 1357
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.6 = INTEGER: 1400
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.7 = INTEGER: 97
                iso.3.6.1.4.1.13742.6.5.2.3.1.4.1.1.8 = INTEGER: 8574135
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.1 = INTEGER: 2
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.4 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.5 = INTEGER: 3
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.6 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.7 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.3.3.4.1.6.1.1.8 = INTEGER: 5
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.1 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.7 = INTEGER: 2
                iso.3.6.1.4.1.13742.6.3.3.4.1.7.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.1 = INTEGER: 2
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.4 = INTEGER: 3
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.5 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.6 = INTEGER: 5
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.7 = INTEGER: 6
                iso.3.6.1.4.1.13742.6.5.2.3.1.3.1.1.8 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.1 = INTEGER: 104
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.4 = INTEGER: 247
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.7 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.24.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.1 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.4 = INTEGER: 188
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.7 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.21.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.1 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.4 = INTEGER: 194
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.7 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.22.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.1 = INTEGER: 128
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.4 = INTEGER: 254
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.5 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.7 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.3.4.1.23.1.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.1 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.2 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.3 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.4 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.5 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.6 = STRING: "Switch Test 1"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.7 = STRING: "Switch Test 2"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.8 = STRING: "Switch Test 3"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.9 = STRING: "Switch Test 4"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.10 = STRING: "Switch Test 5"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.11 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.12 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.13 = STRING: "Switch C1"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.14 = STRING: "Switch C2"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.15 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.16 = STRING: "Switch 1"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.17 = STRING: "Switch 2"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.18 = STRING: "Switch 1"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.19 = STRING: "Switch 2"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.20 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.21 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.22 = STRING: "Switch"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.23 = STRING: "frei"
                iso.3.6.1.4.1.13742.6.3.5.3.1.3.1.24 = STRING: ""
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.1.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.2.14 = INTEGER: 8
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.3.14 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.4.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.5.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.6.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.7.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.8.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.9.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.10.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.11.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.12.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.13.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.14.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.15.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.16.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.17.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.18.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.19.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.20.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.21.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.22.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.23.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.5.4.3.1.3.1.24.14 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.2 = STRING: "Tuerkontakt"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.3 = STRING: "External Sensor 3"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.4 = STRING: "On/Off 1"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.5 = STRING: "Temperature Rack 3"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.6 = STRING: "Humidity 1"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.7 = STRING: "Temperature 2"
                iso.3.6.1.4.1.13742.6.3.6.3.1.4.1.8 = STRING: "Air Pressure 1"
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.2 = INTEGER: 11
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.3 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.4 = INTEGER: 11
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.5 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.6 = INTEGER: 6
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.7 = INTEGER: 3
                iso.3.6.1.4.1.13742.6.5.5.3.1.3.1.8 = INTEGER: 4
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.2 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.3 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.4 = INTEGER: -1
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.5 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.6 = INTEGER: 9
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.7 = INTEGER: 7
                iso.3.6.1.4.1.13742.6.3.6.3.1.16.1.8 = INTEGER: 11
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.5 = INTEGER: 215
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.6 = INTEGER: 45
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.7 = INTEGER: 221
                iso.3.6.1.4.1.13742.6.5.5.3.1.4.1.8 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.5 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.6 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.7 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.6.3.1.17.1.8 = INTEGER: 1
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.2 = INTEGER: 14
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.3 = INTEGER: 14
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.4 = INTEGER: 14
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.5 = INTEGER: 10
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.6 = INTEGER: 11
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.7 = INTEGER: 10
                iso.3.6.1.4.1.13742.6.3.6.3.1.2.1.8 = INTEGER: 13
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.5 = INTEGER: 150
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.6 = INTEGER: 10
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.7 = INTEGER: 150
                iso.3.6.1.4.1.13742.6.3.6.3.1.31.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.5 = INTEGER: 180
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.6 = INTEGER: 15
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.7 = INTEGER: 200
                iso.3.6.1.4.1.13742.6.3.6.3.1.32.1.8 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.5 = INTEGER: 310
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.6 = INTEGER: 80
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.7 = INTEGER: 320
                iso.3.6.1.4.1.13742.6.3.6.3.1.33.1.8 = INTEGER: 1000
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.2 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.3 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.4 = INTEGER: 0
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.5 = INTEGER: 270
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.6 = INTEGER: 70
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.7 = INTEGER: 280
                iso.3.6.1.4.1.13742.6.3.6.3.1.34.1.8 = INTEGER: 800'''
    testagent.register_snmpwalk_ouput(walk)

    # Inlet Critical
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py -H 127.0.0.1:1234 -t inlet",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == (
        "Critical - Inlet. 6.1 A is belowLowerCritical. 6.1 A. 230.0 V is belowLowerWarning. "
        "230.0 V. 1357.0 W. 1400.0 VA is aboveUpperWarning. 1400.0 VA. 0.97  is aboveUpperCritical. "
        "0.97. 8574135.0 Wh | 'Sensor 0 -A-'=6.1;0.0:10.4;0.0:12.8;; 'Sensor 1 -V-"
        "'=230.0;194.0:247.0;188.0:254.0;; "
        "'Sensor 2 -W-'=1357.0;0.0:0.0;0.0:0.0;; 'Sensor 3 -VA-'=1400.0;0.0:0.0;0.0:0.0;; "
        "'Sensor 4 --'=0.97;0.0:0.0;0.0:0.0;; 'Sensor 5 -Wh-'=8574135.0;0.0:0.0;0.0:0.0;;\n"
        "6.1 A: belowLowerCritical\n"
        "230.0 V: belowLowerWarning\n"
        "1357.0 W: normal\n"
        "1400.0 VA: aboveUpperWarning\n"
        "0.97 : aboveUpperCritical\n"
        "8574135.0 Wh: normal\n")


def test_stop():
    # stop the testagent
    testagent.stop_server()