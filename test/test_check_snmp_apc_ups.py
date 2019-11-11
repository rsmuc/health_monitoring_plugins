#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_apc_ups'))

import subprocess
import netsnmp

import testagent
import check_snmp_apc_ups
import snmpSessionBaseClass

import test_util

sys.path.append(r'/home/dausch/eclipse_opt/cpp-neon/eclipse/plugins/org.python.pydev_5.6.0.201703221358/pysrc/')
#import pydevd
#pydevd.settrace('172.29.153.190') # replace IP with address of Eclipse host machine

apc_ups_check_plugin_path = "health_monitoring_plugins/check_snmp_apc_ups/check_snmp_apc_ups.py"

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
testagent.configure(agent_address = "localhost:1234",
    rocommunity='public', rwcommunity='private')

# create netsnmp Sessions for test_get and test_walk
session = netsnmp.Session(Version=2, DestHost='localhost', Community='public')
failSession = netsnmp.Session(Version=2, DestHost='1.2.3.4', Community='public')

a_plugin_helper = check_snmp_apc_ups.setup_plugin_helper()

check_configs_range = {
#     "BASIC_BATTERY_STATUS" : {
#         "value" : 2,
#         "summary" : "blablabla",
#         "has_perfdata" : True
#         },
    "INTERNAL_TEMPERATURE" : {      
        "value" : 26,
        "summary" : "Current internal temperature is",
        "has_perfdata" : True
        },
#     "BATTERY_REPLACE_INDICATOR": {
#         "value" : 1,
#         "summary" : "Battery does not need to be replaced",
#         "has_perfdata" : True
#         },
    "INPUT_VOLTAGE" : {
        "value" : 113,
        "summary" : "Input Voltage is",
        "has_perfdata" : True
        },
    "INPUT_FREQUENCY" : {
        "value" : 49,
        "summary" : "Input Frequency is",
        "has_perfdata" : True
        },
    "OUTPUT_VOLTAGE" : {
        "value" : 230,
        "summary" : "Output voltage is",
        "has_perfdata" : True
        },
    "OUTPUT_LOAD" : {
        "value" : 18,
        "summary" : "Output load is",
        "has_perfdata" : True
        },
    "OUTPUT_CURRENT" : {
        "value" : 1,
        "summary" : "Output current is",
        "has_perfdata" : True
        },
    "OUTPUT_POWER" : {
        "value" : 123,
        "summary" : "Output total power",
        "has_perfdata" : True
        },
#     "LAST_TEST_RESULT" : {
#         "value" : 3,
#         "summary" : "",
#         "has_perfdata" : True
#         },
    "ENVIRONMENT_TEMPERATURE" : {
        "value" : 25,
        "summary" : "",
        "has_perfdata" : True
        }
    }


check_configs_below_threshold = {
    "RUNTIME_REMAINING" : {
        "value" : 20.0,
        "summary" : "",
        "has_perfdata" : True
        },
    "BATTERY_CAPACITY" : {
        "value" : 80,
        "summary" : "80 % remainig battery capacity",
        "has_perfdata" : True
        }
    }

check_configs_above_threshold = {
    "TIME_ON_BATTERY" : {
        "value" : 10.0,
        "summary" : "minutes already running on battery",
        "has_perfdata" : True
        }    
    }


def test_start_apc_agent():
    # start the testagent (APC walk)
    # TimeTicks does not work - Replaced TimeTicks value by INTEGER
    # some of the values are not from a walk - I modified them to have the return values I need (critical etc.)
    # For now left out external temperature sensor oids as no data in snmpwalk
    # apc_oid_environment_temperature     = apc_oid_base + ".1.1.10.2.3.2.1.4.1"
    # apc_oid_environment_temperature_unit= apc_oid_base + ".1.1.10.2.3.2.1.5"
    # TODO add this data

    walk =  '''
        1.3.6.1.4.1.318.1.1.1.2.1.1.0 = INTEGER: 2
        1.3.6.1.4.1.318.1.1.1.2.1.2.0 = INTEGER: 60000
        1.3.6.1.4.1.318.1.1.1.2.2.1.0 = INTEGER: 80
        1.3.6.1.4.1.318.1.1.1.2.2.2.0 = INTEGER: 26
        1.3.6.1.4.1.318.1.1.1.2.2.3.0 = INTEGER: 120000
        1.3.6.1.4.1.318.1.1.1.2.2.4.0 = INTEGER: 1
        1.3.6.1.4.1.318.1.1.1.3.2.1.0 = INTEGER: 113
        1.3.6.1.4.1.318.1.1.1.3.2.2.0 = INTEGER: 115
        1.3.6.1.4.1.318.1.1.1.3.2.3.0 = INTEGER: 113
        1.3.6.1.4.1.318.1.1.1.3.2.4.0 = INTEGER: 49
        1.3.6.1.4.1.318.1.1.1.4.2.1.0 = INTEGER: 230
        1.3.6.1.4.1.318.1.1.1.4.2.2.0 = INTEGER: 49
        1.3.6.1.4.1.318.1.1.1.4.2.3.0 = INTEGER: 18
        1.3.6.1.4.1.318.1.1.1.4.2.4.0 = INTEGER: 1
        1.3.6.1.4.1.318.1.1.1.4.2.6.0 = INTEGER: 3
        1.3.6.1.4.1.318.1.1.1.4.2.8.0 = INTEGER: 123
        1.3.6.1.4.1.318.1.1.1.7.2.3.0 = INTEGER: 3
        1.3.6.1.4.1.318.1.1.10.2.3.2.1.4.1.0 = INTEGER: 25
        1.3.6.1.4.1.318.1.1.10.2.3.2.1.5.0 = INTEGER: 1
        '''   
    testagent.register_snmpwalk_ouput(walk)
    testagent.start_server()

def test_calc_minutes_from_ticks(capsys):
    assert check_snmp_apc_ups.calc_minutes_from_ticks('6000') == 1.0


# integration test
def test_system_call_apc_ups(capsys):
    # without options
    p=subprocess.Popen(apc_ups_check_plugin_path, shell=True, stdout=subprocess.PIPE)
    assert "Unknown - Hostname must be specified" in p.stdout.read()
 
    # No check type specified
    p=subprocess.Popen(apc_ups_check_plugin_path + " -H 1.2.3.4"
                       , shell=True, stdout=subprocess.PIPE)
    assert "Unknown - Check type must be specified" in p.stdout.read()

    # Unreachable host defined -H 1.2.3.4
#    p=subprocess.Popen(apc_ups_check_plugin_path + " -H 1.2.3.4 -t TIME_ON_BATTERY"
#                       , shell=True, stdout=subprocess.PIPE)
#    assert "Unknown - snmpget failed - no data for host" in p.stdout.read()

 
    # with --help
    p=subprocess.Popen(apc_ups_check_plugin_path + " --help"
                       , shell=True, stdout=subprocess.PIPE)
    assert "Options:" in p.stdout.read()


def test_snmpv3(capsys):
    # not reachable

    p = subprocess.Popen(apc_ups_check_plugin_path + " -H 1.2.3.4 -V 3 -t TIME_ON_BATTERY "
                                                     "-U nothinguseful -L authNoPriv -a MD5 "
                                                     "-A nothinguseful -x DES -X nothinguseful --timeout 3",
                         shell=True, stdout=subprocess.PIPE)
    output = p.stdout.read()
    assert "Unknown - snmpget failed - no data for host 1.2.3.4" in output  or "Unknown - Plugin timeout exceeded after" in output



#TODO: fix the tests

# def test_checks_within_range(capsys):
# #    pydevd.settrace('172.29.153.190') # replace IP with address of Eclipse host machine
#     for a_check_type, a_expected_value in check_configs_range.items():
#         test_util.check_within_range(
#             apc_ups_check_plugin_path
#             , a_check_type
#             , a_expected_value["value"]
#             , a_expected_value["summary"])
#         if a_expected_value["has_perfdata"]:
#             test_util.check_performance_data(
#                 apc_ups_check_plugin_path
#                 , a_check_type
#                 , a_expected_value["value"])
#
# def test_checks_below_threshold(capsys):
#     for a_check_type, a_expected_value in check_configs_below_threshold.items():
#         test_util.check_below_threshold(
#             apc_ups_check_plugin_path
#             , a_check_type
#             , a_expected_value["value"]
#             , a_expected_value["summary"])
#         if a_expected_value["has_perfdata"]:
#             test_util.check_performance_data(
#                 apc_ups_check_plugin_path
#                 , a_check_type
#                 , a_expected_value["value"])
#
# def test_checks_above_threshold(capsys):
#     for a_check_type, a_expected_value in check_configs_above_threshold.items():
#         test_util.check_above_threshold(
#             apc_ups_check_plugin_path
#             , a_check_type
#             , a_expected_value["value"]
#             , a_expected_value["summary"])
#         if a_expected_value["has_perfdata"]:
#             test_util.check_performance_data(
#                 apc_ups_check_plugin_path
#                 , a_check_type
#                 , a_expected_value["value"])


def test_basic_battery_status(capsys):
    a_summary = "OK - UPS batteries state is batteryNormal" 
    p=subprocess.Popen(apc_ups_check_plugin_path + " -H localhost:1234 -t BASIC_BATTERY_STATUS"
                       , shell=True, stdout=subprocess.PIPE)
    assert(a_summary in p.stdout.read())

    
def test_battery_replace_indicator(capsys):
    p=subprocess.Popen(
        apc_ups_check_plugin_path + " -H localhost:1234 -t BATTERY_REPLACE_INDICATOR"
        , shell=True, stdout=subprocess.PIPE)
    assert "OK - Battery does not need to be replaced" in p.stdout.read()


def test_last_test_result(capsys):
    p=subprocess.Popen(
        apc_ups_check_plugin_path + " -H localhost:1234 -t LAST_TEST_RESULT"
        , shell=True, stdout=subprocess.PIPE)
    assert "Critical - Result of last UPS diagnostic test was invalid test" in p.stdout.read()


def test_stop():
    # stop the testagent
    testagent.stop_server()
