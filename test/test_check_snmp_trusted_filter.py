#!/usr/bin/python
import context
import subprocess
import testagent

testagent.configure(agent_address = "localhost:1234",
    rocommunity='public', rwcommunity='private')

def test_start_snmp_simulation():
    testagent.start_server()

#integration test
def test_options():
    # without options
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_trusted_filter/check_snmp_trusted_filter.py",
                       shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=context.testenv)
    assert "error: Hostname must be specified" in p.stderr.read()
    # with --help
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_trusted_filter/check_snmp_trusted_filter.py --help",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert "Options:" in p.stdout.read()

def test_trustedfilter_ok():
    walk =  '''
    .1.3.6.1.4.1.2566.107.41.1.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.1.0 = INTEGER: 80
    .1.3.6.1.4.1.2566.107.31.2.2.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.3.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.4.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.5.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.7.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.8.0 = INTEGER: 1
    ''' 
    testagent.register_snmpwalk_ouput(walk)
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_trusted_filter/check_snmp_trusted_filter.py -H localhost:1234",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == (
        "OK - Filter Status | 'logfill'=80%%;;;;\n"
        "Power Supply 1: ok\n"
        "Power Supply 2: ok\n"
        "Fan 1: ok\nFan 2: ok\n"
        "Battery: ok\n"
        "Temperature: ok\n"
        "Fill Level internal log: 80%\n"
        "Activity State: standby\n")

    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_trusted_filter/check_snmp_trusted_filter.py -H localhost:1234 -s localhost:1234",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == (
        "Critical - Filter Status. Filter 1 and Filter 2 standby! | 'logfill'=80%%;;;;\n"
        "Power Supply 1: ok\n"
        "Power Supply 2: ok\n"
        "Fan 1: ok\n"
        "Fan 2: ok\n"
        "Battery: ok\nTemperature: ok\n"
        "Fill Level internal log: 80%\n"
        "Activity State: standby\n"
        "Activity State 2: standby\n")
    testagent.unregister_all()

def test_trustedfilter_ps_absent():
    walk =  '''
    .1.3.6.1.4.1.2566.107.41.1.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.1.0 = INTEGER: 80
    .1.3.6.1.4.1.2566.107.31.2.2.0 = INTEGER: 3
    .1.3.6.1.4.1.2566.107.31.2.3.0 = INTEGER: 3
    .1.3.6.1.4.1.2566.107.31.2.4.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.5.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.7.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.8.0 = INTEGER: 1
    '''
    testagent.register_snmpwalk_ouput(walk)
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_trusted_filter/check_snmp_trusted_filter.py -H localhost:1234",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == (
        "Critical - Filter Status. Power Supply 1: absent. Power Supply 2: absent | 'logfill'=80%%;;;;\n"
        "Power Supply 1: absent\n"
        "Power Supply 2: absent\n"
        "Fan 1: ok\n"
        "Fan 2: ok\n"
        "Battery: ok\n"
        "Temperature: ok\n"
        "Fill Level internal log: 80%\n"
        "Activity State: standby\n")
    testagent.unregister_all()

def test_trustedfilter_ps_acoff():
    walk =  '''
    .1.3.6.1.4.1.2566.107.41.1.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.1.0 = INTEGER: 80
    .1.3.6.1.4.1.2566.107.31.2.2.0 = INTEGER: 4
    .1.3.6.1.4.1.2566.107.31.2.3.0 = INTEGER: 4
    .1.3.6.1.4.1.2566.107.31.2.4.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.5.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.7.0 = INTEGER: 1
    .1.3.6.1.4.1.2566.107.31.2.8.0 = INTEGER: 1
    '''
    testagent.register_snmpwalk_ouput(walk)
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_trusted_filter/check_snmp_trusted_filter.py -H localhost:1234",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == (
        "Critical - Filter Status. Power Supply 1: AC off. Power Supply 2: AC off | 'logfill'=80%%;;;;\n"
        "Power Supply 1: AC off\n"
        "Power Supply 2: AC off\n"
        "Fan 1: ok\n"
        "Fan 2: ok\n"
        "Battery: ok\n"
        "Temperature: ok\n"
        "Fill Level internal log: 80%\n"
        "Activity State: standby\n")
    testagent.unregister_all()

def test_stop_snmp_simulation():
    testagent.stop_server()

def test_no_agent():
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_trusted_filter/check_snmp_trusted_filter.py -H localhost:1234",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == "Unknown - SNMP response incomplete or invalid\n"

def test_no_host():
    p=subprocess.Popen("python health_monitoring_plugins/check_snmp_trusted_filter/check_snmp_trusted_filter.py -H 1.2.3.4:1234",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    assert p.stdout.read() == "Unknown - SNMP response incomplete or invalid\n"