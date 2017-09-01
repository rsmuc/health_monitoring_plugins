#!/usr/bin/env python
import string
import os
import sys
sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_eaton_ups'))
 
import pytest
import subprocess
import netsnmp

import test_util

import testagent 
import check_snmp_eaton_ups
import snmpSessionBaseClass

import pynag.Utils

sys.path.append(r'/home/dausch/eclipse_opt/cpp-neon/eclipse/plugins/org.python.pydev_5.6.0.201703221358/pysrc/')
# import pydevd
# pydevd.settrace('172.29.153.190') # replace IP with address of Eclipse host machine

eaton_ups_check_plugin_path = "health_monitoring_plugins/check_snmp_eaton_ups/check_snmp_eaton_ups.py"

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
testagent.configure(agent_address = "localhost:1234",
    rocommunity='public', rwcommunity='private')

# create netsnmp Sessions for test_get and test_walk
session = netsnmp.Session(Version=2, DestHost='localhost', Community='public')
failSession = netsnmp.Session(Version=2, DestHost='1.2.3.4', Community='public')

a_plugin_helper = check_snmp_eaton_ups.setup_plugin_helper()


check_configs_range = {
    "INPUT_FREQUENCY"
        : {"value" : 50,
           "summary" : "Input Frequency is",
           "has_perfdata" : True
           },
    "INPUT_VOLTAGE"
        : {"value" : 230,
           "summary" : "Input Voltage is",
           "has_perfdata" : True
           },
    "OUTPUT_VOLTAGE"
        : {"value" : 229,
           "summary" : "Output Voltage is",
           "has_perfdata" : True
           },
    "OUTPUT_CURRENT"
        : {"value" : 2,
           "summary" : "Output Current is ",
           "has_perfdata" : True
           },
    "OUTPUT_POWER"
        : {"value" : 536,
           "summary" : "Output Power is",
           "has_perfdata" : True
           },
    "ENVIRONMENT_TEMPERATURE"
        : { "value" : 26,
            "summary" : "Environment Temperature is ",
            "has_perfdata" : True
            },
    "EXTERNAL_ENVIRONMENT_TEMPERATURE"
        : { "value" : 26,
            "summary" : "External Environment Temperature is ",
            "has_perfdata" : True
            },
    }


check_configs_below_threshold = {
    "REMAINING_BATTERY_TIME"
        : {"value" : 30,
           "summary" : "Remaining runtime on battery is",
           "has_perfdata" : True
           },
    "BATTERY_CAPACITY"
        : { "value" : 80,
            "summary" : "Remaining Battery Capacity",
            "has_perfdata" : True
            }
    }

check_configs_above_threshold = {
    "ON_BATTERY"                      
        : {"value" : 60,
           "summary" : "seconds already running on battery",
           "has_perfdata" : True
           },
    "OUTPUT_LOAD"
        : {"value" : 19,
           "summary" : "Output Load is",
           "has_perfdata" : True
           }
    }


def test_start_eaton_agent():
    # start the testagent (Eaton walk)
    # Gauge32 are not working - So I replaced them by INTEGER
    # some of the values are not from a walk - I modified them to have the return values I need (critical etc.)
    #
    # TODO Open issues
    # - SNMP Walk does not contain data for OID iso.3.6.1.4.1.534.1.6.1.0
    # as there was no remote temperature sensor connected to the device.
    # Manually added oid and value 

    # upsSecondsOnBattery
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.2.2.0 = INTEGER: 60''')
    # upsEstimatedMinutesRemaining
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.2.3.0 = INTEGER: 30''')
    # upsInputFrequency
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.3.3.1.2.1 = INTEGER: 500''')
    # upsInputVoltage
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.3.3.1.3.1 = INTEGER: 230''')
    # upsOutputVoltage
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.4.4.1.2.1 = INTEGER: 229''')
    # upsOutputCurrent
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.4.4.1.3.1 = INTEGER: 20''')
    # upsOutputPower
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.4.4.1.4.1 = INTEGER: 536''')
    # upsOutputPercentLoad
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.4.4.1.5.1 = INTEGER: 19''')
    # upsAlarmsPresent
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.6.1.0 = INTEGER: 0''')
    # upsTestResultsSummary
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.3.0 = INTEGER: 1''')
    # upsTestResultsDetail
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.4.0 = STRING: ""''')
    # xupsBatCapacity
    testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.534.1.2.4.0 = INTEGER: 80''')
    # xupsEnvAmbientTemp
    testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.534.1.6.1.0 = INTEGER: 26''')
    # xupsEnvRemoteTemp
    testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.534.1.6.5.0 = INTEGER: 26''')
    # upsmgBatteryFaultBattery
    testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.9.0 = INTEGER: 2''')
    # upsmgBatteryReplacement
    testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.11.0 = INTEGER: 2''')
    # upsmgBatteryLowBattery
    testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.14.0 = INTEGER: 2''')
    
    testagent.start_server()


def test_checks_within_range(capsys):
    for a_check_type, a_expected_value in check_configs_range.items():
        test_util.check_within_range(
            eaton_ups_check_plugin_path
            , a_check_type
            , a_expected_value["value"]
            , a_expected_value["summary"])
        if a_expected_value["has_perfdata"]:
            test_util.check_performance_data(
                eaton_ups_check_plugin_path
                , a_check_type
                , a_expected_value["value"])
        
def test_checks_below_threshold(capsys):
    for a_check_type, a_expected_value in check_configs_below_threshold.items():
        test_util.check_below_threshold(
            eaton_ups_check_plugin_path
            , a_check_type
            , a_expected_value["value"]
            , a_expected_value["summary"])
        if a_expected_value["has_perfdata"]:
            test_util.check_performance_data(
                eaton_ups_check_plugin_path
                , a_check_type
                , a_expected_value["value"])

def test_checks_above_threshold(capsys):
    for a_check_type, a_expected_value in check_configs_above_threshold.items():
        test_util.check_above_threshold(
            eaton_ups_check_plugin_path
            , a_check_type
            , a_expected_value["value"]
            , a_expected_value["summary"])
        if a_expected_value["has_perfdata"]:
            test_util.check_performance_data(
                eaton_ups_check_plugin_path
                , a_check_type
                , a_expected_value["value"])



def test_alarms(capsys):
    a_check_type = "ALARMS"
    # upsAlarmsPresent
    testagent.unregister_all()
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.6.1.0 = INTEGER: 0''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "OK"
        , "0 active alarms")
    
    testagent.unregister_all()
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.6.1.0 = INTEGER: 1''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "Critical"
        , "1 active alarms")


def test_battery_test_summary(capsys):
    a_check_type = "BATTERY_TEST_SUMMARY"

    testagent.unregister_all()
    # upsTestResultsSummary
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.3.0 = INTEGER: 1''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "OK"
        , "pass")
   
    testagent.unregister_all()
    # upsTestResultsSummary
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.3.0 = INTEGER: 5''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "OK"
        , "in progress")

    testagent.unregister_all()
    # upsTestResultsSummary
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.3.0 = INTEGER: 6''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "OK"
        , "no test initiated")
    
    testagent.unregister_all()
    # upsTestResultsSummary
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.3.0 = INTEGER: 2''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "Warning"
        , "warning")
    
    testagent.unregister_all()
    # upsTestResultsSummary
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.3.0 = INTEGER: 4''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "Warning"
        , "aborted")

    testagent.unregister_all()
    # upsTestResultsSummary
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.3.0 = INTEGER: 3''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "Critical"
        , "error")

    testagent.unregister_all()
    # upsTestResultsSummary
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.3.0 = INTEGER: 7''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "Critical"
        , "unknown SNMP value")


def test_battery_test_detail(capsys):
    a_check_type = "BATTERY_TEST_DETAIL"

    testagent.unregister_all()
    # upsTestResultsDetail
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.4.0 = STRING: "Testdetails"''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "OK"
        , "Details of last UPS diagnostic test: Testdetails")


#     "Battery Replacement Warning"
#         : {"value" : ,
#            "summary" : ""},
def test_battery_replacement_warning(capsys):
    a_check_type = "BATTERY_REPLACEMENT_WARNING"

    testagent.unregister_all()
    # upsmgBatteryReplacement
    testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.11.0 = INTEGER: 2''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "OK"
        , "Battery does not need to be replaced")
   
    testagent.unregister_all()
    # upsmgBatteryReplacement
    testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.11.0 = INTEGER: 1''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "Critical"
        , "Battery needs to be replaced")

    testagent.unregister_all()
    # upsmgBatteryReplacement
    testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.11.0 = INTEGER: 3''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "Critical"
        , "Unknown battery replacement state")


def test_battery_low_warning(capsys):
    a_check_type = "BATTERY_LOW_WARNING"

    testagent.unregister_all()
    # upsmgBatteryLowBattery
    testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.14.0 = INTEGER: 2''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "OK"
        , "Battery is not in low state")
   
    testagent.unregister_all()
    # upsmgBatteryLowBattery
    testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.14.0 = INTEGER: 1''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "Critical"
        , "Battery is in low state")

    testagent.unregister_all()
    # upsmgBatteryLowBattery
    testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.14.0 = INTEGER: 3''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "Critical"
        , "Unknown battery low state")


def test_battery_fault_warning(capsys):
    a_check_type = "BATTERY_FAULT_WARNING"

    testagent.unregister_all()
    # upsmgBatteryFaultBattery
    testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.9.0 = INTEGER: 2''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "OK"
        , "Battery is not in fault state")
   
    testagent.unregister_all()
    # upsmgBatteryFaultBattery
    testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.9.0 = INTEGER: 1''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "Critical"
        , "Battery is in fault state")

    testagent.unregister_all()
    # upsmgBatteryFaultBattery
    testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.9.0 = INTEGER: 3''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "Critical"
        , "Unknown battery state")


def test_stop():
    # stop the testagent
    testagent.unregister_all()
    testagent.stop_server()

