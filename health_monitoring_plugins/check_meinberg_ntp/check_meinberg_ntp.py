#!/usr/bin/env python
# check_meinberg_ntp.py - Monitor the Meinberg NTP Server M300.

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
# along with check_meinberg_ntp.py.  If not, see <http://www.gnu.org/licenses/>.

# Import PluginHelper and some utility constants from the Plugins module
import sys
import os
import netsnmp
sys.path.insert(1, os.path.join(sys.path[0], os.pardir))
from snmpSessionBaseClass import add_common_options, get_common_options, verify_host, get_data
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown


# Create an instance of PluginHelper()
helper = PluginHelper()

# add the common command line options
add_common_options(helper)
# define the specific command line options
helper.parser.add_option('-m', help="Version of the Firmware (v5 or NG) (NG = MBG-LANTIME-NG-MIB.mib used in Firmware 6 and newer)", dest="mib")
helper.parse_arguments()

# get the options
mib = helper.options.mib
host, version, community = get_common_options(helper)

# use the correct oids depending on the version of the firmware / MIB
if mib == "NG":
    # OIDs from MBG-LANTIME-NG-MIB.mib    
    oid_ntp_current_state_int = ".1.3.6.1.4.1.5597.30.0.2.1.0"
    oid_gps_position = ".1.3.6.1.4.1.5597.30.0.1.5.0"    
    oid_gps_satellites_good = ".1.3.6.1.4.1.5597.30.0.1.2.1.6.1"
    oid_gps_mode_int = ".1.3.6.1.4.1.5597.30.0.1.2.1.5.1"

    ntp_status = {
        "0" : "notAvailable",
        "1" : "notSynchronized",
        "2" : "synchronized"
        }

    gps_mode = {
        "-1" : "mrsRefNone",
        "0" : "notAvailable",
        "1" : "gpsSync",
        "2" : "gpsTracking",
        "3" : "gpsAntennaDisconnected",
        "4" : "gpsWarmBoot",
        "5" : "gpsColdBoot",
        "6" : "gpsAntennaShortCircuit",
        "50" : "lwNeverSync",
        "51" : "lwNotSync",
        "52" : "lwSync",
        "100" : "tcrNotSync",
        "101" : "tcrSync",
        "150" : "mrsGpsSync",
        "151" : "mrs10MhzSync",
        "152" : "mrsPpsInSync",
        "153" : "mrs10MhzPpsInSync",
        "154" : "mrsIrigSync",
        "155" : "mrsNtpSync",
        "156" : "mrsPtpIeee1588Sync",
        "157" : "mrsPtpOverE1Sync",
        "158" : "mrsFixedFreqInSync",
        "159" : "mrsPpsStringSync",
        "160" : "mrsVarFreqGpioSync",
        "161" : "mrsReserved",
        "162" : "mrsDcf77PzfSync",
        "163" : "mrsLongwaveSync",
        "164" : "mrsGlonassGpsSync",
        "165" : "mrsHavequickSync",
        "166" : "mrsExtOscSync",
        "167" : "mrsIntOscSync"
        }

else:
    # OIDs from MBG-LANTIME-MIB.mib
    oid_ntp_current_state_int = ".1.3.6.1.4.1.5597.3.1.2.0"
    oid_gps_position = ".1.3.6.1.4.1.5597.3.2.7.0"
    oid_gps_satellites_good = ".1.3.6.1.4.1.5597.3.2.9.0"
    oid_gps_mode_int = ".1.3.6.1.4.1.5597.3.2.16.0" 

    ntp_status = {
        "0" : "notSynchronized",
        "1" : "noGoodRefclock",
        "2" : "syncToExtRefclock",
        "3" : "syncToSerialRefclock",
        "4" : "normalOperationPPS",
        "5" : "normalOperationRefclock",
        "99" : "unkown"
        }

    gps_mode = {
        "0" : "notavailable",
        "1" : "normalOperation",
        "2" : "trackingSearching",
        "3" : "antennaFaulty",
        "4" : "warmBoot",
        "5" : "coldBoot",
        "6" : "antennaShortcircuit"
        }

def check_gps_position():
    """
    just print the curret GPS position
    """
    gps_position = get_data(sess, oid_gps_position, helper)
    helper.add_summary(gps_position)

def check_ntp_status():
    """
    check and show the current NTP status
    """
    ntp_status_int = get_data(sess, oid_ntp_current_state_int, helper)

    # convert the ntp_status integer value in a human readable value
    try:
        ntp_status_string = ntp_status[ntp_status_int]
    except KeyError:
        # if we receive an value, that is not in the dict
        helper.exit(summary="received an undefined value from device: " + ntp_status_int, exit_code=unknown, perfdata='')

    # the ntp status should be synchronized (new MIB) or normalOperation (old mib)
    if ntp_status_string != "synchronized" and ntp_status_string != "normalOperationPPS":    
        # that is a critical condition, because the time reference will not be reliable anymore
        helper.status(critical)
        helper.add_summary("NTP status: " + ntp_status_string)

def check_gps_status():
    """
    check and show the current GPS status
    """
    gps_status_int = get_data(sess, oid_gps_mode_int, helper)

    try:
        gps_mode_string = gps_mode[gps_status_int]
    except KeyError:
        # if we receive an value, that is not in the dict
        helper.exit(summary="received an undefined value from device: " + gps_status_int, exit_code=unknown, perfdata='')

    if gps_mode_string != "normalOperation" and gps_mode_string != "gpsSync" :
        # that is a warning condition, NTP could still work without the GPS antenna
        helper.status(warning)
        helper.add_summary("GPS status: " + gps_mode_string)

def check_satellites():
    """
    check and show the good satellites
    """
    # here we get the value for the satellites
    good_satellites = get_data(sess, oid_gps_satellites_good, helper)

    # Show the summary and add the metric and afterwards check the metric
    helper.add_summary("Good satellites: %s" % good_satellites)
    helper.add_metric(label='satellites',value=good_satellites) 

if __name__ == "__main__":

    # verify that a hostname is set
    verify_host(host, helper)

    # The default return value should be always OK
    helper.status(ok)

    sess = netsnmp.Session(Version=version, DestHost=host, Community=community)

    check_gps_position()
    check_ntp_status()
    check_gps_status()
    check_satellites()
    
    # there is only the satellites metric, but we will check all available
    helper.check_all_metrics()

    # Print out plugin information and exit nagios-style
    helper.exit()
