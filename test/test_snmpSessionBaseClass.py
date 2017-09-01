#!/usr/bin/python
import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins'))

import netsnmp
import pytest
import subprocess
import pynag

import snmpSessionBaseClass


# States definitions
normal_state = {
              1 : 'other',
              2 : 'ok',
              3 : 'degraded',
              4 : 'failed'
              }

# create an instance of PluginHelper()
helper = pynag.Plugins.PluginHelper()

# create netsnmp Session for test_get, test_attempt_get, test_walk and test_attempt_walk
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

def test_get(capsys):
    """
    test of the get_data function
    """
    # run a get on a not existing host
    with pytest.raises(SystemExit):
        snmpSessionBaseClass.get_data(failSession, '.1', helper)
    out, err = capsys.readouterr()
    assert 'Unknown - snmpget failed - no data for host' in out
    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert snmpSessionBaseClass.get_data(
        session, '.1.3.6.1.2.1.25.1.1.0', helper)[:-2]\
        == get_system_uptime()[:-2]

def test_attempt_data():
    """
    test of the attempt_get_data function
    """
    # try to get data from a not existing host
    assert snmpSessionBaseClass.attempt_get_data(failSession, '.1') == None
    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert snmpSessionBaseClass.attempt_get_data(
        session, '.1.3.6.1.2.1.25.1.1.0')[:-2] == get_system_uptime()[:-2]

def test_walk_data(capsys):
    """
    test of the walk_data function
    """
    #run a walk on a not existing host
    with pytest.raises(SystemExit):
        assert snmpSessionBaseClass.walk_data(failSession, '.1', helper)
    out, err = capsys.readouterr()
    assert 'Unknown - snmpwalk failed - no data for host' in out
    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert snmpSessionBaseClass.walk_data(
        session, '.1.3.6.1.2.1.25.1.1', helper)[0][0][:-3] == get_system_uptime()[:-3]

def test_attempt_walk_data():
    """
    test of the attempt_walk_data function
    """
    # try to get data from a not existing host
    assert not snmpSessionBaseClass.attempt_walk_data(failSession, '.1')[0]
    # check if we receive the system uptime via snmp and compare it with the local uptime from /proc/uptime (except the last digit)
    assert snmpSessionBaseClass.attempt_walk_data(
        session, '.1.3.6.1.2.1.25.1.1')[0][0][:-3] == get_system_uptime()[:-3]

def test_state_summary_ok():
    summary_output, long_output = snmpSessionBaseClass.state_summary(
        2, 'summary output', normal_state, helper)
    assert 'status: ok' in long_output
    assert not summary_output

def test_state_summary_failed():
    summary_output, long_output = snmpSessionBaseClass.state_summary(
        4, 'summary output', normal_state, helper)
    assert 'status: failed' in long_output
    assert 'status: failed' in summary_output