#!/usr/bin/env python
# check_snmp_large_storage.py - Check the used / free disk space of a device via SNMP (using the HOST-RESOURCES-MIB hrStorageSize).
# example command ./check_snmp_large_storage.py -H 192.168.2.1 -d "C:\" -u TB 
# Copyright (C) 2016 rsmuc rsmuc@mailbox.org
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
# along with check_snmp_large_storage.py.  If not, see <http://www.gnu.org/licenses/>.

# Import PluginHelper and some utility constants from the Plugins module
import sys
import os
import netsnmp
sys.path.insert(1, os.path.join(sys.path[0], os.pardir)) 
from snmpSessionBaseClass import add_common_options, get_common_options, verify_host, get_data, walk_data
from pynag.Plugins import PluginHelper,ok,unknown

# Create an instance of PluginHelper()
helper = PluginHelper()

# Add command line parameters
add_common_options(helper)
helper.parser.add_option('-p', '--partition',
                         dest='partition',
                         help='The disk / partition you want to monitor',
                         type='str')
helper.parser.add_option('-u', '--unit', dest="targetunit", help="The unit you want to have (MB, GB, TB)", default="GB")
helper.parser.add_option('-s', '--scan',   dest  = 'scan_flag', default   = False,    action = "store_true", help      = 'Show all available storages')
helper.parse_arguments()

# get the options
disk = helper.options.partition
scan = helper.options.scan_flag
targetunit = helper.options.targetunit
host, version, community = get_common_options(helper)

# The OIDs we need from HOST-RESOURCES-MIB
oid_hrStorageIndex              = ".1.3.6.1.2.1.25.2.3.1.1"
oid_hrStorageDescr              = ".1.3.6.1.2.1.25.2.3.1.3"
oid_hrStorageAllocationUnits    = ".1.3.6.1.2.1.25.2.3.1.4"
oid_hrStorageUsed               = ".1.3.6.1.2.1.25.2.3.1.6"
oid_hrStorageSize               = ".1.3.6.1.2.1.25.2.3.1.5"

def calculate_real_size(value):
    # check if we have a 32 bit counter overrun
    # calculate the real_size; we check if the integer is positive
    if value > 0:
        return value
    else:
        # if the integer is negative, the counter overran        
        real_size = -value + 2147483647
        return real_size

def convert_to_XX(value, unit, targetunit):
    #convert the value to the target unit (MB, GB or TB) dependend on the hrStorageAllocationUnits
    # value = the space
    # unit = the storageAllocationUnit
    # the target unit (MB, GB, TB)
    if value < 0:
        helper.exit(summary="Something went completely wrong", exit_code=unknown, perfdata='')
    else:
        # we need a float
        value = float(value)
        unit = float(unit)
        if targetunit == "MB":
            result = value * unit / 1024 / 1024

        elif targetunit == "GB":
            result = value * unit / 1024 / 1024 / 1024

        elif targetunit == "TB":
            result = value * unit / 1024 / 1024 / 1024 / 1024

        else:
            helper.exit(summary="Wrong targetunit: %s" % targetunit, exit_code=unknown, perfdata='')
        
    if result == 0.0:
        helper.exit(summary="Invalid data received", exit_code=unknown, perfdata='')

    return result

def run_scan():
    """
    show all available partitions
    """
    all_disks = walk_data(sess, oid_hrStorageDescr, helper)[0]
        
    print "All available disks at: " + host
    for disk in all_disks:        
        print "Disk: \t'" + disk + "'"
    quit()

def partition_found(partition, description):
    """
    returns True, if the partition (--partition) is in the description we received from the host
    """
    # if we want to have a linux partition (/) we use the full path (startswith "/" would result in / /var /dev etc). 
    # if we start with something else, we use the startswith function
    if "/" in partition:
        use_fullcompare = True            
    else:
        use_fullcompare = False
        
    if use_fullcompare and (partition == description):
        return True
    elif not use_fullcompare and description.startswith(partition):
        return True
    else:
        return False
            
def check_partition():
    """
    check the defined partition
    """
    
    all_index           = walk_data(sess, oid_hrStorageIndex, helper)[0]
    all_descriptions    = walk_data(sess, oid_hrStorageDescr, helper)[0]
    # we need the sucess flag for the error handling (partition found or not found)
    sucess              = False

    # here we zip all index and descriptions to have a list like
    # [('Physical memory', '1'), ('Virtual memory', '3'), ('/', '32'), ('/proc/xen', '33')]
    zipped = zip(all_index, all_descriptions)
    
    for partition in zipped:
        index       = partition[0]
        description = partition[1]
        
        if partition_found(disk, description):
            # we found the partition
            sucess = True

            # receive all values we need
            unit    =   float(get_data(sess, oid_hrStorageAllocationUnits + "." + index, helper))
            size    =   float(get_data(sess, oid_hrStorageSize + "." + index, helper))
            used    =   float(get_data(sess, oid_hrStorageUsed + "." + index, helper))

            if size == 0 or used == 0:
                # if the host return "0" as used or size, then we have a problem with the calculation (devision by zero)
                helper.exit(summary="Received value 0 as StorageSize or StorageUsed: calculation error", exit_code=unknown, perfdata='')

            # calculate the real size (size*unit) and convert the results to the target unit the user wants to see
            used_result     = convert_to_XX(calculate_real_size(used), unit, targetunit)
            size_result     = convert_to_XX(calculate_real_size(size), unit, targetunit)
            
            # calculation of the used percentage
            percent_used    = used_result / size_result * 100
            
            # we need a string and want only two decimals
            used_string     = str(float("{0:.2f}".format(used_result)))
            size_string     = str(float("{0:.2f}".format(size_result)))
            percent_string  = str(float("{0:.2f}".format(percent_used)))
            
            if percent_used < 0 or percent_used > 100:
                # just a validation that percent_used is not smaller then 0% or lager then 100%                
                helper.exit(summary="Calculation error - second counter overrun?", exit_code=unknown, perfdata='')                   
            
            # show the summary
            helper.add_summary("%s%% used (%s%s of %s%s) at '%s'" % (percent_string, used_string, targetunit, size_string, targetunit, description))
            # add the metric in percent. 
            helper.add_metric(label='percent used',value=percent_string, min="0", max="100", uom="%")
                    
    else:
        if not sucess:
            # if the partition was not found in the data output, we return an error
            helper.exit(summary="Partition '%s' not found" % disk, exit_code=unknown, perfdata='')

# The default return value should be always OK
helper.status(ok)

if __name__ == "__main__":
    
    # verify that a hostname is set
    verify_host(host, helper)

    sess = netsnmp.Session(Version=version, DestHost=host, Community=community)

    # if no partition / disk is set, we will do a scan
    if disk == "" or disk is None:
        scan = True

    #########
    # here we show all available disks at the host
    #########
        
    if scan:
        run_scan()
    
    ########
    # the check for the defined partition
    ########
    else:
        check_partition()
            
    helper.check_all_metrics()
    
    # Print out plugin information and exit nagios-style
    helper.exit()
