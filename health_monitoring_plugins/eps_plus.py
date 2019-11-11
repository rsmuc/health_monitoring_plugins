"""
Module for check_snmp_eps_plus.py
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
from pynag.Plugins import critical, unknown

# that is the base oid
DEVICE_NAME_OID = ".1.3.6.1.4.1.24734.16.2.1.1.3"
OUTLET_NAME_OID = ".1.3.6.1.4.1.24734.16.8.1.1.4"
OUTLET_STATUS_OID = ".1.3.6.1.4.1.24734.16.8.1.1.5"
SENSOR_ID_OID = ".1.3.6.1.4.1.24734.16.5.1.1.3"
SENSOR_VALUE_OID = ".1.3.6.1.4.1.24734.16.5.1.1.6"


class EPSplus(object):
    """EpowerSwitch"""

    @staticmethod
    def get_outlet_info(helper, session):
        """ get the infos for the outlet """

        device_name_oid = "{}.{}".format(DEVICE_NAME_OID, helper.options.device)
        outlet_name_oid = "{}.{}.{}".format(OUTLET_NAME_OID,
                                            helper.options.device, helper.options.outlet)
        outlet_status_oid = "{}.{}.{}".format(OUTLET_STATUS_OID,
                                              helper.options.device, helper.options.outlet)

        return helper.get_snmp_values_or_exit(session, helper,
                                              device_name_oid, outlet_name_oid, outlet_status_oid)

    @staticmethod
    def get_sensor_info(helper, session):
        """ get the infos for the outlet """

        sensor_ids = helper.walk_snmp_values_or_exit(session, helper,
                                                     SENSOR_ID_OID, "Sensor IDs")
        sensor_values = helper.walk_snmp_values_or_exit(session, helper,
                                                        SENSOR_VALUE_OID, "Sensor Values")

        values = zip(sensor_ids, sensor_values)

        for entry in values:
            sid = entry[0]
            value = entry[1]
            unit = None
            name = None

            if "T" in sid:
                unit = "deg. C"
                name = "temperature sensor"
            elif "H" in sid:
                unit = "percent"
                name = "humidity sensor"

            if sid == helper.options.sensor:
                return name, value, unit

        helper.exit(summary="Sensor not found", exit_code=unknown, perfdata='')
        return None

    def check_outlet(self, helper, session):
        """
        check the status of an outlet (on, off)
        """

        infos = self.get_outlet_info(helper, session)

        device_name = infos[0]
        outlet_name = infos[1]
        outlet_status = infos[2]

        helper.add_summary("{} - {}: {}".format(device_name, outlet_name, outlet_status))

        if outlet_status != helper.options.expected:
            helper.status(critical)

    def check_sensor(self, helper, session):
        """
        check the value of an sensor
        """

        infos = self.get_sensor_info(helper, session)

        sensor_name = infos[0]
        sensor_value = infos[1]
        sensor_unit = infos[2]

        helper.add_summary("{}: {} {}".format(sensor_name, sensor_value, sensor_unit))
        helper.add_metric("{} (in {})".format(sensor_name, sensor_unit).lower(),
                          sensor_value, "", "", "", "", "")
