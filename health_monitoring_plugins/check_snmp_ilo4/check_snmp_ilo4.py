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
# along with check_snmp_ilo4.py.  If not, see <http://www.gnu.org/licenses/>.

# Import PluginHelper and some utility constants from the Plugins module
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown
import netsnmp
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], os.pardir))
from snmpSessionBaseClass import snmpSessionBaseClass, snmp_walk_data_class, snmp_get_data_class, snmp_try_walk_data_class, add_common_options, get_common_options, verify_host

# Create an instance of PluginHelper()
helper = PluginHelper()

# Define the command line options
add_common_options(helper)
helper.parser.add_option('--drives', help='Amount of physical drives', dest='amount_drvs')
helper.parser.add_option('--ps', help='Amount of connected power supplies', dest='amount_pwr_sply')
helper.parser.add_option('--fan', help='Amount of fans', dest='amount_fans')
helper.parser.add_option('--scan', help='Scan the server if you do not know what is build in (does not return a health status)', default=False, action='store_true', dest='scan_server')
helper.parser.add_option('--noStorage', help='Do not check global storage condition', default=True, action='store_false', dest='no_storage')
helper.parser.add_option('--noSystem', help='Do not check global system state', default=True, action='store_false', dest='no_system')
helper.parser.add_option('--noPowerSupply', help='Do not check global power supply condition', default=True, action='store_false', dest='no_power_supply')
helper.parser.add_option('--noPowerState', help='Do not check power state', default=True, action='store_false', dest='no_power_state')
helper.parser.add_option('--noTemp', help='Do not check Overall thermal environment condition', default=True, action='store_false', dest='no_temp')
helper.parser.add_option('--noTempSens', help='Do not check temperature sensor condition', default=True, action='store_false', dest='no_temp_sens')
helper.parser.add_option('--noDriveTemp', help='Do not check temperature sensor of the hard drives', default=True, action='store_false', dest='no_drive_sens')
helper.parser.add_option('--noFan', help='Do not check global fan condition', default=True, action='store_false', dest='no_fan')
helper.parser.add_option('--noMemory', help='Do not check memory condition', default=True, action='store_false', dest='no_mem')
helper.parser.add_option('--noController', help='Do not check controller condition', default=True, action='store_false', dest='no_ctrl')
helper.parser.add_option('--noPowerRedundancy', help='Do not check powersupply redundancy', default=True, action='store_false', dest='no_pwr_redund')
helper.parse_arguments()

# Get the options
host, version, community = get_common_options(helper)
input_phy_drv = helper.options.amount_drvs
input_pwr_sply = helper.options.amount_pwr_sply
input_fan = helper.options.amount_fans
scan = helper.options.scan_server
storage_flag = helper.options.no_storage
system_flag = helper.options.no_system
power_supply_flag = helper.options.no_power_supply
power_state_flag = helper.options.no_power_state
temp_flag = helper.options.no_temp
temp_sens_flag = helper.options.no_temp_sens
temp_drive_flag = helper.options.no_drive_sens
fan_flag = helper.options.no_fan
mem_flag = helper.options.no_mem
ctrl_flag = helper.options.no_ctrl
power_redundancy_flag = helper.options.no_pwr_redund

# States definitions
normal_state = {
              1 : 'other',
              2 : 'ok',
              3 : 'degraded',
              4 : 'failed'
              }

server_power_state = {
              1 : 'unknown',
              2 : 'poweredOff',
              3 : 'poweredOn',
              4 : 'insufficientPowerOrPowerOnDenied'
              }

log_drv_state = {
              1 : 'other',
              2 : 'ok',
              3 : 'failed',
              4 : 'unconfigured',
              5 : 'recovering',
              6 : 'readyForRebuild',
              7 : 'rebuilding',
              8 : 'wrongDrive',
              9 : 'badConnect',
              10: 'overheating',
              11: 'shutdown',
              12: 'expanding',
              13: 'notAvailable',
              14: 'queuedForExpansion',
              15: 'multipathAccessDegraded',
              16: 'erasing',
              17: 'predictiveSpareRebuildReady',
              18: 'rapidParityInitInProgress',
              19: 'rapidParityInitPending',
              20: 'noAccessEncryptedNoCntlrKey',
              21: 'unencryptedToEncryptedInProgress',
              22: 'newLogDrvKeyRekeyInProgress',
              23: 'noAccessEncryptedCntlrEncryptnNotEnbld',
              24: 'unencryptedToEncryptedNotStarted',
              25: 'newLogDrvKeyRekeyRequestReceived'
              }

phy_drv_state = {
              1 : 'other',
              2 : 'ok',
              3 : 'failed',
              4 : 'predictiveFailure',
              5 : 'erasing',
              6 : 'eraseDone',
              7 : 'eraseQueued',
              8 : 'ssdWearOut',
              9 : 'notAuthenticated'
              }

phy_drv_smrt_state = {
              1 : 'other',
              2 : 'ok',
              3 : 'replaceDrive',
              4 : 'replaceDriveSSDWearOut'
              }

ps_redundant_state = {
              1 : 'other',
              2 : 'notRedundant',
              3 : 'redundant'
              }

### from CPQIDA-MIB
oid_product_name = '.1.3.6.1.4.1.232.2.2.4.2'
oid_serial_numb = '.1.3.6.1.4.1.232.2.2.2.1'

# for global state
oid_storage = '.1.3.6.1.4.1.232.3.1.3.0'
oid_system = '.1.3.6.1.4.1.232.6.1.3.0'
oid_glob_power_supply = '.1.3.6.1.4.1.232.6.2.9.1.0'
oid_power_state = '.1.3.6.1.4.1.232.9.2.2.32.0'
oid_glob_temp = '.1.3.6.1.4.1.232.6.2.6.1.0'
oid_glob_temp_sens = '.1.3.6.1.4.1.232.6.2.6.3.0'
oid_glob_fan = '.1.3.6.1.4.1.232.6.2.6.4.0'
oid_mem = '.1.3.6.1.4.1.232.6.2.14.4.0'
oid_ctrl = '.1.3.6.1.4.1.232.3.2.2.1.1.6'

# for physical drive(s)
oid_phy_drv_status = '.1.3.6.1.4.1.232.3.2.5.1.1.6'
oid_phy_drv_smrt = '.1.3.6.1.4.1.232.3.2.5.1.1.57'
oid_phy_drv_temp = '.1.3.6.1.4.1.232.3.2.5.1.1.70'
oid_phy_drv_temp_thres = '.1.3.6.1.4.1.232.3.2.5.1.1.71'

# for logical drive(s)
oid_log_drv = '.1.3.6.1.4.1.232.3.2.3.1.1.4'

# for environment temperature
oid_env_temp = '.1.3.6.1.4.1.232.6.2.6.8.1.4'
oid_env_temp_thres = '.1.3.6.1.4.1.232.6.2.6.8.1.5'

# for fan(s)
oid_fan = '.1.3.6.1.4.1.232.6.2.6.7.1.9'

# for power supply
oid_ps = '.1.3.6.1.4.1.232.6.2.9.3.1.4'
oid_ps_redundant = '.1.3.6.1.4.1.232.6.2.9.3.1.9'


# scan function. terminates programm at the end
def scan_ilo():
    ps = snmp_walk_data_class(parameter_list, oid_ps)
    fan = snmp_walk_data_class(parameter_list, oid_fan)
    phy_drv_status = snmp_try_walk_data_class(parameter_list, oid_phy_drv_status, 'If the connection did not fail, then there were no physical drives detected!')

    data, err_msg = phy_drv_status.try_walk_data()
    if data:
        for x in range(phy_drv_status.get_len()):
            helper.add_long_output('Physical drive %d: %s' % (x, phy_drv_state[int(phy_drv_status.valueAt(x))]))
        helper.add_long_output('')
    else:
        helper.add_long_output(err_msg)
        helper.add_long_output('')

    for x in range(ps.get_len()):
        helper.add_long_output('Power supply %d: %s'  % (x, normal_state[int(ps.valueAt(x))]))
    helper.add_long_output('')

    for x in range(fan.get_len()):
        helper.add_long_output('Fan %d: %s'  % (x, normal_state[int(fan.valueAt(x))]))
    helper.add_summary('This is not a health status!')
    helper.exit(exit_code=unknown, perfdata='')


def check_global_status(flag, name, oid):
    """
    check a global status
    check_global_status(True, "Global Storage", '.1.3.6.1.4.1.232.3.1.3.0')
    """
    # only check the status, if the "no" flag is not set
    if flag:
        # get the data via snmp
        myData = snmp_get_data_class(parameter_list, oid)
        data_summary_output, data_long_output = state_summary(myData.get_data(), name, normal_state)
        add_output(data_summary_output, data_long_output)

# Function for summary
def state_summary(value, name, state_list, info = None):
    summary_output = ''
    long_output = ''
    if not info:
        info = ''
    state_value = state_list[int(value)]
    if state_value != 'ok':
        summary_output += ('%s status: %s %s ' % (name, state_value, info))
        helper.status(critical)
    long_output += ('%s status: %s %s\n' % (name, state_value, info))
    return (summary_output, long_output)


def special_state_summary(value, name, state_list, ok_value):
    state_value = state_list[int(value)]
    summary_output = ''
    long_output = ''
    if state_value != ok_value:
        summary_output += ('%s status: %s ' % (name, state_value))
        helper.status(critical)
    long_output += ('%s status: %s\n' % (name, state_value))
    return (summary_output, long_output)

# check if summary is empty, otherwise we would have empty spaces (e.g.: '. . . . .') in our summary report
def add_output(summary_output, long_output):
    if summary_output != '':
        helper.add_summary(summary_output)
    helper.add_long_output(long_output)

# physical drive check
def check_phy_drv(parameter_list, temp_drive_flag, input_phy_drv):
    physical_drive_status = snmp_walk_data_class(parameter_list, oid_phy_drv_status)
    physical_drive_smart = snmp_walk_data_class(parameter_list, oid_phy_drv_smrt)
    physical_drive_temp = snmp_walk_data_class(parameter_list, oid_phy_drv_temp)
    physical_drive_temp_thres = snmp_walk_data_class(parameter_list, oid_phy_drv_temp_thres)
    phy_drv_count_ok = 0
    summary_output = ''
    long_output = ''
    
    for x in range(physical_drive_status.get_len()):        
        if phy_drv_state[int(physical_drive_status.valueAt(x))] == 'ok' and phy_drv_smrt_state[int(physical_drive_smart.valueAt(x))] == 'ok':
            # check how many drives in OK state we find
            phy_drv_count_ok += 1
        else:
            # status is not ok
            helper.status(critical)
            summary_output += ('Physical drive %d status: %s ' % (x+1, phy_drv_state[int(physical_drive_status.valueAt(x))]))
            summary_output +=('Physical drive %d smart status: %s ' % (x+1, phy_drv_smrt_state[int(physical_drive_smart.valueAt(x))]))
        
        # we always want to show the drive status in the long output, independend from the status
        long_output += ('Physical drive %d status: %s\n' % (x+1, phy_drv_state[int(physical_drive_status.valueAt(x))]))
    
        # check of the harddrive temperatures
        if temp_drive_flag:
            # only evaluate the temperatures if temp_drive_flag is not set (--noDriveTemp). We need that for our 15k SAS drives.            
            if int(physical_drive_temp.valueAt(x)) != -1:
                # OID returns -1 if the drive temperature (threshold) cannot be calculated or if the controller does not support reporting drive temperature threshold
                if int(physical_drive_temp_thres.valueAt(x)) != -1:
                    if int(physical_drive_temp.valueAt(x)) > int(physical_drive_temp_thres.valueAt(x)):
                        summary_output += ('Physical drive %d temperature above threshold (%s / %s) ' % (x+1, physical_drive_temp.valueAt(x), physical_drive_temp_thres.valueAt(x)))
                        helper.status(critical)
                    long_output += ('Physical drive %d temperature: %s Celsius (threshold: %s Celsius)\n' % (x+1, physical_drive_temp.valueAt(x), physical_drive_temp_thres.valueAt(x)))
                else:
                    long_output += ('Physical drive %d temperature: %s Celsius (no threshold given)\n' % (x+1, physical_drive_temp.valueAt(x)))
            
    # if the count of the found OK drives does not match the amount of configured drives (--drives parameter)
    if int(phy_drv_count_ok) != int(input_phy_drv):
        summary_output += ('%s physical drive(s) expected - %s physical drive(s) in ok state! ' % (input_phy_drv, phy_drv_count_ok))
        helper.status(critical)
    
        # Check Logical drive
    logical_drive = snmp_walk_data_class(parameter_list, oid_log_drv)

    for x in range(logical_drive.get_len()):
        log_drv_summary_output, log_drv_long_output = state_summary(logical_drive.valueAt(x), 'Logical drive %d' % x, log_drv_state)
        summary_output += log_drv_summary_output
        long_output += log_drv_long_output
    return (summary_output, long_output)

# Check power supply
def check_ps(parameter_list, input_pwr_sply, check_redundant_flag):
    ps = snmp_walk_data_class(parameter_list, oid_ps)
    count_ps_ok = 0
    ps_redundant = snmp_walk_data_class(parameter_list, oid_ps_redundant)
    count_ps_redundant_ok = 0
    redundant_state_ok = ''
    summary_output = ''
    long_output = ''

    # If we should have 1 power supply running, its state should be 'notRedundant'
    if int(input_pwr_sply) == 1:
        redundant_state_ok = 'notRedundant'
    # If we should have more than 1, its state should be 'redundant'
    else:
        redundant_state_ok = 'redundant'

    for x in range(ps.get_len()):
        if normal_state[int(ps.valueAt(x))] == 'ok':
            count_ps_ok += 1
        if ps_redundant_state[int(ps_redundant.valueAt(x))] == redundant_state_ok:
            count_ps_redundant_ok += 1
            
    # Here we check, if as many power supply in 'ok'-state as given from the input and if their redundant_state is ok
    if (int(count_ps_ok) != int(input_pwr_sply)) or (int(count_ps_redundant_ok) < int(input_pwr_sply)):
        summary_output += ('%s power supply/supplies expected - %s power supply/supplies detected - %s power supply/supplies ok ' % (input_pwr_sply, ps.get_len(), count_ps_ok))
        helper.status(critical)

        for x in range(ps.get_len()):
            if normal_state[int(ps.valueAt(x))] != 'ok':
                summary_output += ('Power supply %d: %s ' % (x, normal_state[int(ps.valueAt(x))]))
            long_output += 'Power supply %d: %s' % (x, normal_state[int(ps.valueAt(x))])
            if check_redundant_flag:
                if ps_redundant_state[int(ps_redundant.valueAt(x))] != redundant_state_ok:
                    summary_output += ('Power supply %d is %s' % (x, ps_redundant_state[int(ps_redundant.valueAt(x))]))
                long_output += ' is %s' % (ps_redundant_state[int(ps_redundant.valueAt(x))])
            long_output += '\n'
    
    else:
        for x in range(ps.get_len()):
            if check_redundant_flag:
                long_output += ('Power supply %d: %s is %s\n' % (x, normal_state[int(ps.valueAt(x))], ps_redundant_state[int(ps_redundant.valueAt(x))]))
            else:
                long_output += ('Power supply %d: %s' % (x, normal_state[int(ps.valueAt(x))]))
    return (summary_output, long_output)

# Check fan
def check_fan(parameter_list, input_fan):
    fan = snmp_walk_data_class(parameter_list, oid_fan)
    fan_count = 0
    summary_output = ''
    long_output = ''

    for x in range(fan.get_len()):
        if normal_state[int(fan.valueAt(x))] == 'ok':
            fan_count += 1

    if int(fan_count) != int(input_fan):
        summary_output += '%s fan(s) expected - %s fan(s) slot(s) detected - %s fan(s) ok. ' % (input_fan, fan.get_len(), fan_count)
        helper.status(critical)

        for x in range(fan.get_len()):
            if normal_state[int(fan.valueAt(x))] != 'ok':
                summary_output += 'Fan %d: %s. ' % (x, normal_state[int(fan.valueAt(x))])
            long_output += 'Fan %d: %s.\n' % (x, normal_state[int(fan.valueAt(x))])
    else:
        for x in range(fan.get_len()):
            if normal_state[int(fan.valueAt(x))] == 'ok':
                long_output += 'Fan %d: %s.\n' % (x, normal_state[int(fan.valueAt(x))])
    return (summary_output, long_output)

if __name__ == '__main__':    
    # Create default parameter list for snmp classes
    parameter_list = [host, version, community, helper]
    
    # The default return value should be always OK
    helper.status(ok)

    # verify that a hostname is set
    verify_host(host, helper)
    
    # If the --scan option is set, we show all components and end the script
    if scan:
        scan_ilo()
    
    # Show always the product name and the serial number in the summary
    product_name = snmp_walk_data_class(parameter_list, oid_product_name)
    serial_number = snmp_walk_data_class(parameter_list, oid_serial_numb)    
    helper.add_summary('%s - Serial number:%s' % (product_name.valueAt(0), serial_number.valueAt(0)))
    
    # Verify that there is an input for the amount of components
    if input_phy_drv == '' or input_phy_drv is None:
        helper.exit(summary="Amount of physical drives must be specified (--drives)", exit_code=unknown, perfdata='')
    if input_pwr_sply == '' or input_pwr_sply is None:
        helper.exit(summary="Amount of power supplies must be specified (--ps)", exit_code=unknown, perfdata='')
    if input_fan == '' or input_fan is None:
        helper.exit(summary="Amount of fans must be specified (--fan)", exit_code=unknown, perfdata='')

    # Check the global status
    check_global_status(storage_flag, 'Global storage', oid_storage)
    check_global_status(system_flag,'Global system',oid_system)
    check_global_status(power_supply_flag,'Global power supply',oid_glob_power_supply)
    check_global_status(temp_flag,'Overall thermal environment',oid_glob_temp)
    check_global_status(temp_sens_flag,'Temperature sensors',oid_glob_temp_sens)
    check_global_status(fan_flag,'Fan(s)',oid_glob_fan)
    check_global_status(mem_flag,'Memory',oid_mem)
    
    if power_state_flag:
        power_state = snmp_get_data_class(parameter_list, oid_power_state)
        power_state_summary_output, power_state_long_output = special_state_summary(power_state.get_data(), 'Server power', server_power_state, server_power_state[3])
        add_output(power_state_summary_output, power_state_long_output)
    
    if ctrl_flag:
        ctrl = snmp_walk_data_class(parameter_list, oid_ctrl)
        for x in range(ctrl.get_len()):
            ctrl_summary_output, ctrl_long_output = state_summary(ctrl.valueAt(x), 'Controller %d' % x, normal_state)
            add_output(ctrl_summary_output, ctrl_long_output)
    
    # Physical drive check
    if int(input_phy_drv) != 0:
        phy_drv_summary_output, phy_drv_long_output = check_phy_drv(parameter_list,temp_drive_flag, input_phy_drv)
        add_output(phy_drv_summary_output, phy_drv_long_output)
            
    # Power supply check
    if int(input_pwr_sply) != 0:
        ps_summary_output, ps_long_output = check_ps(parameter_list, input_pwr_sply, power_redundancy_flag)
        add_output(ps_summary_output, ps_long_output)
    
    # Fan check
    if int(input_fan) != 0:
        fan_summary_output, fan_long_output = check_fan(parameter_list, input_fan)
        add_output(fan_summary_output, fan_long_output)
    
    # Environment temperature check
    env_temp = snmp_walk_data_class(parameter_list, oid_env_temp)
    env_temp_thres = snmp_walk_data_class(parameter_list, oid_env_temp_thres)
    
    for x in range(env_temp.get_len()):
        # OID returns -99 or 0 if environment temperature (threshold) cannot be determined by software
        if (int(env_temp.valueAt(x)) != -99) and (int(env_temp.valueAt(x)) != 0):
            if (int(env_temp_thres.valueAt(x)) != -99) and (int(env_temp_thres.valueAt(x)) != 0):
                if int(env_temp.valueAt(x)) > int(env_temp_thres.valueAt(x)):
                    helper.add_summary('Temperature at sensor %d above threshold (%s / %s)' % (x,env_temp.valueAt(x), env_temp_thres.valueAt(x)))
                    helper.status(critical)
                helper.add_long_output('Temperature %d: %s Celsius (threshold: %s Celsius)' % (x,env_temp.valueAt(x), env_temp_thres.valueAt(x)))
            else:
                helper.add_long_output('Temperature %d: %s Celsius (no threshold given)' % (x, env_temp.valueAt(x)))
        else:
            helper.add_summary('Temperature %d could not be determined' % x)
            helper.status(critical)
    
    # Print out plugin information and exit nagios-style
    helper.exit()