#!/usr/bin/env python
# check_meinberg_ntp.py - Monitor the Meinberg NTP Server M300.

# Copyright (C) 2016-2018 rsmuc <rsmuc@mailbox.org>
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

from pynag.Plugins import ok
import health_monitoring_plugins.meinberg

if __name__ == "__main__":
    HELPER = health_monitoring_plugins.SnmpHelper()
    HELPER.parser.add_option('-m',
                             help="Version of the Firmware (v5 or NG) "
                                  "(NG = MBG-LANTIME-NG-MIB.mib used in Firmware 6 and newer)",
                             dest="mibversion")
    HELPER.parse_arguments()
    SESS = health_monitoring_plugins.SnmpSession(**HELPER.get_snmp_args())

    # The default return value should be always OK
    HELPER.status(ok)

    MEINBERG = health_monitoring_plugins.meinberg.Meinberg(SESS, HELPER.options.mibversion)

    # GPSPosition

    SNMP_RESULT = HELPER.get_snmp_value(SESS, HELPER, MEINBERG.oids['oid_gps_position'])
    MEINBERG.check_gps_position(HELPER, SNMP_RESULT)

    # NTP Status
    SNMP_RESULT = HELPER.get_snmp_value(SESS, HELPER, MEINBERG.oids['oid_ntp_current_state_int'])
    MEINBERG.update_status(HELPER, MEINBERG.check_ntp_status(SNMP_RESULT))

    # GPS Status
    SNMP_RESULT = HELPER.get_snmp_value(SESS, HELPER, MEINBERG.oids['oid_gps_mode_int'])
    MEINBERG.update_status(HELPER, MEINBERG.check_gps_status(SNMP_RESULT))

    # Satellites
    SNMP_RESULT = HELPER.get_snmp_value(SESS, HELPER, MEINBERG.oids['oid_gps_satellites_good'])
    MEINBERG.check_satellites(HELPER, SNMP_RESULT)

    # there is only the satellites metric, but we will check all available
    HELPER.check_all_metrics()

    # Print out plugin information and exit nagios-style
    HELPER.exit()
