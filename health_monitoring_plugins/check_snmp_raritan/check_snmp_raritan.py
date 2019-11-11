#!/usr/bin/env python

# check_snmp_raritan.py - Check a Raritan Dominition PX PDU (Power Distribution Unit), the inlets, outlets and the connected sensors

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

import health_monitoring_plugins.raritan
from pynag.Plugins import ok

if __name__ == "__main__":
    helper = health_monitoring_plugins.SnmpHelper()
    helper.parser.add_option('-t', help="The type you want to monitor (inlet, outlet, sensor)", default="inlet", dest="typ")
    helper.parser.add_option('-i', help="The id of the outlet / sensor you want to monitor (1-99)", default="1", dest="id")
    helper.parse_arguments()

    sess = health_monitoring_plugins.SnmpSession(**helper.get_snmp_args())

    # The default return value should be always OK
    helper.status(ok)

    raritan = health_monitoring_plugins.raritan.Raritan(sess, helper.options.id)
    device_type = helper.options.typ.lower()
    if device_type == "inlet":
        raritan.check_inlet(helper)
    elif device_type == "outlet":
        raritan.check_outlet(helper)
    elif device_type == "sensor":
        raritan.check_sensor(helper)

    helper.exit()
