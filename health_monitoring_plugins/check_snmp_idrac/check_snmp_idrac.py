#!/usr/bin/env python

# Copyright (C) 2016 rsmuc <rsmuc@mailbox.org>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with check_snmp_idrac.py.  If not, see <http://www.gnu.org/licenses/>.

# Import PluginHelper and some utility constants from the Plugins module
from pynag.Plugins import PluginHelper,ok,critical
import netsnmp
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], os.pardir))
from snmpSessionBaseClass import add_common_options, get_common_options, verify_host, get_data, walk_data, state_summary, add_output

# Create an instance of PluginHelper()
helper = PluginHelper()

# Define the command line options
add_common_options(helper)
helper.parse_arguments()

# Get the options
host, version, community = get_common_options(helper)


# States definitions
normal_state = {
            1 : 'other',
            2 : 'unknown',
            3 : 'ok',
            4 : 'nonCritical',
            5 : 'critical',
            6 : 'nonRecoverable'
            }

system_power_state = {
            1 : 'other',
            2 : 'unknown',
            3 : 'off',
            4 : 'on'
            }

power_unit_redundancy_state = {
            1 : 'other',
            2 : 'unknown',
            3 : 'full',
            4 : 'degraded',
            5 : 'lost',
            6 : 'notRedundant',
            7 : 'redundancyOffline'
            }

probe_state = {
            1 : 'other',
            2 : 'unknown',
            3 : 'ok',
            4 : 'nonCriticalUpper',
            5 : 'criticalUpper',
            6 : 'nonRecoverableUpper',
            7 : 'nonCriticalLower',
            8 : 'criticalLower',
            9 : 'nonRecoverableLower',
            10 : 'failed'
            }


### from IDRAC-MIB-SMIv2
oid_user_assigned_name         = '.1.3.6.1.4.1.674.10892.5.4.300.10.1.7.1'
oid_product_type               = '.1.3.6.1.4.1.674.10892.5.4.300.10.1.9.1'
oid_service_tag                = '.1.3.6.1.4.1.674.10892.5.4.300.10.1.11.1'

# Global state OIDs
oid_global_system              = '.1.3.6.1.4.1.674.10892.5.2.1.0'
oid_system_lcd                 = '.1.3.6.1.4.1.674.10892.5.2.2.0'
oid_global_storage             = '.1.3.6.1.4.1.674.10892.5.2.3.0'
oid_system_power               = '.1.3.6.1.4.1.674.10892.5.2.4.0'


oid_power_unit_redundancy      = '.1.3.6.1.4.1.674.10892.5.4.600.10.1.5'
oid_power_unit_name            = '.1.3.6.1.4.1.674.10892.5.4.600.10.1.7'
oid_power_unit_status          = '.1.3.6.1.4.1.674.10892.5.4.600.10.1.8'

oid_chassis_intrusion          = '.1.3.6.1.4.1.674.10892.5.4.300.70.1.5'
oid_chassis_intrusion_location = '.1.3.6.1.4.1.674.10892.5.4.300.70.1.8'

oid_cooling_unit_name          = '.1.3.6.1.4.1.674.10892.5.4.700.10.1.7'
oid_cooling_unit_status        = '.1.3.6.1.4.1.674.10892.5.4.700.10.1.8'

oid_temperature_probe_status   = '.1.3.6.1.4.1.674.10892.5.4.700.20.1.5'
oid_temperature_probe_reading  = '.1.3.6.1.4.1.674.10892.5.4.700.20.1.6'
oid_temperature_probe_location = '.1.3.6.1.4.1.674.10892.5.4.700.20.1.8'

oid_voltage_probe_status       = '.1.3.6.1.4.1.674.10892.5.4.600.20.1.5'
oid_voltage_probe_reading      = '.1.3.6.1.4.1.674.10892.5.4.600.20.1.6'
oid_voltage_probe_location     = '.1.3.6.1.4.1.674.10892.5.4.600.20.1.8'


# check the power unit
def power_unit_check(power_unit_redundancy_data, power_unit_name_data, power_unit_status_data):
    power_unit_summary_output = ''
    power_unit_long_output = ''
    
    for x in range(len(power_unit_status_data)):
        if  normal_state[int(power_unit_status_data[x])] != 'ok' or power_unit_redundancy_state[int(power_unit_redundancy_data[x])] != 'full':
            # status is not OK or redundancy is not FULL
            helper.status(critical)
            power_unit_summary_output += 'Power unit "%s" status: %s. Redundancy: %s. ' % (power_unit_name_data[x], normal_state[int(power_unit_status_data[x])], power_unit_redundancy_state[int(power_unit_redundancy_data[x])])
        # we always want to show the information in the long output, independend from the status
        power_unit_long_output += 'Power unit "%s" status: %s. Redundancy: %s\n' % (power_unit_name_data[x], normal_state[int(power_unit_status_data[x])], power_unit_redundancy_state[int(power_unit_redundancy_data[x])])
    # erase the last '.' for a prettier summary output
    power_unit_summary_output = power_unit_summary_output[:-2]
    return power_unit_summary_output, power_unit_long_output

# check the chassis intrusion
def chassis_intrusion_check(chassis_intrusion_data, chassis_intrusion_location_data):
    chassis_intrusion_summary_output = ''
    chassis_intrusion_long_output = ''
    
    for x in range(len(chassis_intrusion_data)):
        if normal_state[int(chassis_intrusion_data[x])] != 'ok':
            # status is not OK
            helper.status(critical)
            chassis_intrusion_summary_output += 'Chassis intrusion sensor "%s" is %s. ' % (chassis_intrusion_location_data[x], normal_state[int(chassis_intrusion_data[x])])
        chassis_intrusion_long_output += 'Chassis intrusion sensor "%s" is %s\n' % (chassis_intrusion_location_data[x], normal_state[int(chassis_intrusion_data[x])])
    # erase the last '.' for a prettier summary output
    chassis_intrusion_summary_output = chassis_intrusion_summary_output[:-2]
    return chassis_intrusion_summary_output, chassis_intrusion_long_output

# check the cooling unit
def cooling_unit_check(cooling_unit_name_data, cooling_unit_status_data):
    cooling_unit_summary_output = ''
    cooling_unit_long_output = ''
    
    for x in range(len(cooling_unit_status_data)):
        if normal_state[int(cooling_unit_status_data[x])] != 'ok':
            # status is not OK
            helper.status(critical)
            cooling_unit_summary_output += 'Cooling unit "%s" status: %s. ' % (cooling_unit_name_data[x], normal_state[int(cooling_unit_status_data[x])])
        # we always want to show the information in the long output, independend from the status
        cooling_unit_long_output += 'Cooling unit "%s" status: %s\n' % (cooling_unit_name_data[x], normal_state[int(cooling_unit_status_data[x])])
    # erase the last '.' for a prettier summary output
    cooling_unit_summary_output = cooling_unit_summary_output[:-2]
    return cooling_unit_summary_output, cooling_unit_long_output

# check the temperature probes
def temperature_probe_check(temperature_probe_status_data, temperature_probe_status_tag, temperature_probe_reading_data, temperature_probe_reading_tag, temperature_probe_location_data):
    temperature_probe_summary_output = ''
    temperature_probe_long_output = ''
    
    for x in range(0, len(temperature_probe_reading_data)):
        temperature_probe_reading_data[x] = int(temperature_probe_reading_data[x])/10
        for y in range(0, len(temperature_probe_status_data)):
            # wheen the oids have the same ending, they belong together (they are organised in a table)
            if temperature_probe_reading_tag[x][39:] == temperature_probe_status_tag[y][39:]:
                temperature_probe_location_data[y] = temperature_probe_location_data[y].lower()
                helper.add_metric(label = '%s' % temperature_probe_location_data[y], value = temperature_probe_reading_data[x])
                if probe_state[int(temperature_probe_status_data[y])] != 'ok':
                    # status is not OK
                    helper.status(critical)
                    temperature_probe_summary_output += 'Temperature probe at "%s" is %s. ' % (temperature_probe_location_data[y], probe_state[int(temperature_probe_status_data[y])])
                # we always want to show the information in the long output, independend from the status
                temperature_probe_long_output += 'Status of temperature probe at "%s" is %s with %sC\n' % (temperature_probe_location_data[y], probe_state[int(temperature_probe_status_data[y])], temperature_probe_reading_data[x])
        # erase the last '.' for a prettier summary output
        temperature_probe_summary_output = temperature_probe_summary_output[:-2]
    return temperature_probe_summary_output, temperature_probe_long_output

# check the voltage probes
def voltage_probe_check(voltage_probe_status_data, voltage_probe_status_tag, voltage_probe_reading_data, voltage_probe_reading_tag , voltage_probe_location_data):
    voltage_probe_summary_output = ''
    voltage_probe_long_output = ''
    
    for x in range(0, len(voltage_probe_reading_data)):
        voltage_probe_reading_data[x] = int(voltage_probe_reading_data[x])/1000
        for y in range(0, len(voltage_probe_status_data)):
            # when the oids have the same ending, they belong together (they are organised in a table)
            if voltage_probe_reading_tag[x][39:] == voltage_probe_status_tag[y][39:]:
                # location name has to be lowercase, otherwise we would get a problem with add_metric
                voltage_probe_location_data[y] = voltage_probe_location_data[y].lower()
                helper.add_metric(label = '%s' % voltage_probe_location_data[y], value = voltage_probe_reading_data[x])
                if probe_state[int(voltage_probe_status_data[y])] != 'ok':
                    # status is not OK
                    helper.status(critical)
                    voltage_probe_summary_output += 'Voltage probe at "%s" is %s. ' % (voltage_probe_location_data[y], probe_state[int(voltage_probe_status_data[y])])
                # we always want to show the information in the long output, independend from the status
                voltage_probe_long_output += 'Status of voltage probe at "%s" is %s with %s V\n' % (voltage_probe_location_data[y], probe_state[int(voltage_probe_status_data[y])], voltage_probe_reading_data[x])
    #erase the last '.'for a prettier summary output
    voltage_probe_summary_output = voltage_probe_summary_output[:-2]
    return voltage_probe_summary_output, voltage_probe_long_output

if __name__ == '__main__':    
    # verify that a hostname is set
    verify_host(host, helper)
    
    # The default return value should be always OK
    helper.status(ok)
    
    sess = netsnmp.Session(Version=version, DestHost=host, Community=community)
    
    user_assigned_name_data = get_data(sess, oid_user_assigned_name, helper)
    product_type_data = get_data(sess, oid_product_type, helper)
    service_tag_data = get_data(sess, oid_service_tag, helper)
    
    helper.add_summary('User assigned name: %s - Typ: %s - Service tag: %s' % (user_assigned_name_data, product_type_data, service_tag_data))
    
    
    global_system_data = get_data(sess, oid_global_system, helper)
    system_lcd_data = get_data(sess, oid_system_lcd, helper)
    global_storage_data = get_data(sess, oid_global_storage, helper)
    system_power_data = get_data(sess, oid_system_power, helper)
    
    global_system_summary, global_system_long = state_summary(global_system_data, 'Global System', normal_state, helper)
    system_lcd_summary, system_lcd_long = state_summary(system_lcd_data, 'System LCD', normal_state, helper)
    global_storage_summary, global_storage_long = state_summary(global_storage_data, 'Global Storage', normal_state, helper)
    system_power_summary, system_power_long = state_summary(system_power_data, 'System Power', system_power_state, helper, 'on')
    
    add_output(global_system_summary, global_system_long, helper)
    add_output(system_lcd_summary, system_lcd_long, helper)
    add_output(global_storage_summary, global_storage_long, helper)
    add_output(system_power_summary, system_power_long, helper)
    
    # power unit
    power_unit_redundancy_data = walk_data(sess, oid_power_unit_redundancy, helper)[0]
    power_unit_name_data = walk_data(sess, oid_power_unit_name, helper)[0]
    power_unit_status_data = walk_data(sess, oid_power_unit_status, helper)[0]
    
    power_unit_summary_output, power_unit_long_output = power_unit_check(power_unit_redundancy_data, power_unit_name_data, power_unit_status_data)
    
    add_output(power_unit_summary_output, power_unit_long_output, helper)
    
    # chassis
    chassis_intrusion_data = walk_data(sess, oid_chassis_intrusion, helper)[0]
    chassis_intrusion_location_data = walk_data(sess, oid_chassis_intrusion_location, helper)[0]
    
    chassis_intrusion_summary_output, chassis_intrusion_long_output = chassis_intrusion_check(chassis_intrusion_data, chassis_intrusion_location_data)
    
    add_output(chassis_intrusion_summary_output, chassis_intrusion_long_output, helper)
    
    # cooling unit
    cooling_unit_name_data = walk_data(sess, oid_cooling_unit_name, helper)[0]
    cooling_unit_status_data = walk_data(sess, oid_cooling_unit_status, helper)[0]
    
    cooling_unit_summary_output, cooling_unit_long_output = cooling_unit_check(cooling_unit_name_data, cooling_unit_status_data)
    
    add_output(cooling_unit_summary_output, cooling_unit_long_output, helper)
    
    # temperature probes
    temperature_probe_status_data, temperature_probe_status_tag = walk_data(sess, oid_temperature_probe_status, helper)
    temperature_probe_reading_data, temperature_probe_reading_tag = walk_data(sess, oid_temperature_probe_reading, helper)
    temperature_probe_location_data = walk_data(sess, oid_temperature_probe_location, helper)[0]
    
    temperature_probe_summary_output, temperature_probe_long_output = temperature_probe_check(temperature_probe_status_data, temperature_probe_status_tag, temperature_probe_reading_data, temperature_probe_reading_tag, temperature_probe_location_data)
    
    add_output(temperature_probe_summary_output, temperature_probe_long_output, helper)
    
    # voltage probes
    voltage_probe_summary_output = ''
    voltage_probe_long_output = ''
    
    voltage_probe_status_data, voltage_probe_status_tag = walk_data(sess, oid_voltage_probe_status, helper)
    voltage_probe_reading_data, voltage_probe_reading_tag = walk_data(sess, oid_voltage_probe_reading, helper)
    voltage_probe_location_data, voltage_probe_location_tag = walk_data(sess, oid_voltage_probe_location, helper)
    
    voltage_probe_summary_output, voltage_probe_long_output = voltage_probe_check(voltage_probe_status_data, voltage_probe_status_tag, voltage_probe_reading_data, voltage_probe_reading_tag, voltage_probe_location_data)
    
    add_output(voltage_probe_summary_output, voltage_probe_long_output, helper)
    
    
    helper.check_all_metrics()
    # Print out plugin information and exit nagios-style
    helper.exit()
