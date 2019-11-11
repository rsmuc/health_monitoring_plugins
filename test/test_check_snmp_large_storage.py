#!/usr/bin/python
import context
import netsnmp
import subprocess
from health_monitoring_plugins.storage import *
from testagent import *

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address="localhost:1234",
          rocommunity='public', rwcommunity='private')

# create netsnmp Sessions for test_get and test_walk_data
session = netsnmp.Session(Version=2, DestHost='localhost', Community='public')
failSession = netsnmp.Session(Version=2, DestHost='1.2.3.4', Community='public')


def test_start():
    # linux host  
    walk = '''.1.3.6.1.2.1.25.2.3.1.1.10 = INTEGER: 10
            .1.3.6.1.2.1.25.2.3.1.1.31 = INTEGER: 31
            .1.3.6.1.2.1.25.2.3.1.3.10 = STRING: Swap space
            .1.3.6.1.2.1.25.2.3.1.3.31 = STRING: /
            .1.3.6.1.2.1.25.2.3.1.4.10 = INTEGER: 1024
            .1.3.6.1.2.1.25.2.3.1.4.31 = INTEGER: 4096
            .1.3.6.1.2.1.25.2.3.1.5.10 = INTEGER: 1324028
            .1.3.6.1.2.1.25.2.3.1.5.31 = INTEGER: 7381523
            .1.3.6.1.2.1.25.2.3.1.6.10 = INTEGER: 12504
            .1.3.6.1.2.1.25.2.3.1.6.31 = INTEGER: 628056'''
    register_snmpwalk_ouput(walk)
    start_server()


def test_calculate_real_size():
    """
    test calculate_real_size
    """
    assert calculate_real_size(5) == 5
    assert calculate_real_size(-5) == 2147483652


def test_partition_found():
    """
    test partition_found(partition, description)
    """
    assert partition_found("/etc", "/etc") == True
    assert partition_found("/etc", "/etc/var/bin/test") == False
    assert partition_found("C:\\", "C:\\ Data Test ID x123") == True
    assert partition_found("C:\\", "D:\\") == False


# def test_convert_to_XX(capsys):
#     """
#     test convert_to_XX(value, unit, targetunit)
#     """
#     assert convert_to("1024", "4096", "MB") == 4
#     assert convert_to("1048576", "4096", "GB") == 4
#     assert convert_to("1073741824", "4096", "TB") == 4
#     with pytest.raises(SystemExit):
#         convert_to("1024", "4096", "XYZ")
#     out, err = capsys.readouterr()
#     assert "Unknown - Wrong targetunit: XYZ\n" == out


def test_snmpv3(capsys):
    # not reachable

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_idrac/check_snmp_idrac.py' + " -H 1.2.3.4 -V 3 "
                                                                           "-U nothinguseful -L authNoPriv -a MD5 "
                                                                           "-A nothinguseful -x DES -X nothinguseful --snmptimeout 3",
        shell=True, stdout=subprocess.PIPE)
    assert "Unknown - No response from device for oid .1.3.6.1.2.1.1.5.0" in p.stdout.read()


def test_without_options(capsys):
    # without options
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_service/check_snmp_service.py",
                         shell=True, stderr=subprocess.PIPE)
    assert "Hostname must be specified\n" in p.stderr.read()


def test_help():
    # with --help
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_large_storage/check_snmp_large_storage.py --help",
        shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()


def test_scan():
    # scan
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_large_storage/check_snmp_large_storage.py -H 127.0.0.1:1234",
        shell=True, stdout=subprocess.PIPE)
    assert "All available disks at: 127.0.0.1:1234\nDisk: \t'Swap space'" in p.stdout.read()


def test_root_partition():
    # root partition
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_large_storage/check_snmp_large_storage.py -H 127.0.0.1:1234 -p /",
        shell=True, stdout=subprocess.PIPE)
    assert "OK - 8.51% used (2.4GB of 28.16GB) at '/' | 'percent used'=8.51%;;;0;100" in p.stdout.read()


def test_root_partition_warning():
    # root partition in warning
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_large_storage/check_snmp_large_storage.py -H 127.0.0.1:1234 -p / --threshold metric='percent used',warning=5..inf,critical=95..inf",
        shell=True, stdout=subprocess.PIPE)
    assert "Warning - 8.51% used (2.4GB of 28.16GB) at '/'. Warning on percent used | 'percent used'=8.51%;~:5;~:95;0;100\n" in p.stdout.read()


def test_root_partition_in_tb():
    # root partition in TB
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_large_storage/check_snmp_large_storage.py -H 127.0.0.1:1234 -p / -u TB",
        shell=True, stdout=subprocess.PIPE)
    assert "OK - 8.51% used (0.0TB of 0.03TB) at '/' | 'percent used'=8.51%;;;0;100\n" in p.stdout.read()


def test_root_partition_in_mb():
    # root partition in TB
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_large_storage/check_snmp_large_storage.py -H 127.0.0.1:1234 -p / -u MB",
        shell=True, stdout=subprocess.PIPE)
    assert "OK - 8.51% used (2453.34MB of 28834.07MB) at '/' | 'percent used'=8.51%;;;0;100\n" in p.stdout.read()


def test_stop():
    # stop the testagent
    stop_server()
