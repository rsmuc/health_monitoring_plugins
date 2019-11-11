"""
Module for check_snmp_large_storage
"""

#    Copyright (C) 2016-2019 rsmuc <rsmuc@sec-dev.de>

#    This file is part of "Health Monitoring Plugins".

#    "Health Monitoring Plugins" is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    "Health Monitoring Plugins" is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with "Health Monitoring Plugins".  If not, see <https://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function
from pynag.Plugins import unknown

# The OIDs we need from HOST-RESOURCES-MIB
OID_HR_STORAGE_INDEX = ".1.3.6.1.2.1.25.2.3.1.1"
OID_HR_STORAGE_DESCR = ".1.3.6.1.2.1.25.2.3.1.3"
OID_HR_STORAGE_ALLOCATION_UNITS = ".1.3.6.1.2.1.25.2.3.1.4"
OID_HR_STORAGE_USED = ".1.3.6.1.2.1.25.2.3.1.6"
OID_HR_STORAGE_SIZE = ".1.3.6.1.2.1.25.2.3.1.5"


def calculate_real_size(value):
    """
    check if we have a 32 bit counter overrun
    calculate the real_size; we check if the integer is positive
    """
    if value > 0:
        return value

    # if the integer is negative, the counter overran
    real_size = -value + 2147483647
    return real_size


def partition_found(partition, description):
    """
    returns True, if the partition (--partition) is in the description we received from the host

    if we want to have a linux partition (/),
    we use the full path (startswith "/" would result in / /var /dev etc).
    if we start with something else, we use the startswith function
    """

    if "/" in partition:
        use_fullcompare = True
    else:
        use_fullcompare = False

    if use_fullcompare and (partition == description):
        return True

    elif not use_fullcompare and description.startswith(partition):
        return True

    return False


class Storage(object):
    """Class for check_snmp_large_storage"""

    def __init__(self, session):
        self.sess = session

    @staticmethod
    def run_scan(helper, session):
        """
        show all available partitions
        """

        all_disks = helper.walk_snmp_values_or_exit(session, helper, OID_HR_STORAGE_DESCR, "Scan")

        print("All available disks at: " + helper.options.hostname)

        for disk in all_disks:
            print("Disk: \t'" + disk + "'")
        quit()

    @staticmethod
    def convert_to(helper, value, unit, targetunit):
        """
        convert the value to the target unit (MB, GB or TB) dependent
        on the hrStorageAllocationUnits
        value = the space
        unit = the storageAllocationUnit
        the target unit (MB, GB, TB)
        """
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
                helper.exit(summary="Wrong targetunit: %s" % targetunit, exit_code=unknown,
                            perfdata='')

        if result == 0.0:
            helper.exit(summary="Invalid data received", exit_code=unknown, perfdata='')

        return result

    def check_partition(self, helper, session):
        """
        check the defined partition
        """

        all_index = helper.walk_snmp_values_or_exit(session, helper,
                                                    OID_HR_STORAGE_INDEX, "Index")
        all_descriptions = helper.walk_snmp_values_or_exit(session, helper,
                                                           OID_HR_STORAGE_DESCR, "Desc")
        # we need the success flag for the error handling (partition found or not found)
        success = False

        # here we zip all index and descriptions to have a list like
        # [('Physical memory', '1'), ('Virtual memory', '3'), ('/', '32'), ('/proc/xen', '33')]
        zipped = zip(all_index, all_descriptions)

        for partition in zipped:
            index = partition[0]
            description = partition[1]

            if partition_found(helper.options.partition, description):
                # we found the partition
                success = True

                # receive all values we need
                unit = float(helper.get_snmp_value_or_exit(session, helper,
                                                           OID_HR_STORAGE_ALLOCATION_UNITS +
                                                           "." + index))
                size = float(helper.get_snmp_value_or_exit(session, helper,
                                                           OID_HR_STORAGE_SIZE +
                                                           "." + index))
                used = float(helper.get_snmp_value_or_exit(session, helper,
                                                           OID_HR_STORAGE_USED +
                                                           "." + index))

                if size == 0 or used == 0:
                    # if the host return "0" as used or size, the plugin must exit
                    # otherwise there will be a problem with the calculation (devision by zero)
                    helper.exit(
                        summary="Received value 0 as StorageSize or StorageUsed: calculation error",
                        exit_code=unknown, perfdata='')
                    break

                # calculate the real size (size*unit) and convert the results
                # to the target unit the user wants to see
                used_result = self.convert_to(helper, calculate_real_size(used),
                                              unit, helper.options.targetunit)

                size_result = self.convert_to(helper, calculate_real_size(size),
                                              unit, helper.options.targetunit)

                # calculation of the used percentage
                percent_used = used_result / size_result * 100

                # we need a string and want only two decimals
                used_string = str(float("{0:.2f}".format(used_result)))
                size_string = str(float("{0:.2f}".format(size_result)))
                percent_string = str(float("{0:.2f}".format(percent_used)))

                if percent_used < 0 or percent_used > 100:
                    # just a validation that percent_used is not smaller then 0% or lager then 100%
                    helper.exit(summary="Calculation error - second counter overrun?",
                                exit_code=unknown, perfdata='')
                    break

                # show the summary
                helper.add_summary("%s%% used (%s%s of %s%s) at '%s'" %
                                   (percent_string,
                                    used_string,
                                    helper.options.targetunit,
                                    size_string,
                                    helper.options.targetunit,
                                    description))

                # add the metric in percent.
                helper.add_metric(label='percent used', value=percent_string, min="0", max="100",
                                  uom="%")

        else:
            if not success:
                # if the partition was not found in the data output, we return an error
                helper.exit(summary="Partition '%s' not found" %
                            helper.options.partition, exit_code=unknown, perfdata='')
