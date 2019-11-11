import context
import subprocess
import testagent

testagent.configure(agent_address = "localhost:1234",
    rocommunity='public', rwcommunity='private')
testagent.start_server()

def notest_mib_not_reachable():
    p=subprocess.Popen(("health_monitoring_plugins/check_microwavemodem/check_microwavemodem.py -H 127.0.0.1:1234 -m SK-IP"),
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    p.wait()
    assert p.returncode == 3
    assert p.stdout.read() == "Unknown - SNMP response incomplete or invalid\n"
    p=subprocess.Popen(("health_monitoring_plugins/check_microwavemodem/check_microwavemodem.py -H 127.0.0.1:1234 -m AX-60"),
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    p.wait()
    assert p.returncode == 3
    assert p.stdout.read() == "Unknown - SNMP response incomplete or invalid\n"

def test_all_good():
    walk =  '''.1.3.6.1.4.1.29890.1.6.2.4.3.8.0 = INTEGER: 40
               .1.3.6.1.4.1.29890.1.6.2.4.3.9.0 = INTEGER: 40
               .1.3.6.1.4.1.29890.1.6.2.4.3.5.0 = INTEGER: 40
               .1.3.6.1.4.1.29890.1.6.2.4.3.6.0 = INTEGER: 40
               .1.3.6.1.4.1.29890.1.6.2.4.3.4.0 = INTEGER: 40
               .1.3.6.1.4.1.29890.1.6.2.4.3.7.0 = INTEGER: 40
               .1.3.6.1.4.1.29890.1.6.2.4.3.1.0 = INTEGER: 40
               .1.3.6.1.4.1.29890.1.6.2.4.4.2.1.0 = INTEGER: 100
               .1.3.6.1.4.1.29890.1.6.2.4.4.2.2.0 = INTEGER: 120
               .1.3.6.1.4.1.29890.1.6.2.4.4.2.3.0 = INTEGER: 250
               .1.3.6.1.4.1.29890.1.6.2.4.4.2.4.0 = INTEGER: 250
               .1.3.6.1.4.1.29890.1.6.2.4.4.2.5.0 = INTEGER: 330
               .1.3.6.1.4.1.29890.1.6.2.4.4.2.6.0 = INTEGER: 500
               .1.3.6.1.4.1.29890.1.6.2.4.4.2.7.0 = INTEGER: 900
               .1.3.6.1.4.1.29890.1.8.1.4.3.7.0 = INTEGER: 40000
               .1.3.6.1.4.1.29890.1.8.1.4.3.8.0 = INTEGER: 40000
               .1.3.6.1.4.1.29890.1.8.1.4.3.4.0 = INTEGER: 40000
               .1.3.6.1.4.1.29890.1.8.1.4.3.5.0 = INTEGER: 40000
               .1.3.6.1.4.1.29890.1.8.1.4.3.9.0 = INTEGER: 40000
               .1.3.6.1.4.1.29890.1.8.1.4.3.10.0 = INTEGER: 40000
               .1.3.6.1.4.1.29890.1.8.1.4.3.1.0 = INTEGER: 40000
               .1.3.6.1.4.1.29890.1.6.2.6.2.0 = STRING: "0000 0010"
               .1.3.6.1.4.1.29890.1.6.2.6.3.0 = STRING: "0000 0001"
               .1.3.6.1.4.1.29890.1.8.1.6.1.0 = INTEGER: 0'''
    testagent.register_snmpwalk_ouput(walk)
    p=subprocess.Popen(("health_monitoring_plugins/check_microwavemodem/check_microwavemodem.py -H 127.0.0.1:1234 -m SK-IP"),
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    p.wait()
    assert p.returncode == 2
    assert p.stdout.read() == (
        "WORK Microwave SK-IP Modem. System status: 1 error(s). Demodulator status: 1 warning(s). | "
        "'volt_dmd7'=9.0;;;; 'temp_demod_deg_c'=40.0;;;; 'volt_dmd5'=3.3;;;; 'volt_dmd4'=2.5;;;; "
        "'temp_demod_psu_deg_c'=40.0;;;; 'volt_dmd2'=1.2;;;; 'volt_dmd1'=1.0;;;; 'volt_dmd6'=5.0;;;; "
        "'temp_cpu2_deg_c'=40.0;;;; 'temp_ctl1_deg_c'=40.0;;;; 'temp_ctl2_deg_c'=40.0;;;; 'volt_dmd3'=2.5;;;; "
        "'temp_frontpanel_deg_c'=40.0;;;; 'temp_cpu1_deg_c'=40.0;;;;\n"
        "System: Mod. communication alarm\n"
        "Demodulator: FIFO full warning\n")
    p=subprocess.Popen(("health_monitoring_plugins/check_microwavemodem/check_microwavemodem.py -H 127.0.0.1:1234 -m AX-60"),
                       shell=True, stdout=subprocess.PIPE, env=context.testenv)
    p.wait()
    assert p.returncode == 0
    assert p.stdout.read() == (
        "WORK Microwave AX-60 Modem. Global status: Ok. | 'temp_cpu_board_deg_c'=40.0;;;; "
        "'temp_cpu_deg_c'=40.0;;;; 'temp_demodulator_deg_c'=40.0;;;; 'temp_device_deg_c'=40.0;;;; "
        "'temp_bridge_chip_deg_c'=40.0;;;; 'temp_demodulator_board_deg_c'=40.0;;;; 'temp_bridge_board_deg_c'=40.0;;;;\n")

def test_stop_server():
    testagent.stop_server()
