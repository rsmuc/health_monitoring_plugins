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
# along with check_snmp_ilo.py.  If not, see <http://www.gnu.org/licenses/>.

# Import PluginHelper and some utility constants from the Plugins module
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown
import netsnmp

# Function for snmpget
def get_data(host, version, community, oid):
    try:
        var = netsnmp.Varbind(oid)
        data = netsnmp.snmpget(var, Version=version, DestHost=host, Community=community)
        value = data[0]
    except:
        helper.exit(summary="\n SNMP connection to device failed " + oid, exit_code=unknown, perdata='')
    if not value:
        helper.exit(summary="\n SNMP connection to device failed " + oid, exit_code=unknown, perfdata='')
    return value

# Function for snmpwalk
def walk_data(host, version, community, oid):
    var = netsnmp.Varbind(oid)
    try:
        data = netsnmp.snmpwalk(var, Version=version, DestHost=host, Community=community)
    except:
        helper.exit(summary="\n SNMP connection to device failed " + oid, exit_code=unknown, perfdata='')
    if not data:
        helper.exit(summary="\n SNMP connection to device failed " + oid, exit_code=unknown, perfdata='')
    return data

def state_summary(value, name, state_list, info = None):
    if not info:
        info = ''
    state_value = state_list[int(value)]
    if state_value != 'ok':
        helper.add_summary('%s status: %s %s' % (name, state_value, info))
        helper.status(critical)
    helper.add_long_output('%s status: %s %s' % (name, state_value, info))

def special_state_summary(value, name, state_list, ok_value):
    state_value = state_list[int(value)]
    if state_value != ok_value:
        helper.add_summary('%s status: %s' % (name, state_value))
        helper.status(critical)
    helper.add_long_output('%s status: %s' % (name, state_value))

# Function is only for commandline use. Does not return a health status
def scan_ilo():
    #physical_drive = walk_data(host, version, community, oid_phy_drv)
    ps = walk_data(host, version, community, oid_ps)
    fan = walk_data(host, version, community, oid_fan)
    # It could be that the server has 0 physical drives
    var = netsnmp.Varbind(oid_phy_drv_status)
    try:
        physical_drive = netsnmp.snmpwalk(var, Version=version, DestHost=host, Community=community)
        for x in range(len(physical_drive)):
            helper.add_long_output('Physical drive %d: %s'  % (x+1 , phy_drv_state[int(physical_drive[x])]))
    except:
        helper.add_long_output('No Physical drives detected')
    helper.add_long_output('')

    for x in range(len(ps)):
        helper.add_long_output('Power supply %d: %s'  % (x+1 , normal_state[int(ps[x])]))
    helper.add_long_output('')

    for x in range(len(fan)):
        helper.add_long_output('Fan %d: %s'  % (x+1 , normal_state[int(fan[x])]))

# Function for physical drives
def check_phy_drv():
    physical_drive_status = walk_data(host, version, community, oid_phy_drv_status)
    physical_drive_smart = walk_data(host, version, community, oid_phy_drv_smrt)
    physical_drive_temp = walk_data(host, version, community, oid_phy_drv_temp)
    physical_drive_temp_thres = walk_data(host, version, community, oid_phy_drv_temp_thres)
    phy_drv_count_ok = 0
            
    for x in range(len(physical_drive_status)):        
        if phy_drv_state[int(physical_drive_status[x])] == 'ok':
            # check how many drives in OK state we find
            phy_drv_count_ok += 1
        else:
            # status is not ok
            helper.status(critical)
            helper.add_summary('Physical drive status %d: %s' % (x+1, phy_drv_state[int(physical_drive_status[x])]))
        
        # we always want to show the drive status in the long output, independend from the status
        helper.add_long_output('Physical drive status %d: %s' % (x+1, phy_drv_state[int(physical_drive_status[x])]))
    
        # check of the harddrive temperatures
        if temp_drive_flag:
            # only evaluate the temperatures if temp_drive_flag is not set (--noDriveTemp). We need that for our 15k SAS drives.            
            if int(physical_drive_temp[x]) != -1:
                # OID returns 0 or -1 if the drive temperature (threshold) cannot be calculated or if the controller does not support reporting drive temperature threshold
                if int(physical_drive_temp_thres[x]) != -1:
                    if int(physical_drive_temp[x]) > int(physical_drive_temp_thres[x]):
                        helper.add_summary('Physical drive temperature %d above threshold (%s / %s)' % (x+1, physical_drive_temp[x], physical_drive_temp_thres[x]))
                        helper.status(critical)
                    helper.add_long_output('Physical drive temperature %d: %s Celsius (threshold: %s Celsius)' % (x+1, physical_drive_temp[x], physical_drive_temp_thres[x]))
                else:
                    helper.add_long_output('Physical drive temperature %d: %s Celsius (no threshold given)' % (x+1, physical_drive_temp[x]))
            
    # if the count of the found OK drives does not match the amount of configured drives (--drives parameter)
    if phy_drv_count_ok != input_phy_drv:
        helper.add_summary('%s physical drive(s) expected - %s physical drive(s) in ok state!' % (input_phy_drv, phy_drv_count_ok))
        helper.status(critical)
    
    
    helper.add_long_output('')

    # Check Logical drive
    logical_drive = walk_data(host, version, community, oid_log_drv)

    for x in range(len(logical_drive)):
        state_summary(logical_drive[x], 'Logical drive %d' % x, log_drv_state)
    helper.add_long_output('')

# Check power supply
def check_ps():
    ps = walk_data(host, version, community, oid_ps)
    ps_redundant = walk_data(host, version, community, oid_ps_redundant)
    count_ps = 0    

    
    for x in range(len(ps)):
        helper.add_long_output('Power supply %d: %s' % (x+1, normal_state[int(ps[x])]))
        if normal_state[int(ps[x])] == 'ok':
            # check how many drives in OK state we find
            count_ps += 1

    if int(count_ps) != int(input_pwr_sply):
        # if the count of the found OK power supplies does not match the amount of configured power supplies (--ps parameter)
        helper.add_summary('%s power supply/supplies expected - %s power supply/supplies detected - %s power supply/supplies ok!' % (input_pwr_sply, len(ps), count_ps))
        helper.status(critical)

        for x in range(len(ps)):
            if normal_state[int(ps[x])] != 'ok':
                helper.add_summary('Power supply %d: %s' % (x+1, normal_state[int(ps[x])]))
            if ps_redundant_state[int(ps_redundant[x])] != 'notRedundant':
                helper.add_summary('Power supply %d is %s' % (x+1, ps_redundant_state[int(ps_redundant[x])]))

    helper.add_long_output('')

# Check fan
def check_fan():
    fan = walk_data(host, version, community, oid_fan)
    fan_count = 0

    for x in range(len(fan)):
        helper.add_long_output('Fan %d: %s' % (x+1, normal_state[int(fan[x])]))
        if normal_state[int(fan[x])] == 'ok':
            # check how many fans in OK state we find
            fan_count += 1
        
    if int(fan_count) != int(input_fan):
        # if the count of the found OK fans does not match the amount of configured fans (--fan parameter)
        helper.add_summary('%s fan(s) expected - %s fan(s) slot(s) detected - %s fan(s) ok!' % (input_fan, len(fan), fan_count))
        helper.status(critical)
        
        for x in range(len(fan)):
            if normal_state[int(fan[x])] != 'ok':
                helper.add_summary('Fan %d: %s' % (x+1, normal_state[int(fan[x])]))
            
    helper.add_long_output('')

# Create an instance of PluginHelper()
helper = PluginHelper()

if __name__ == "__main__":

    # Define the command line options
    helper.parser.add_option('-H', dest='hostname', help='Hostname or ip address')
    helper.parser.add_option('-C', '--community', dest='community', help='SNMP community of the SNMP service on target host.', default='public')
    helper.parser.add_option('-V', '--snmpversion', dest='version', help='SNMP version. (1 or 2)', default=2, type='int')
    helper.parser.add_option('-c', '--drives', dest='amount_drvs', help='Amount of physical drives. Requires an integer. (0 to disable the check)', type='int')
    helper.parser.add_option('-p', '--ps', dest='amount_pwr_sply', help='Amount of connected power supplies. Requires an integer. (0 to disable the check)', type='int')
    helper.parser.add_option('-f', '--fan', dest='amount_fans', help='Amount of fans. Requires an integer. (0 to disable the check)', type='int')
    helper.parser.add_option('--scan', dest='scan_server', help='Scan the server for all available components', default=False, action='store_true')
    helper.parser.add_option('--noStorage', dest='no_storage', help='Do not check global storage condition', default=True, action='store_false')
    helper.parser.add_option('--noSystem', dest='no_system', help='Do not check global system state', default=True, action='store_false')
    helper.parser.add_option('--noPowerSupply', dest='no_power_supply', help='Do not check global power supply condition', default=True, action='store_false')
    helper.parser.add_option('--noPowerState', dest='no_power_state', help='Do not check power state', default=True, action='store_false')
    helper.parser.add_option('--noTemp', dest='no_temp', help='Do not check global temperature condition', default=True, action='store_false')
    helper.parser.add_option('--noTempSens', dest='no_temp_sens', help='Do not check temperature sensor condition', default=True, action='store_false')
    helper.parser.add_option('--noDriveTemp', dest='no_drive_sens', help='Do not check temperature sensor of the hard drives', default=True, action='store_false')
    helper.parser.add_option('--noFan', dest='no_fan', help='Do not check global fan condition', default=True, action='store_false')
    helper.parser.add_option('--noMemory', dest='no_mem', help='Do not check memory condition', default=True, action='store_false')
    helper.parser.add_option('--noController', dest='no_ctrl', help='Do not check controller condition', default=True, action='store_false')
    helper.parse_arguments()

    # Get the options
    host = helper.options.hostname
    version = helper.options.version
    community = helper.options.community
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


    # Verify that there required parameters are set
    if host == '' or host == None:
        helper.exit(summary='Hostname must be specified', exit_code=unknown, perfdata='')

    if input_phy_drv == '' or input_phy_drv == None:
        helper.exit(summary='Amount of physical drives must be specified. Use --scan to show all available components', exit_code=unknown, perfdata='')
    
    if input_pwr_sply == '' or input_pwr_sply == None:
        helper.exit(summary='Amount of power supplies must be specified. Use --scan to show all available components', exit_code=unknown, perfdata='')
    
    if input_fan == '' or input_fan == None:
        helper.exit(summary='Amount of fans must be specified. Use --scan to show all available components.', exit_code=unknown, perfdata='')


    # The default return value should be always OK
    helper.status(ok)


    ### All required SNMP OIDs

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


    # Show the product name (e.g. HP DL380 G9) and the Serial numver of the server
    product_name = walk_data(host, version, community, oid_product_name)
    serial_number = walk_data(host, version, community, oid_serial_numb)
    helper.add_summary('%s - Serial number:%s' % (product_name[0], serial_number[0]))


    # Show all components that we find via snmp walk. Should only be used for operations on the commandline. Will always return an unknown.
    if scan:
        scan_ilo()    
        helper.exit(exit_code=unknown, perfdata='')
   
    # Check the global states
    if storage_flag:
        global_storage = get_data(host, version, community, oid_storage)
        state_summary(global_storage, 'Global storage', normal_state)
        helper.add_long_output('')

    if system_flag:
        global_system = get_data(host, version, community, oid_system)
        state_summary(global_system, 'Global system', normal_state)
        helper.add_long_output('')

    if power_supply_flag:
        glob_power_supply = get_data(host, version, community, oid_glob_power_supply)
        state_summary(glob_power_supply, 'Global power supply', normal_state)
        helper.add_long_output('')

    if power_state_flag:
        power_state = get_data(host, version, community, oid_power_state)
        special_state_summary(power_state, 'Server power', server_power_state, server_power_state[3])
        helper.add_long_output('')

    if temp_flag:
        temp = get_data(host, version, community, oid_glob_temp)
        state_summary(temp, 'Overall thermal environment', normal_state)
        helper.add_long_output('')

    if temp_sens_flag:
        temp_sens = get_data(host, version, community, oid_glob_temp_sens)
        state_summary(temp_sens, 'Temperature sensors', normal_state)
        helper.add_long_output('')

    if fan_flag:
        glob_fan = get_data(host, version, community, oid_glob_fan)
        state_summary(glob_fan, 'Fan(s)', normal_state)
        helper.add_long_output('')

    if mem_flag:
        mem = get_data(host, version, community, oid_mem)
        state_summary(mem, 'Memory', normal_state)
        helper.add_long_output('')

    if ctrl_flag:
        ctrl = walk_data(host, version, community, oid_ctrl)
        for x in range(len(ctrl)):
            state_summary(ctrl[x], 'Controller %s' % x, normal_state)
        helper.add_long_output('')

    # Physical drive check
    if input_phy_drv != 0:
        check_phy_drv()


    # Power supply check
    if input_pwr_sply != 0:
        check_ps()

    # Environment temperature check
    env_temp = walk_data(host, version, community, oid_env_temp)
    env_temp_thres = walk_data(host, version, community, oid_env_temp_thres)

    for x in range(len(env_temp)):
        # OID returns -99 or 0 if environment temperature (threshold) cannot be determined by software
        if (int(env_temp[x]) != -99) and (int(env_temp[x]) != 0):
            if (int(env_temp_thres[x]) != -99) and (int(env_temp_thres[x]) != 0):
                if int(env_temp[x]) > int(env_temp_thres[x]):
                    helper.add_summary('Temperature at sensor %d above threshold (%s / %s)' % (x+1,env_temp[x], env_temp_thres[x]))
                    helper.status(critical)
                helper.add_long_output('Temperature %d: %s Celsius (threshold: %s Celsius)' % (x+1,env_temp[x], env_temp_thres[x]))
            else:
                helper.add_long_output('Temperature %d: %s Celsius (no threshold given)' % (x+1, env_temp[x]))
        else:
            helper.add_summary('Temperature %d could not be determined' % x+1)
            helper.status(critical)
    helper.add_long_output('')

    # Fan check
    if input_fan != 0:
        check_fan()
    
    # Print out plugin information and exit nagios-style
    helper.exit()
