#!/usr/bin/python
import context
import health_monitoring_plugins.meinberg
import subprocess
from testagent import *


#############
# Unittests #
#############

# 0: ok
# 1: warning
# 2: critical
# 3: unknown

def test_check_gps_status():
    """ test the check_gps_status function"""
    ################
    # OLD FIRMWARE #
    ################
    meinberg = health_monitoring_plugins.meinberg.Meinberg(None, "LEGACY")
    # Integer -> unknown
    assert meinberg.check_gps_status(1) == (3, 'GPS status: unknown')
    # Unknown string -> unknown
    assert meinberg.check_gps_status("invalidstring") == (3, 'GPS status: unknown')
    # Valid string but not ok -> Warning
    assert meinberg.check_gps_status("5") == (1, 'GPS status: coldBoot')
    # Valid string normal operation -> we do not show a status
    assert meinberg.check_gps_status("1") is None

    ###############
    # NG FIRMWARE #
    ###############
    meinberg = health_monitoring_plugins.meinberg.Meinberg(None, "NG")
    # Integer -> unknown
    assert meinberg.check_gps_status(1) == (3, 'GPS status: unknown')
    # Unknown string -> unknown
    assert meinberg.check_gps_status("invalidstring") == (3, 'GPS status: unknown')
    # Valid string but not ok -> Warning
    assert meinberg.check_gps_status("5") == (1, 'GPS status: gpsColdBoot')
    # Valid string normal operation -> we do not show a status
    assert meinberg.check_gps_status("1") is None


def test_check_ntp_status():
    """ test the check_ntp_status function"""
    ################
    # OLD FIRMWARE #
    ################
    meinberg = health_monitoring_plugins.meinberg.Meinberg(None, "LEGACY")
    # Integer -> unknown
    assert meinberg.check_ntp_status(1) == (3, 'NTP status: unknown')
    # Unknown string -> unknown
    assert meinberg.check_ntp_status("invalidstring") == (3, 'NTP status: unknown')
    # Valid string but not ok -> Critical
    assert meinberg.check_ntp_status("0") == (2, 'NTP status: notSynchronized')
    # Valid string normal operation -> we do not show a status
    assert meinberg.check_ntp_status("4") is None

    ###############
    # NG FIRMWARE #
    ###############
    meinberg = health_monitoring_plugins.meinberg.Meinberg(None, "NG")
    # Integer -> unknown
    assert meinberg.check_ntp_status(1) == (3, 'NTP status: unknown')
    # Unknown string -> unknown
    assert meinberg.check_ntp_status("invalidstring") == (3, 'NTP status: unknown')
    # Valid string but not ok -> Critical
    assert meinberg.check_ntp_status("1") == (2, 'NTP status: notSynchronized')
    # Valid string normal operation -> we do not show a status
    assert meinberg.check_ntp_status("2") is None

####################
# integration test #
####################

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address="localhost:1234", rocommunity='public', rwcommunity='private')


def test_start():
    # start the testagent
    # Gauge32 are not working - So I replaced them by INTEGER
    # Old Firmware # Everything ok
    walk = '''
            iso.3.6.1.4.1.5597.3.1.2.0 = INTEGER: 4
            iso.3.6.1.4.1.5597.3.2.7.0 = STRING: "GPS Position: 48.1276 11.6124 619m"
            iso.3.6.1.4.1.5597.3.2.9.0 = INTEGER: 7
            iso.3.6.1.4.1.5597.3.2.16.0 = INTEGER: 1
            '''
    register_snmpwalk_ouput(walk)
    start_server()


def test_system_test_meinberg(capsys):
    # without options
    p = subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py", shell=True,
                         stderr=subprocess.PIPE)
    assert "check_meinberg_ntp.py: error: Hostname must be specified" in p.stderr.read()

    # without -H 1.2.3.4 (unknown host)
    p = subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H 1.2.3.4 --snmptimeout 3", shell=True,
                         stdout=subprocess.PIPE)
    assert "Unknown - No response from device for oid .1.3.6.1.4.1.5597.3.2.7.0" in p.stdout.read()

    # with --help
    p = subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py --help", shell=True,
                         stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()


def test_snmpv3(capsys):
    # not reachable

    p = subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py" + " -H 1.2.3.4 -V 3 "
                                                                                                "-U nothinguseful -L authNoPriv -a MD5 "
                                                                                                "-A nothinguseful -x DES -X nothinguseful --snmptimeout 3",
                         shell=True, stdout=subprocess.PIPE)
    assert "Unknown - No response from device for oid .1.3.6.1.4.1.5597.3.2.7.0" in p.stdout.read()


############################################
# integration tests with the new firmware #
###########################################

def test_with_host_ok():
    # everything ok
    p = subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234",
                         shell=True, stdout=subprocess.PIPE)
    assert "OK - GPS Position: 48.1276 11.6124 619m. Good satellites: 7 | 'satellites'=7;;;;\n" in p.stdout.read()


def test_less_satellites_warning():
    # warning threshold 8 satellites
    p = subprocess.Popen(
        "health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234 --threshold metric=satellites,warning=8:,critical=2:",
        shell=True, stdout=subprocess.PIPE)
    assert "Warning - GPS Position: 48.1276 11.6124 619m. Good satellites: 7. Warning on satellites | 'satellites'=7;8:;2:;;\n" in p.stdout.read()


def test_less_satellites_critical():
    # critical threhold 8 satellites
    p = subprocess.Popen(
        "health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234 --threshold metric=satellites,warning=9:,critical=8:",
        shell=True, stdout=subprocess.PIPE)
    assert "Critical - GPS Position: 48.1276 11.6124 619m. Good satellites: 7. Critical on satellites | 'satellites'=7;9:;8:;;\n" in p.stdout.read()


def test_with_host_ok_old_firmware_flag():
    # everything ok
    p = subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234 -m 1",
                         shell=True, stdout=subprocess.PIPE)
    assert "OK - GPS Position: 48.1276 11.6124 619m. Good satellites: 7 | 'satellites'=7;;;;\n" in p.stdout.read()


def test_old_firmware_ntp_status():
    # start the testagent
    # Old Firmware # NTP not ok and gps not ok
    unregister_all()
    walk = '''
            iso.3.6.1.4.1.5597.3.1.2.0 = INTEGER: 0
            iso.3.6.1.4.1.5597.3.2.7.0 = STRING: "GPS Position: 48.1276 11.6124 619m"
            iso.3.6.1.4.1.5597.3.2.9.0 = INTEGER: 7
            iso.3.6.1.4.1.5597.3.2.16.0 = INTEGER: 0
            '''

    register_snmpwalk_ouput(walk)

    p = subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234 -m 1",
                         shell=True, stdout=subprocess.PIPE)
    assert "Critical - GPS Position: 48.1276 11.6124 619m. NTP status: notSynchronized. GPS status: notavailable. Good satellites: 7 | 'satellites'=7;;;;\n" in p.stdout.read()


############################################
# integration tests with the new firmware #
###########################################


def test_start_ng():
    # start simulation of new firmware
    # everything is ok
    unregister_all()
    walk = '''
            iso.3.6.1.4.1.5597.30.0.2.1.0 = INTEGER: 2
            iso.3.6.1.4.1.5597.30.0.1.5.0 = STRING: "GPS Position: 48.1276 11.6124 619m"
            iso.3.6.1.4.1.5597.30.0.1.2.1.6.1 = INTEGER: 7
            iso.3.6.1.4.1.5597.30.0.1.2.1.5.1 = INTEGER: 1
            '''
    register_snmpwalk_ouput(walk)


def test_with_host_ok_ng():
    # everything ok
    p = subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234 -m NG",
                         shell=True, stdout=subprocess.PIPE)
    assert "OK - GPS Position: 48.1276 11.6124 619m. Good satellites: 7 | 'satellites'=7;;;;\n" in p.stdout.read()


def test_less_satellites_warning_ng():
    # warning threhold 8 satellites
    p = subprocess.Popen(
        "health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234 -m NG --threshold metric=satellites,warning=8:,critical=2:",
        shell=True, stdout=subprocess.PIPE)
    assert "Warning - GPS Position: 48.1276 11.6124 619m. Good satellites: 7. Warning on satellites | 'satellites'=7;8:;2:;;\n" in p.stdout.read()


def test_less_satellites_critical_ng():
    # critical threhold 8 satellites
    p = subprocess.Popen(
        "health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234 -m NG --threshold metric=satellites,warning=9:,critical=8:",
        shell=True, stdout=subprocess.PIPE)
    assert "Critical - GPS Position: 48.1276 11.6124 619m. Good satellites: 7. Critical on satellites | 'satellites'=7;9:;8:;;\n" in p.stdout.read()


def test_ntp_status_ng():
    # start the testagent
    # Old Firmware # NTP not ok and gps not ok
    unregister_all()
    walk = '''
            iso.3.6.1.4.1.5597.30.0.2.1.0 = INTEGER: 1
            iso.3.6.1.4.1.5597.30.0.1.5.0 = STRING: "GPS Position: 48.1276 11.6124 619m"
            iso.3.6.1.4.1.5597.30.0.1.2.1.6.1 = INTEGER: 7
            iso.3.6.1.4.1.5597.30.0.1.2.1.5.1 = INTEGER: 0
            '''
    register_snmpwalk_ouput(walk)

    p = subprocess.Popen("health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py -H localhost:1234 -m NG",
                         shell=True, stdout=subprocess.PIPE)
    assert "Critical - GPS Position: 48.1276 11.6124 619m. NTP status: notSynchronized. GPS status: notAvailable. Good satellites: 7 | 'satellites'=7;;;;\n" in p.stdout.read()


def test_stop():
    # stop the testagent
    stop_server()
