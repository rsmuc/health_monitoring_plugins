import context
import subprocess
import testagent

testagent.configure(agent_address = "localhost:1234",
    rocommunity='public', rwcommunity='private')
testagent.start_server()

def test_mib_not_reachable():
    p=subprocess.Popen("health_monitoring_plugins/check_newtecmodem/check_newtecmodem.py -H 127.0.0.1:1234 -m MDM6000",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    p.wait()
    assert p.returncode == 3
    assert p.stdout.read() == "Unknown - SNMP response incomplete or invalid\n"
    p=subprocess.Popen("health_monitoring_plugins/check_newtecmodem/check_newtecmodem.py -H 127.0.0.1:1234 -m MDM6000",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    p.wait()
    assert p.returncode == 3
    assert p.stdout.read() == "Unknown - SNMP response incomplete or invalid\n"

def test_all_good():
    walk =  '''.1.3.6.1.4.1.5835.5.2.5700.1.3.3.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.5700.1.3.1.1.3.1 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.100.1.10.11.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.100.1.10.12.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.100.1.10.6.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.100.1.10.2.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.100.1.10.1.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.100.1.10.10.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.100.1.10.5.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.100.1.10.8.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.100.1.10.7.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.500.1.6.11.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.500.1.6.12.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.500.1.6.17.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.3500.1.1.1.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.4600.1.1.2.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.4600.1.1.1.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.100.1.9.2.0 = INTEGER: 251
               .1.3.6.1.4.1.5835.5.2.100.1.9.1.0 = INTEGER: 21'''
    testagent.register_snmpwalk_ouput(walk)
    p=subprocess.Popen("health_monitoring_plugins/check_newtecmodem/check_newtecmodem.py -H 127.0.0.1:1234 -m MDM6000",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    p.wait()
    assert p.returncode == 0
    assert p.stdout.read() == "Newtec MDM6000. Status: OK. | 'power_v'=2.51;;;; 'temp_deg_c'=21.0;;;;\n"
    p=subprocess.Popen("health_monitoring_plugins/check_newtecmodem/check_newtecmodem.py -H 127.0.0.1:1234 -m MDM9000",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    p.wait()
    assert p.returncode == 0
    assert p.stdout.read() == "Newtec MDM9000. Status: OK. | 'power_v'=2.51;;;; 'temp_deg_c'=21.0;;;;\n"

def test_some_alarms():
    testagent.unregister_all()
    walk =  '''.1.3.6.1.4.1.5835.5.2.5700.1.3.3.0 = INTEGER: 1
               .1.3.6.1.4.1.5835.5.2.5700.1.3.1.1.3.1 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.100.1.10.11.0 = INTEGER: 1
               .1.3.6.1.4.1.5835.5.2.100.1.10.12.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.100.1.10.6.0 = INTEGER: 1
               .1.3.6.1.4.1.5835.5.2.100.1.10.2.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.100.1.10.1.0 = INTEGER: 1
               .1.3.6.1.4.1.5835.5.2.100.1.10.10.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.100.1.10.5.0 = INTEGER: 1
               .1.3.6.1.4.1.5835.5.2.100.1.10.8.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.100.1.10.7.0 = INTEGER: 1
               .1.3.6.1.4.1.5835.5.2.500.1.6.11.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.500.1.6.12.0 = INTEGER: 1
               .1.3.6.1.4.1.5835.5.2.500.1.6.17.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.3500.1.1.1.0 = INTEGER: 1
               .1.3.6.1.4.1.5835.5.2.4600.1.1.2.0 = INTEGER: 0
               .1.3.6.1.4.1.5835.5.2.4600.1.1.1.0 = INTEGER: 1
               .1.3.6.1.4.1.5835.5.2.100.1.9.2.0 = INTEGER: 251
               .1.3.6.1.4.1.5835.5.2.100.1.9.1.0 = INTEGER: 21'''
    testagent.register_snmpwalk_ouput(walk)
    p=subprocess.Popen("health_monitoring_plugins/check_newtecmodem/check_newtecmodem.py -H 127.0.0.1:1234 -m MDM6000",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    p.wait()
    assert p.returncode == 2
    assert p.stdout.read() == (
        "Newtec MDM6000. Status: 7 alarms active. | 'power_v'=2.51;;;; 'temp_deg_c'=21.0;;;;\n"
        "Alarm: Antenna non-functional\n"
        "Alarm: Frontpanel communication failed\n"
        "Alarm: General device failure\n"
        "Alarm: License file non-existent or wrongly signed\n"
        "Alarm: Software upgrade failed\n"
        "Alarm: Failure is detected on data ethernet interface\n"
        "Alarm: Fan failure\n")
    p=subprocess.Popen("health_monitoring_plugins/check_newtecmodem/check_newtecmodem.py -H 127.0.0.1:1234 -m MDM9000",
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    p.wait()
    assert p.returncode == 2
    assert p.stdout.read() == (
        "Newtec MDM9000. Status: 9 alarms active. | 'power_v'=2.51;;;; 'temp_deg_c'=21.0;;;;\n"
        "Alarm: Antenna non-functional\n"
        "Alarm: Hardware malfunction\n"
        "Alarm: Frontpanel communication failed\n"
        "Alarm: General device failure\n"
        "Alarm: License file non-existent or wrongly signed\n"
        "Alarm: Software upgrade failed\n"
        "Alarm: Failure is detected on data ethernet interface\n"
        "Alarm: Fan failure\n"
        "Alarm: Converter not working due to hardware failures\n")

def test_stop_server():
    testagent.stop_server()
