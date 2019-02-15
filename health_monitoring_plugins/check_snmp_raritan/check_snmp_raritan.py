#!/usr/bin/env python

# check_snmp_raritan.py - Check a Raritan Dominition PX PDU (Power Distribution Unit), the inlets, outlets and the connected sensors

# Copyright (C) 2016 rsmuc <rsmuc@mailbox.org>

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
