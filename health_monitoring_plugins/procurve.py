"""
Module for check_snmp_procurve
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
from pynag.Plugins import unknown, critical, warning


# required OIDS
# The sensor description (e.g. Power Supply Sensor or Fan Sensor)
OID_DESCRIPTION = ".1.3.6.1.4.1.11.2.14.11.1.2.6.1.7"
# The status of the sensor
OID_STATUS = ".1.3.6.1.4.1.11.2.14.11.1.2.6.1.4"


# Sensor Status table
SENOR_STATUS_TABLE = {
    "1": "unknown",
    "2": "bad",
    "3": "warning",
    "4": "good",
    "5": "notPresent"
}


class Procurve(object):
    """Class for check_snmp_time2"""

    def __init__(self, session):
        self.sess = session

    @staticmethod
    def check_sensors(helper, session):
        """
        collect and check all available sensors
        """

        all_sensors = helper.walk_snmp_values_or_exit(session, helper, OID_DESCRIPTION, "Sensors")
        all_status = helper.walk_snmp_values_or_exit(session, helper, OID_STATUS, "Sensor Status")

        # here we zip all index and descriptions to have a list like
        # [('Fan Sensor', '2'), ('Power Supply Sensor', '4')]
        # we are doomed if the lists do not have the same length ...
        # but that should never happen ... hopefully
        zipped = zip(all_sensors, all_status)

        for sensor in zipped:
            description = sensor[0]
            status = sensor[1]
            # translate the value to human readable
            try:
                status_string = SENOR_STATUS_TABLE[status]
            except KeyError:
                # if we receive an invalid value, we don't want to crash...
                helper.exit(summary="received an undefined value from device: " + status,
                            exit_code=critical, perfdata='')

            # for each sensor the summary is added like: Fan Sensor: good
            helper.add_summary("%s: %s" % (description, status_string))

            # set the status
            if status == "2":
                helper.status(critical)
            if status == "3":
                helper.status(warning)
