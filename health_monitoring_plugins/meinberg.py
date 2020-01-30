"""
Module for check_meinberg_ntp
"""
#    Copyright (C) 2018-2019 rsmuc <rsmuc@sec-dev.de>

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

from pynag.Plugins import unknown, warning, critical


class Meinberg(object):
    """Class for check_meinberg_ntp"""
    def __init__(self, session, mibversion):
        self.oids = self.get_oids(mibversion)
        self.ntp_status = self.get_ntp_status(mibversion)
        self.gps_mode = self.get_gps_mode(mibversion)

    @staticmethod
    def get_oids(mibversion):
        """use the correct oids depending on the version of the firmware / MIB"""
        if mibversion == "NG":
            # OIDs from MBG-LANTIME-NG-MIB.mib
            return {
                "oid_ntp_current_state_int": ".1.3.6.1.4.1.5597.30.0.2.1.0",
                "oid_gps_position": ".1.3.6.1.4.1.5597.30.0.1.5.0",
                "oid_gps_satellites_good": ".1.3.6.1.4.1.5597.30.0.1.2.1.6.1",
                "oid_gps_mode_int": ".1.3.6.1.4.1.5597.30.0.1.2.1.5.1"
            }

        # OIDs from MBG-LANTIME-MIB.mib
        return {
            "oid_ntp_current_state_int": ".1.3.6.1.4.1.5597.3.1.2.0",
            "oid_gps_position": ".1.3.6.1.4.1.5597.3.2.7.0",
            "oid_gps_satellites_good": ".1.3.6.1.4.1.5597.3.2.9.0",
            "oid_gps_mode_int": ".1.3.6.1.4.1.5597.3.2.16.0"
        }

    @staticmethod
    def get_ntp_status(mibversion):
        """return the correct ntp status depending on the firmware"""
        if mibversion == "NG":
            # from MBG-LANTIME-NG-MIB.mib
            return {
                "0": "notAvailable",
                "1": "notSynchronized",
                "2": "synchronized"
            }

        # from MBG-LANTIME-MIB.mib
        return {
            "0": "notSynchronized",
            "1": "noGoodRefclock",
            "2": "syncToExtRefclock",
            "3": "syncToSerialRefclock",
            "4": "normalOperationPPS",
            "5": "normalOperationRefclock",
            "99": "unknown"
            }

    @staticmethod
    def get_gps_mode(mibversion):
        """return the correct gps mode depending on the firmware"""
        if mibversion == "NG":
            # from MBG-LANTIME-NG-MIB.mib
            return {
                "-1": "mrsRefNone",
                "0": "notAvailable",
                "1": "gpsSync",
                "2": "gpsTracking",
                "3": "gpsAntennaDisconnected",
                "4": "gpsWarmBoot",
                "5": "gpsColdBoot",
                "6": "gpsAntennaShortCircuit",
                "50": "lwNeverSync",
                "51": "lwNotSync",
                "52": "lwSync",
                "100": "tcrNotSync",
                "101": "tcrSync",
                "150": "mrsGpsSync",
                "151": "mrs10MhzSync",
                "152": "mrsPpsInSync",
                "153": "mrs10MhzPpsInSync",
                "154": "mrsIrigSync",
                "155": "mrsNtpSync",
                "156": "mrsPtpIeee1588Sync",
                "157": "mrsPtpOverE1Sync",
                "158": "mrsFixedFreqInSync",
                "159": "mrsPpsStringSync",
                "160": "mrsVarFreqGpioSync",
                "161": "mrsReserved",
                "162": "mrsDcf77PzfSync",
                "163": "mrsLongwaveSync",
                "164": "mrsGlonassGpsSync",
                "165": "mrsHavequickSync",
                "166": "mrsExtOscSync",
                "167": "mrsIntOscSync"
            }

        # from MBG-LANTIME-MIB.mib
        return {
            "0": "notavailable",
            "1": "normalOperation",
            "2": "trackingSearching",
            "3": "antennaFaulty",
            "4": "warmBoot",
            "5": "coldBoot",
            "6": "antennaShortcircuit"
        }

    def process_gps_position(self, helper, sess):
        """
        just print the current GPS position
        """

        gps_position = helper.get_snmp_value_or_exit(sess, helper, self.oids['oid_gps_position'])

        if gps_position:
            helper.add_summary(gps_position)
        else:
            helper.add_summary("Could not retrieve GPS position")
            helper.status(unknown)

    def process_status(self, helper, sess, check):
        """ get the snmp value, check the status and update the helper"""

        if check == 'ntp_current_state':
            ntp_status_int = helper.get_snmp_value_or_exit(sess, helper,
                                                           self.oids['oid_ntp_current_state_int'])
            result = self.check_ntp_status(ntp_status_int)
        elif check == 'gps_mode':
            gps_status_int = helper.get_snmp_value_or_exit(sess, helper,
                                                           self.oids['oid_gps_mode_int'])
            result = self.check_gps_status(gps_status_int)
        else:
            return

        helper.update_status(helper, result)

    def check_ntp_status(self, ntp_status_int):
        """
        check the NTP status
        """
        # convert the ntp_status integer value in a human readable value
        ntp_status_string = self.ntp_status.get(ntp_status_int, "unknown")

        if ntp_status_string == "unknown":
            return warning, ("NTP status: " + ntp_status_string)

        # the ntp status should be synchronized (new MIB) or normalOperation (old mib)
        elif ntp_status_string != "synchronized" and ntp_status_string != "normalOperationPPS":
            # that is a critical condition, because the time reference will not be reliable anymore
            return critical, ("NTP status: " + ntp_status_string)

        return None

    def check_gps_status(self, gps_status_int):
        """
        check the GPS status
        """
        gps_mode_string = self.gps_mode.get(gps_status_int, "unknown")

        if gps_mode_string == "unknown":
            return warning, ("GPS status: " + gps_mode_string)

        elif gps_mode_string != "normalOperation" \
                and gps_mode_string != "gpsSync":
            # that is a warning condition, NTP could still work without the GPS antenna
            return warning, ("GPS status: " + gps_mode_string)

        return None

    def process_satellites(self, helper, sess):
        """
        check and show the good satellites
        """
        good_satellites = helper.get_snmp_value_or_exit(sess, helper,
                                                        self.oids['oid_gps_satellites_good'])

        # Show the summary and add the metric and afterwards check the metric
        helper.add_summary("Good satellites: {}".format(good_satellites))
        helper.add_metric(label='satellites', value=good_satellites)
