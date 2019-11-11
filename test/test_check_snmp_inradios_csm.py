#!/usr/bin/python

# Copyright (C) 2018 haxtibal haxtibal@posteo.de

import pytest
import context
import subprocess
import testagent
import health_monitoring_plugins.inradios_csm

# Unit tests

def test_format_perfdata():
    inradios_health = health_monitoring_plugins.inradios_csm.InradiosCsmHealth(None, None)
    assert(inradios_health.format_perfdata(float(-10), float(10)) == "-10..10")
    assert(inradios_health.format_perfdata(float('nan'), float(10)) == "-inf..10")
    assert(inradios_health.format_perfdata(float('-10'), float('nan')) == "-10..inf")
    assert(inradios_health.format_perfdata(float('nan'), float('nan')) == None)
    assert(inradios_health.format_perfdata(float('-inf'), float('inf')) == None)
    assert(inradios_health.format_perfdata(float(-10.12345678), float(10.12345678)) == "-10.12346..10.12346")

def test_parse_data_ok_no_range():
    snmp_data = {
        'comment': str("Monitors the SNR by Spectrum Data of the Carrier"),
        'value': float(2.1),
        'uom': "dB",
        'valueDateTime': str("18.05.2018 08:47:29"),
        'parameter': str("Center-Frequency: 1.501 GHz; Bandwidth: 2.048 MHz; Attenuation: 3 dB;"),
        'status': int(2),
        'label': str("Test2")
    }
    inradios_health = health_monitoring_plugins.inradios_csm.InradiosCsmHealth(None, None)
    inradios_health.snmp_data = snmp_data
    assert(inradios_health.make_value_str() == "Test2 = 2.1 dB")
    assert(inradios_health.make_clock_str() == "last update: 08:47:29")
    assert(inradios_health.make_prm_info() == ['Center-Frequency: 1.501 GHz', 'Bandwidth: 2.048 MHz',
                                               'Attenuation: 3 dB', 'Last update: 18.05.2018 08:47:29'] )
    assert(inradios_health.make_metric() == {'label': 'Test2', 'value': float(2.1), 'uom': 'dB'})

def test_parse_data_crit_above_alarm():
    snmp_data = {
        'comment': str("Monitors the SNR by Spectrum Data of the Carrier"),
        'value': float(2.1),
        'uom': None,
        'valueDateTime': str("18.05.2018 08:47:29"),
        'parameter': str("Center-Frequency: 1.501 GHz; Bandwidth: 2.048 MHz; Attenuation: 3 dB;"),
        'status': int(4),
        'label': str("Test2"),
        'alarm_upper': float(2.0)
    }
    inradios_health = health_monitoring_plugins.inradios_csm.InradiosCsmHealth(None, None)
    inradios_health.snmp_data = snmp_data
    assert(inradios_health.make_value_str() == "Test2 = 2.1")
    assert(inradios_health.make_clock_str() == "last update: 08:47:29")
    assert(inradios_health.make_prm_info() == ['Center-Frequency: 1.501 GHz', 'Bandwidth: 2.048 MHz',
                                               'Attenuation: 3 dB', 'Last update: 18.05.2018 08:47:29'] )
    assert(inradios_health.make_metric() == {'label': 'Test2', 'value': float(2.1), 'crit': '-inf..2'})

# Integration tests

class csmTable(object):
    "Simulation of INRADIOS::csmMonitoringTable"

    def __init__(self):
        self.setup_oids()

    def setup_oids(self):
        self.csmTable = testagent.Table(
            oidstr = "INRADIOS::csmMonitoringTable",
            indexes = [
                testagent.Integer32()
            ],
            columns = [
                (1, testagent.DisplayString("")),
                (2, testagent.DisplayString("")),
                (3, testagent.DisplayString("")),
                (4, testagent.DisplayString("")),
                (5, testagent.Integer32(0)),
                (6, testagent.DisplayString("")),
                (7, testagent.DisplayString("")),
                (8, testagent.DisplayString("")),
                (9, testagent.DisplayString("")),
                (10, testagent.DisplayString("")),
                (11, testagent.DisplayString(""))
            ],
        )

    def add_row(self, row_idx, columns):
        csmTableRow1 = self.csmTable.addRow([testagent.Integer32(row_idx)])
        for colid in columns:
            csmTableRow1.setRowCell(colid, columns[colid]),

testagent.configure(agent_address = "localhost:1234",
                    rocommunity='public', rwcommunity='private')
simulation = None
simulation = csmTable()

def test_start_server():
    testagent.start_server()

def test_simple_ok():
    simulation.add_row(1, {
               1: testagent.DisplayString("Monitors the SNR by Spectrum Data of the Carrier"),
               2: testagent.DisplayString("2.1"),
               3: testagent.DisplayString("18.05.2018 08:47:29"),
               4: testagent.DisplayString("Center-Frequency: 1.501 GHz; Bandwidth: 2.048 MHz; Attenuation: 3 dB;"),
               5: testagent.Integer32(2),
               6: testagent.DisplayString("dB"),
               7: testagent.DisplayString("NaN"),
               8: testagent.DisplayString("NaN"),
               9: testagent.DisplayString("1.9"),
               10: testagent.DisplayString("1.5"),
               11: testagent.DisplayString("Test2")
            })
    expected = ("OK - Test2 = 2.1 dB (last update: 08:47:29) | 'Test2'=2.1dB;~:1.9;~:1.5;;\n"
                "Center-Frequency: 1.501 GHz\n"
                "Bandwidth: 2.048 MHz\n"
                "Attenuation: 3 dB\n"
                "Last update: 18.05.2018 08:47:29\n")
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_inradios_csm/check_snmp_inradios_csm.py -H localhost:1234 -V 2 -C public -i 1",
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=context.testenv)
    plugin_out = p.stdout.read()
    assert(plugin_out == expected) 

def test_simple_critical():
    simulation.add_row(2, {
               1: testagent.DisplayString("Monitors the SNR by Spectrum Data of the Carrier"),
               3: testagent.DisplayString("18.05.2018 08:47:29"),
               4: testagent.DisplayString("Center-Frequency: 1.501 GHz; Bandwidth: 2.048 MHz; Attenuation: 3 dB;"),
               5: testagent.Integer32(1),
               6: testagent.DisplayString("dB"),
               7: testagent.DisplayString("0.1"),
               8: testagent.DisplayString("0.3"),
               9: testagent.DisplayString("1.9"),
               10: testagent.DisplayString("1.5"),
               11: testagent.DisplayString("Test2")
            })
    expected = ("Not available - Test2 = n/a (last update: 08:47:29)\n"
                "Center-Frequency: 1.501 GHz\n"
                "Bandwidth: 2.048 MHz\n"
                "Attenuation: 3 dB\n"
                "Last update: 18.05.2018 08:47:29\n")
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_inradios_csm/check_snmp_inradios_csm.py -H localhost:1234 -V 2 -C public -i 2",
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=context.testenv)
    plugin_out = p.stdout.read()
    assert(plugin_out == expected) 

def test_oids_minimal():
    simulation.add_row(3, {
               5: testagent.Integer32(2),
               7: testagent.DisplayString("NaN"),
               8: testagent.DisplayString("NaN"),
               9: testagent.DisplayString("1.9"),
               10: testagent.DisplayString("1.5"),
            })
    expected = ("OK - Measurement ID 3 = n/a (last update: n/a)\n")
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_inradios_csm/check_snmp_inradios_csm.py -H localhost:1234 -V 2 -C public -i 3",
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=context.testenv)
    plugin_out = p.stdout.read()
    assert(plugin_out == expected) 

def test_stop_server():
    testagent.stop_server()

def test_snmp_agent_offline():
    expected = ("Unknown - SNMP response incomplete or invalid\n")
    p = subprocess.Popen("health_monitoring_plugins/check_snmp_inradios_csm/check_snmp_inradios_csm.py -H localhost:1234 -V 2 -C public -i 1 --snmptimeout 100",
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=context.testenv)
    plugin_out = p.stdout.read()
    assert(plugin_out == expected)
