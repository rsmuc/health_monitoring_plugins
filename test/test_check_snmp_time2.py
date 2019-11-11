#!/usr/bin/python
import context
import netsnmp
import subprocess
from health_monitoring_plugins.timesource import *
from testagent import *

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
configure(agent_address="localhost:1234",
          rocommunity='public', rwcommunity='private')

# create netsnmp Session  for test_attempt_get and test_walk
session = netsnmp.Session(Version=2, DestHost='localhost', Community='public')
failSession = netsnmp.Session(Version=2, DestHost='1.2.3.4', Community='public')


def get_system_uptime():
    """
    just a helper to get the system uptime in seconds
    """
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = str(f.readline().split()[0])
        uptime_seconds = uptime_seconds.replace('.', '')
        return str(uptime_seconds)


def test_start():
    # Time Stamp of Linux system  
    walk = '''.1.3.6.1.2.1.25.1.2.0 = STRING: \x07\xe0\x05\x0e\x13\x04\x1d\x10+\x02\x02
            .1.3.6.1.2.1.1.1.0 = STRING: Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64
            '''
    register_snmpwalk_ouput(walk)
    start_server()


def test_without_options():
    # without options
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py",
                         shell=True, stderr=subprocess.PIPE)
    assert "Hostname must be specified\n" in p.stderr.read()


def test_help():
    # with --help
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py --help",
                         shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()


def test_snmpv3(capsys):
    # not reachable

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py' + " -H 1.2.3.4 -V 3 "
                                                                           "-U nothinguseful -L authNoPriv -a MD5 "
                                                                           "-A nothinguseful -x DES -X nothinguseful --snmptimeout 3",
        shell=True, stdout=subprocess.PIPE)
    assert "Unknown - No response from device for oid" in p.stdout.read()


def test_linux_no_threshold():
    # high offset, but no threshold is set
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H 127.0.0.1:1234",
        shell=True, stdout=subprocess.PIPE)
    assert "OK - Remote (UTC): 17:02:29. Offset =" in p.stdout.read()


def test_linux_with_threshold():
    # high offset, but threshold => critical
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H 127.0.0.1:1234 --th metric=offset,warning=-5:5,critical=-15:15",
        shell=True, stdout=subprocess.PIPE)
    assert "Critical - Remote (UTC): 17:02:29. Offset = " in p.stdout.read()


def test_linux_with_threshold_localhost():
    # no offset, set threshold => OK
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H 127.0.0.1 --th metric=offset,warning=-5:5,critical=-15:15",
        shell=True, stdout=subprocess.PIPE)
    assert "Offset = 0 s | 'offset'=0.0;-5:5;-15:15;" in p.stdout.read()


def test_windows():
    # Time Stamp of Windows system  
    unregister_all()
    walk = '''.1.3.6.1.2.1.25.1.2.0 = STRING: \x07\xe0\x05\x0e\x13\x04\x1d\x10
            .1.3.6.1.2.1.1.1.0 = STRING: Hardware: Intel64 Family 6 Model 23 Stepping 10 AT/AT COMPATIBLE - Software: Windows Version 6.3 (Build 10586 Multiprocessor Free)
            '''
    register_snmpwalk_ouput(walk)
    p = subprocess.Popen(
        "health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H 127.0.0.1:1234 --th metric=offset,warning=-5:5,critical=-15:15",
        shell=True, stdout=subprocess.PIPE)
    assert "Critical on offset | 'offset'=" in p.stdout.read()


def test_plus_two_hours():
    unregister_all()
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.25.1.2.0 = STRING: "\x07\xe0\x04\x09\x0b\x04\x2b\x01+\x02\x01"''')
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.1.1.0 = STRING: "Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64"''')

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H localhost:1234',
        shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Remote (UTC): 2016.04.09 09:03:43' in cmd_output


def test_plus_thirty_minutes():
    unregister_all()

    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.25.1.2.0 = STRING: "\x07\xe0\x04\x03\x03\x0f\x2b\x01+\x01\x1e"''')
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.1.1.0 = STRING: "Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64"''')

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H localhost:1234',
        shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Remote (UTC): 2016.04.03 01:45:43' in cmd_output


def test_minus_two_hours():
    unregister_all()

    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.25.1.2.0 = STRING: "\x07\xe0\x04\x03\x16\x01\x2b\x01-\x02\x01"''')
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.1.1.0 = STRING: "Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64"''')

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H localhost:1234',
        shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Remote (UTC): 2016.04.04 00:02:43' in cmd_output


def test_minus_two_hours():
    unregister_all()

    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.25.1.2.0 = STRING: "\x07\xe0\x04\x03\x16\x1e\x2b\x01-\x01\x1e"''')
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.1.1.0 = STRING: "Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64"''')

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H localhost:1234',
        shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Remote (UTC): 2016.04.04 00:00:43' in cmd_output


def test_feb_to_mar_leap_year_minus():
    unregister_all()

    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.25.1.2.0 = STRING: "\x07\xe0\x02\x1d\x16\x1e\x2b\x01-\x01\x1e"''')
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.1.1.0 = STRING: "Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64"''')

    the_time = struct.unpack('BBBBBBBBcBB', '\x07\xe0\x02\x1d\x16\x1e\x2b\x01-\x01\x1e')

    the_year = (the_time[0] * 256) + the_time[1]

    print 'Year: %d' % the_year  # year
    print 'Month: %d' % the_time[2]  # month
    print 'Day: %d' % the_time[3]  # day
    print 'Hour: %d' % the_time[4]  # hours
    print 'Minute: %d' % the_time[5]  # minutes
    print 'Second: %d' % the_time[6]  # seconds
    print 'Offset-hour: %d' % the_time[9]  # offset-
    print 'Offset-minute: %d' % the_time[10]  # offset-

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H localhost:1234',
        shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Remote (UTC): 2016.03.01 00:00:43' in cmd_output


def test_feb_to_mar_minus():
    unregister_all()

    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.25.1.2.0 = STRING: "\x07\xdf\x02\x1c\x16\x1e\x2b\x01-\x01\x1e"''')
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.1.1.0 = STRING: "Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64"''')

    the_time = struct.unpack('BBBBBBBBcBB', '\x07\xdf\x02\x1c\x16\x1e\x2b\x01-\x01\x1e')

    the_year = (the_time[0] * 256) + the_time[1]

    print 'Year: %d' % the_year  # year
    print 'Month: %d' % the_time[2]  # month
    print 'Day: %d' % the_time[3]  # day
    print 'Hour: %d' % the_time[4]  # hours
    print 'Minute: %d' % the_time[5]  # minutes
    print 'Second: %d' % the_time[6]  # seconds
    print 'Offset-hour: %d' % the_time[9]  # offset-
    print 'Offset-minute: %d' % the_time[10]  # offset-

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H localhost:1234',
        shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Remote (UTC): 2015.03.01 00:00:43' in cmd_output


def test_mar_to_feb_leap_year_plus():
    unregister_all()

    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.25.1.2.0 = STRING: "\x07\xe0\x03\x01\x01\x1d\x2b\x01+\x01\x1e"''')
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.1.1.0 = STRING: "Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64"''')

    the_time = struct.unpack('BBBBBBBBcBB', '\x07\xe0\x03\x01\x01\x1d\x2b\x01+\x01\x1e')

    the_year = (the_time[0] * 256) + the_time[1]

    print 'Year: %d' % the_year  # year
    print 'Month: %d' % the_time[2]  # month
    print 'Day: %d' % the_time[3]  # day
    print 'Hour: %d' % the_time[4]  # hours
    print 'Minute: %d' % the_time[5]  # minutes
    print 'Second: %d' % the_time[6]  # seconds
    print 'Offset-hour: %d' % the_time[9]  # offset-
    print 'Offset-minute: %d' % the_time[10]  # offset-

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H localhost:1234',
        shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Remote (UTC): 2016.02.29 23:59:43' in cmd_output


def test_mar_to_feb_plus():
    unregister_all()

    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.25.1.2.0 = STRING: "\x07\xdf\x03\x01\x01\x1d\x2b\x01+\x01\x1e"''')
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.1.1.0 = STRING: "Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64"''')

    the_time = struct.unpack('BBBBBBBBcBB', '\x07\xdf\x03\x01\x01\x1d\x2b\x01+\x01\x1e')

    the_year = (the_time[0] * 256) + the_time[1]

    print 'Year: %d' % the_year  # year
    print 'Month: %d' % the_time[2]  # month
    print 'Day: %d' % the_time[3]  # day
    print 'Hour: %d' % the_time[4]  # hours
    print 'Minute: %d' % the_time[5]  # minutes
    print 'Second: %d' % the_time[6]  # seconds
    print 'Offset-hour: %d' % the_time[9]  # offset-
    print 'Offset-minute: %d' % the_time[10]  # offset-

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H localhost:1234',
        shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Remote (UTC): 2015.02.28 23:59:43' in cmd_output


def test_feb_to_jan_leap_year_plus():
    unregister_all()

    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.25.1.2.0 = STRING: "\x07\xe0\x02\x01\x01\x1d\x2b\x01+\x01\x1e"''')
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.1.1.0 = STRING: "Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64"''')

    the_time = struct.unpack('BBBBBBBBcBB', '\x07\xe0\x02\x01\x01\x1d\x2b\x01+\x01\x1e')

    the_year = (the_time[0] * 256) + the_time[1]

    print 'Year: %d' % the_year  # year
    print 'Month: %d' % the_time[2]  # month
    print 'Day: %d' % the_time[3]  # day
    print 'Hour: %d' % the_time[4]  # hours
    print 'Minute: %d' % the_time[5]  # minutes
    print 'Second: %d' % the_time[6]  # seconds
    print 'Offset-hour: %d' % the_time[9]  # offset-
    print 'Offset-minute: %d' % the_time[10]  # offset-

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H localhost:1234',
        shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Remote (UTC): 2016.01.31 23:59:43' in cmd_output


def test_feb_to_jan_plus():
    unregister_all()

    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.25.1.2.0 = STRING: "\x07\xdf\x02\x01\x01\x1d\x2b\x01+\x01\x1e"''')
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.1.1.0 = STRING: "Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64"''')

    the_time = struct.unpack('BBBBBBBBcBB', '\x07\xdf\x02\x01\x01\x1d\x2b\x01+\x01\x1e')

    the_year = (the_time[0] * 256) + the_time[1]

    print 'Year: %d' % the_year  # year
    print 'Month: %d' % the_time[2]  # month
    print 'Day: %d' % the_time[3]  # day
    print 'Hour: %d' % the_time[4]  # hours
    print 'Minute: %d' % the_time[5]  # minutes
    print 'Second: %d' % the_time[6]  # seconds
    print 'Offset-hour: %d' % the_time[9]  # offset-
    print 'Offset-minute: %d' % the_time[10]  # offset-

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H localhost:1234',
        shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Remote (UTC): 2015.01.31 23:59:43' in cmd_output


def test_aug_to_jul_leap_year_plus():
    unregister_all()

    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.25.1.2.0 = STRING: "\x07\xe0\x08\x01\x01\x1d\x2b\x01+\x01\x1e"''')
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.1.1.0 = STRING: "Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64"''')

    the_time = struct.unpack('BBBBBBBBcBB', '\x07\xe0\x08\x01\x01\x1d\x2b\x01+\x01\x1e')

    the_year = (the_time[0] * 256) + the_time[1]

    print 'Year: %d' % the_year  # year
    print 'Month: %d' % the_time[2]  # month
    print 'Day: %d' % the_time[3]  # day
    print 'Hour: %d' % the_time[4]  # hours
    print 'Minute: %d' % the_time[5]  # minutes
    print 'Second: %d' % the_time[6]  # seconds
    print 'Offset-hour: %d' % the_time[9]  # offset-
    print 'Offset-minute: %d' % the_time[10]  # offset-

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H localhost:1234',
        shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Remote (UTC): 2016.07.31 23:59:43' in cmd_output


def test_aug_to_jul_plus():
    unregister_all()

    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.25.1.2.0 = STRING: "\x07\xdf\x08\x01\x01\x1d\x2b\x01+\x01\x1e"''')
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.1.1.0 = STRING: "Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64"''')

    the_time = struct.unpack('BBBBBBBBcBB', '\x07\xdf\x08\x01\x01\x1d\x2b\x01+\x01\x1e')

    the_year = (the_time[0] * 256) + the_time[1]

    print 'Year: %d' % the_year  # year
    print 'Month: %d' % the_time[2]  # month
    print 'Day: %d' % the_time[3]  # day
    print 'Hour: %d' % the_time[4]  # hours
    print 'Minute: %d' % the_time[5]  # minutes
    print 'Second: %d' % the_time[6]  # seconds
    print 'Offset-hour: %d' % the_time[9]  # offset-
    print 'Offset-minute: %d' % the_time[10]  # offset-

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H localhost:1234',
        shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Remote (UTC): 2015.07.31 23:59:43' in cmd_output


def test_jun_to_jul_leap_year_minus():
    unregister_all()

    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.25.1.2.0 = STRING: "\x07\xe0\x06\x1e\x16\x1e\x2b\x01-\x01\x1e"''')
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.1.1.0 = STRING: "Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64"''')

    the_time = struct.unpack('BBBBBBBBcBB', '\x07\xe0\x06\x1e\x16\x1e\x2b\x01-\x01\x1e')

    the_year = (the_time[0] * 256) + the_time[1]

    print 'Year: %d' % the_year  # year
    print 'Month: %d' % the_time[2]  # month
    print 'Day: %d' % the_time[3]  # day
    print 'Hour: %d' % the_time[4]  # hours
    print 'Minute: %d' % the_time[5]  # minutes
    print 'Second: %d' % the_time[6]  # seconds
    print 'Offset-hour: %d' % the_time[9]  # offset-
    print 'Offset-minute: %d' % the_time[10]  # offset-

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H localhost:1234',
        shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Remote (UTC): 2016.07.01 00:00:43' in cmd_output


def test_jun_to_jul_minus():
    unregister_all()

    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.25.1.2.0 = STRING: "\x07\xdf\x06\x1e\x16\x1e\x2b\x01-\x01\x1e"''')
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.1.1.0 = STRING: "Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64"''')

    the_time = struct.unpack('BBBBBBBBcBB', '\x07\xdf\x06\x1e\x16\x1e\x2b\x01-\x01\x1e')

    the_year = (the_time[0] * 256) + the_time[1]

    print 'Year: %d' % the_year  # year
    print 'Month: %d' % the_time[2]  # month
    print 'Day: %d' % the_time[3]  # day
    print 'Hour: %d' % the_time[4]  # hours
    print 'Minute: %d' % the_time[5]  # minutes
    print 'Second: %d' % the_time[6]  # seconds
    print 'Offset-hour: %d' % the_time[9]  # offset-
    print 'Offset-minute: %d' % the_time[10]  # offset-

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H localhost:1234',
        shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Remote (UTC): 2015.07.01 00:00:43' in cmd_output


def test_jul_to_jun_leap_year_plus():
    unregister_all()

    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.25.1.2.0 = STRING: "\x07\xe0\x07\x01\x01\x1d\x2b\x01+\x01\x1e"''')
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.1.1.0 = STRING: "Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64"''')

    the_time = struct.unpack('BBBBBBBBcBB', '\x07\xe0\x07\x01\x01\x1d\x2b\x01+\x01\x1e')

    the_year = (the_time[0] * 256) + the_time[1]

    print 'Year: %d' % the_year  # year
    print 'Month: %d' % the_time[2]  # month
    print 'Day: %d' % the_time[3]  # day
    print 'Hour: %d' % the_time[4]  # hours
    print 'Minute: %d' % the_time[5]  # minutes
    print 'Second: %d' % the_time[6]  # seconds
    print 'Offset-hour: %d' % the_time[9]  # offset-
    print 'Offset-minute: %d' % the_time[10]  # offset-

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H localhost:1234',
        shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Remote (UTC): 2016.06.30 23:59:43' in cmd_output


def test_jul_to_jun_plus():
    unregister_all()

    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.25.1.2.0 = STRING: "\x07\xdf\x07\x01\x01\x1d\x2b\x01+\x01\x1e"''')
    register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.1.1.0 = STRING: "Linux debian-dev 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt20-1+deb8u4 (2016-02-29) x86_64"''')

    the_time = struct.unpack('BBBBBBBBcBB', '\x07\xdf\x07\x01\x01\x1d\x2b\x01+\x01\x1e')

    the_year = (the_time[0] * 256) + the_time[1]

    print 'Year: %d' % the_year  # year
    print 'Month: %d' % the_time[2]  # month
    print 'Day: %d' % the_time[3]  # day
    print 'Hour: %d' % the_time[4]  # hours
    print 'Minute: %d' % the_time[5]  # minutes
    print 'Second: %d' % the_time[6]  # seconds
    print 'Offset-hour: %d' % the_time[9]  # offset-
    print 'Offset-minute: %d' % the_time[10]  # offset-

    p = subprocess.Popen(
        'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py -H localhost:1234',
        shell=True, stdout=subprocess.PIPE)
    cmd_output = p.stdout.read()
    print cmd_output
    assert 'Remote (UTC): 2015.06.30 23:59:43' in cmd_output


def test_stop():
    # stop the testagent
    stop_server()
