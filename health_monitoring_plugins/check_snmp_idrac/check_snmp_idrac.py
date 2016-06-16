#!/usr/bin/python

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
from pynag.Plugins import PluginHelper,ok,critical,unknown
import netsnmp
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], os.pardir))
from snmpSessionBaseClass import add_common_options, get_common_options, verify_host, get_data, walk_data

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

temperature_probe_state = {
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
oid_temperature_probe_location = '.1.3.6.1.4.1.674.10892.5.4.700.20.1.8'


def state_summary(value,name, state_list, info = None, ok_value = 'ok'):
    """
    Always add the status to the long output, and if the status is not ok (or ok_value), 
    we show it in the summary and set the status to critical
    """
    # translate the value (integer) we recieve to a human readable value (e.g. ok, critical etc.) with the given state_list
    state_value = state_list[int(value)]
    summary_output = ''
    long_output = ''
    if not info:
        info = ''
    if state_value != ok_value:
        summary_output += ('%s status: %s %s' % (name, state_value, info))
        helper.status(critical)
    long_output += ('%s status: %s %s\n' % (name, state_value, info))
    return summary_output, long_output


def add_output(summary_output, long_output):
    """
    if the summary output is empty, we don't add it as summary, otherwise we would have empty spaces (e.g.: '. . . . .') in our summary report
    """
    if summary_output != '':
        helper.add_summary(summary_output)
    helper.add_long_output(long_output)

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

# check the temperature probe
def temperature_probe_check(temperature_probe_status_data, temperature_probe_location_data):
    temperature_probe_summary_output = ''
    temperature_probe_long_output = ''
    
    for x in range(len(temperature_probe_status_data)):
        if temperature_probe_state[int(temperature_probe_status_data[x])] != 'ok':
            # status is not OK
            helper.status(critical)
            temperature_probe_summary_output += 'Temperature probe at "%s" is %s. ' % (temperature_probe_location_data[x], temperature_probe_state[int(temperature_probe_status_data[x])])
        # we always want to show the information in the long output, independend from the status
        temperature_probe_long_output += 'Temperature probe at "%s" is %s\n' % (temperature_probe_location_data[x], temperature_probe_state[int(temperature_probe_status_data[x])])
    # erase the last '.' for a prettier summary output
    temperature_probe_summary_output = temperature_probe_summary_output[:-2]
    return temperature_probe_summary_output, temperature_probe_long_output

if __name__ == '__main__':    
    # Create default parameter list for snmp classes
    parameter_list = [host, version, community, helper]
    
    # The default return value should be always OK
    helper.status(ok)

    # verify that a hostname is set
    verify_host(host, helper)
    
    user_assigned_name_data = get_data(host,version, community, oid_user_assigned_name, helper)
    product_type_data = get_data(host, version, community, oid_product_type, helper)
    service_tag_data = get_data(host, version, community, oid_service_tag, helper)
    
    helper.add_summary('User assigned name: %s - Typ: %s - Service tag: %s' % (user_assigned_name_data, product_type_data, service_tag_data))
    
    
    global_system_data = get_data(host, version, community, oid_global_system, helper)
    system_lcd_data = get_data(host, version, community, oid_system_lcd, helper)
    global_storage_data = get_data(host, version, community, oid_global_storage, helper)
    system_power_data = get_data(host, version, community, oid_system_power, helper)
    
    global_system_summary, global_system_long = state_summary(global_system_data, 'Global System', normal_state)
    system_lcd_summary, system_lcd_long = state_summary(system_lcd_data, 'System LCD', normal_state)
    global_storage_summary, global_storage_long = state_summary(global_storage_data, 'Global Storage', normal_state)
    system_power_summary, system_power_long = state_summary(system_power_data, 'System Power', system_power_state, None, 'on')
    
    add_output(global_system_summary, global_system_long)
    add_output(system_lcd_summary, system_lcd_long)
    add_output(global_storage_summary, global_storage_long)
    add_output(system_power_summary, system_power_long)
    
    # power unit
    power_unit_redundancy_data = walk_data(host, version, community, oid_power_unit_redundancy, helper)
    power_unit_name_data = walk_data(host, version, community, oid_power_unit_name, helper)
    power_unit_status_data = walk_data(host, version, community, oid_power_unit_status, helper)
    
    power_unit_summary_output, power_unit_long_output = power_unit_check(power_unit_redundancy_data, power_unit_name_data, power_unit_status_data)
    
    add_output(power_unit_summary_output, power_unit_long_output)
    
    # chassis
    chassis_intrusion_data = walk_data(host, version,community, oid_chassis_intrusion, helper)
    chassis_intrusion_location_data = walk_data(host, version, community, oid_chassis_intrusion_location, helper)
    
    chassis_intrusion_summary_output, chassis_intrusion_long_output = chassis_intrusion_check(chassis_intrusion_data, chassis_intrusion_location_data)
    
    add_output(chassis_intrusion_summary_output, chassis_intrusion_long_output)
    
    # cooling unit
    cooling_unit_name_data = walk_data(host, version, community, oid_cooling_unit_name, helper)
    cooling_unit_status_data = walk_data(host, version, community, oid_cooling_unit_status, helper)
    
    cooling_unit_summary_output, cooling_unit_long_output = cooling_unit_check(cooling_unit_name_data, cooling_unit_status_data)
    
    add_output(cooling_unit_summary_output, cooling_unit_long_output)
    
    # temperature probes
    temperature_probe_status_data = walk_data(host, version, community, oid_temperature_probe_status, helper)
    temperature_probe_location_data = walk_data(host, version, community, oid_temperature_probe_location, helper)
    
    temperature_probe_summary_output, temperature_probe_long_output = temperature_probe_check(temperature_probe_status_data, temperature_probe_location_data)
    
    add_output(temperature_probe_summary_output, temperature_probe_long_output)
    
    # Print out plugin information and exit nagios-style
    helper.exit()
