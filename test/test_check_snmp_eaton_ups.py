#!/usr/bin/env python
import context
import os
import sys

sys.path.insert(0, os.path.abspath('health_monitoring_plugins/check_snmp_eaton_ups'))

import netsnmp
import test_util
import testagent

eaton_ups_check_plugin_path = "health_monitoring_plugins/check_snmp_eaton_ups/check_snmp_eaton_ups.py"

# configuration of the testagent
os.environ['MIBDIRS'] = os.path.dirname(os.path.abspath(__file__))
testagent.configure(agent_address="localhost:1234",
                    rocommunity='public', rwcommunity='private')

# create netsnmp Sessions for test_get and test_walk
session = netsnmp.Session(Version=2, DestHost='localhost', Community='public')
failSession = netsnmp.Session(Version=2, DestHost='1.2.3.4', Community='public')

check_configs_range = {
    "input_frequency"
    : {"value": 50,
       "summary": "input frequency",
       "has_perfdata": True
       },
    "input_voltage"
    : {"value": 230,
       "summary": "input voltage",
       "has_perfdata": True
       },
    "output_voltage"
    : {"value": 229,
       "summary": "output voltage",
       "has_perfdata": True
       },
    "output_current"
    : {"value": 2,
       "summary": "output current",
       "has_perfdata": True
       },
    "output_power"
    : {"value": 536,
       "summary": "output power",
       "has_perfdata": True
       },
    "environment_temperature"
    : {"value": 26,
       "summary": "environment temperature",
       "has_perfdata": True
       },
    "external_environment_temperature"
    : {"value": 26,
       "summary": "external environment temperature",
       "has_perfdata": True
       },
}

check_configs_below_threshold = {
    "remaining_battery_time"
    : {"value": 30,
       "summary": "time remaining on battery",
       "has_perfdata": True
       },
    "battery_capacity"
    : {"value": 80,
       "summary": "remaining battery capacity",
       "has_perfdata": True
       }
}

check_configs_above_threshold = {
    "on_battery"
    : {"value": 60,
       "summary": "time running on battery",
       "has_perfdata": True
       },
    "output_load"
    : {"value": 19,
       "summary": "output load",
       "has_perfdata": True
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
    testagent.register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.33.1.3.3.1.2.1 = INTEGER: 500
        iso.3.6.1.2.1.33.1.3.3.1.2.2 = INTEGER: 500
        iso.3.6.1.2.1.33.1.3.3.1.2.3 = INTEGER: 500''')
    # upsInputVoltage
    testagent.register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.33.1.3.3.1.3.1 = INTEGER: 230
        iso.3.6.1.2.1.33.1.3.3.1.3.2 = INTEGER: 230
        iso.3.6.1.2.1.33.1.3.3.1.3.3 = INTEGER: 230
        iso.3.6.1.2.1.33.1.3.3.1.3.4 = INTEGER: 400
        iso.3.6.1.2.1.33.1.3.3.1.3.5 = INTEGER: 400
        iso.3.6.1.2.1.33.1.3.3.1.3.6 = INTEGER: 400       
        ''')
    # upsOutputVoltage
    testagent.register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.33.1.4.4.1.2.1 = INTEGER: 229
        iso.3.6.1.2.1.33.1.4.4.1.2.2 = INTEGER: 229
        iso.3.6.1.2.1.33.1.4.4.1.2.3 = INTEGER: 229
        iso.3.6.1.2.1.33.1.4.4.1.2.4 = INTEGER: 229
        iso.3.6.1.2.1.33.1.4.4.1.2.5 = INTEGER: 229
        iso.3.6.1.2.1.33.1.4.4.1.2.6 = INTEGER: 229
        ''')
    # upsOutputCurrent
    testagent.register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.33.1.4.4.1.3.1 = INTEGER: 20
        iso.3.6.1.2.1.33.1.4.4.1.3.2 = INTEGER: 20
        iso.3.6.1.2.1.33.1.4.4.1.3.3 = INTEGER: 20''')
    # upsOutputPower
    testagent.register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.33.1.4.4.1.4.1 = INTEGER: 536
        iso.3.6.1.2.1.33.1.4.4.1.4.2 = INTEGER: 536
        iso.3.6.1.2.1.33.1.4.4.1.4.3 = INTEGER: 536''')
    # upsOutputPercentLoad
    testagent.register_snmpwalk_ouput(
        '''iso.3.6.1.2.1.33.1.4.4.1.5.1 = INTEGER: 19
        iso.3.6.1.2.1.33.1.4.4.1.5.2 = INTEGER: 19
        iso.3.6.1.2.1.33.1.4.4.1.5.3 = INTEGER: 19''')
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
        , "active alarms = 0")

    testagent.unregister_all()
    testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.6.1.0 = INTEGER: 1''')
    test_util.check_value_without_thresholds(
        eaton_ups_check_plugin_path
        , a_check_type
        , "Critical"
        , "active alarms = 1")


#
# def test_battery_test_summary(capsys):
#     a_check_type = "BATTERY_TEST_SUMMARY"
#
#     testagent.unregister_all()
#     # upsTestResultsSummary
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.3.0 = INTEGER: 1''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "OK"
#         , "pass")
#
#     testagent.unregister_all()
#     # upsTestResultsSummary
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.3.0 = INTEGER: 5''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "OK"
#         , "in progress")
#
#     testagent.unregister_all()
#     # upsTestResultsSummary
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.3.0 = INTEGER: 6''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "OK"
#         , "no test initiated")
#
#     testagent.unregister_all()
#     # upsTestResultsSummary
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.3.0 = INTEGER: 2''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "Warning"
#         , "warning")
#
#     testagent.unregister_all()
#     # upsTestResultsSummary
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.3.0 = INTEGER: 4''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "Warning"
#         , "aborted")
#
#     testagent.unregister_all()
#     # upsTestResultsSummary
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.3.0 = INTEGER: 3''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "Critical"
#         , "error")
#
#     testagent.unregister_all()
#     # upsTestResultsSummary
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.3.0 = INTEGER: 7''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "Critical"
#         , "unknown SNMP value")


# def test_battery_test_detail(capsys):
#     a_check_type = "BATTERY_TEST_DETAIL"
#
#     testagent.unregister_all()
#     # upsTestResultsDetail
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.2.1.33.1.7.4.0 = STRING: "Testdetails"''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "OK"
#         , "Details of last UPS diagnostic test: Testdetails")
#
#
# #     "Battery Replacement Warning"
# #         : {"value" : ,
# #            "summary" : ""},
# def test_battery_replacement_warning(capsys):
#     a_check_type = "BATTERY_REPLACEMENT_WARNING"
#
#     testagent.unregister_all()
#     # upsmgBatteryReplacement
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.11.0 = INTEGER: 2''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "OK"
#         , "Battery does not need to be replaced")
#
#     testagent.unregister_all()
#     # upsmgBatteryReplacement
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.11.0 = INTEGER: 1''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "Critical"
#         , "Battery needs to be replaced")
#
#     testagent.unregister_all()
#     # upsmgBatteryReplacement
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.11.0 = INTEGER: 3''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "Critical"
#         , "Unknown battery replacement state")
#
#
# def test_battery_low_warning(capsys):
#     a_check_type = "BATTERY_LOW_WARNING"
#
#     testagent.unregister_all()
#     # upsmgBatteryLowBattery
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.14.0 = INTEGER: 2''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "OK"
#         , "Battery is not in low state")
#
#     testagent.unregister_all()
#     # upsmgBatteryLowBattery
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.14.0 = INTEGER: 1''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "Critical"
#         , "Battery is in low state")
#
#     testagent.unregister_all()
#     # upsmgBatteryLowBattery
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.14.0 = INTEGER: 3''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "Critical"
#         , "Unknown battery low state")
#
#
# def test_battery_fault_warning(capsys):
#     a_check_type = "BATTERY_FAULT_WARNING"
#
#     testagent.unregister_all()
#     # upsmgBatteryFaultBattery
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.9.0 = INTEGER: 2''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "OK"
#         , "Battery is not in fault state")
#
#     testagent.unregister_all()
#     # upsmgBatteryFaultBattery
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.9.0 = INTEGER: 1''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "Critical"
#         , "Battery is in fault state")
#
#     testagent.unregister_all()
#     # upsmgBatteryFaultBattery
#     testagent.register_snmpwalk_ouput('''iso.3.6.1.4.1.705.1.5.9.0 = INTEGER: 3''')
#     test_util.check_value_without_thresholds(
#         eaton_ups_check_plugin_path
#         , a_check_type
#         , "Critical"
#         , "Unknown battery state")


def test_stop():
    # stop the testagent
    testagent.unregister_all()
    testagent.stop_server()
