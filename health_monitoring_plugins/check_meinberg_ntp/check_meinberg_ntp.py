#!/usr/bin/python
# check_meinberg_ntp.py - Check Meinberg NTP Server. Thresholds can be specified from the commandline
# example command: ./check_meinberg_ntp.py -m fake -H demo.snmplabs.com -w 3..5 -c 0..3
# if no threshold is given, the default threshold will be used: warning=2..4, critical=0..2

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
# along with check_meinberg_ntp.py.  If not, see <http://www.gnu.org/licenses/>.

# Import PluginHelper and some utility constants from the Plugins module
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown
import sys
import netsnmp

# Create an instance of PluginHelper()
helper = PluginHelper()

def get_data(host, version, community, oid):
    # make an snmp get, if it fails exit the plugin
    try:
        var = netsnmp.Varbind(oid)
        data = netsnmp.snmpget(var, Version=version, DestHost=host, Community=community)
        value = data[0]
        if not value:
            helper.exit(summary="snmpget failed - no data for OID- maybe wrong MIB version selected or snmp is disabled at target device: " + host + " OID: " +oid, exit_code=unknown, perfdata='')
    except:
        helper.exit(summary="snmpget failed - exception", exit_code=unknown, perfdata='')
    return value

# Optionally, let helper handle command-line arguments for us for example --threshold
# Note: If your plugin needs any commandline arguments on its own (like --hostname) you should add them
# before this step with helper.parser.add_option()
if __name__ == "__main__":
    helper.parser.add_option('-H', help="Hostname or ip address", dest="hostname")
    helper.parser.add_option('-C', '--community', dest='community', help='SNMP community of the SNMP service on target host.', default='public')
    helper.parser.add_option('-V', '--snmpversion', dest='version', help='SNMP version. (1 or 2)', default=2, type='int')
    helper.parser.add_option('-m', help="Version of the MIB (NG = MBG-LANTIME-NG-MIB.mib)", dest="mib")

    helper.parse_arguments()

    # get the arguments
    mib = helper.options.mib
    host = helper.options.hostname
    version = helper.options.version
    community = helper.options.community

    # verify that a hostname is set
    if host == "" or host == None:
        helper.exit(summary="Hostname must be specified", exit_code=unknown, perfdata='')

    # use the correct oids depending on the version of the firmware / MIB
    if mib == "NG":
        # OIDs from MBG-LANTIME-NG-MIB.mib    
        ntp_current_state_int = ".1.3.6.1.4.1.5597.30.0.2.1.0"
        gps_position = ".1.3.6.1.4.1.5597.30.0.1.5.0"    
        gps_satellites_good = ".1.3.6.1.4.1.5597.30.0.1.2.1.6.1"
        gps_mode_int = ".1.3.6.1.4.1.5597.30.0.1.2.1.5.1"
    
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
            "150" : "mrsGpsSync",
            "151" : "mrs10MhzSync",
            "152" : "mrsPpsInSync",
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
        ntp_current_state_int = ".1.3.6.1.4.1.5597.3.1.2.0"
        gps_position = ".1.3.6.1.4.1.5597.3.2.7.0"
        gps_satellites_good = ".1.3.6.1.4.1.5597.3.2.9.0"
        gps_mode_int = ".1.3.6.1.4.1.5597.3.2.16.0" 
 
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
 
    # The default return value should be always OK
    helper.status(ok)

    #############
    # here we just want to print the current GPS position
    #############

    # clenaup: don't know if we really want to show the position in the summary or if we should move it to the long output

    gps_position = get_data(host, version, community, gps_position)
    helper.add_summary(gps_position)


    ############
    # here we check the ntp state for the new Meinbergs
    ############
    ntp_status_int = get_data(host, version, community, ntp_current_state_int)

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

    ##########
    # here we check the status of the GPS
    #########

    gps_status_int = get_data(host, version, community, gps_mode_int)

    try:
        gps_mode_string = gps_mode[gps_status_int]
    except KeyError:
        # if we receive an value, that is not in the dict
        helper.exit(summary="received an undefined value from device: " + gps_status_int, exit_code=unknown, perfdata='')

    if gps_mode_string != "normalOperation" and gps_mode_string != "gpsSync" :
        # that is a warning condition, NTP could still work without the GPS antenna
        helper.status(warning)
        helper.add_summary("GPS status: " + gps_mode_string)

    #############
    # check the amount of good satellites
    #############

    # here we get the value for the satellites
    good_satellites = get_data(host, version, community, gps_satellites_good)

    # Show the summary and add the metric and afterwards check the metric
    helper.add_summary("Good satellites: %s" % good_satellites)
    helper.add_metric(label='satellites',value=good_satellites) 

    helper.check_all_metrics()

    # Print out plugin information and exit nagios-style
    helper.exit()
