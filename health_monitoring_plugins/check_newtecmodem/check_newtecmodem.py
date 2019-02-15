#!/usr/bin/env python

# Copyright (C) 2019 haxtibal haxtibal@posteo.de

import netsnmp
import health_monitoring_plugins
import health_monitoring_plugins.newtecmodem as newtecmodem

if __name__ == '__main__':
    helper = health_monitoring_plugins.SnmpHelper()
    helper.parser.add_option('-m', '--modem', type='choice', choices=['MDM6000', 'MDM9000'], help="Select modem model.")
    helper.parse_arguments()

    if (not helper.options.hostname):
        helper.parser.error("Host not specified.")
    if helper.options.modem == 'MDM6000':
        modem = newtecmodem.TYPE_MDM6000
    elif helper.options.modem == 'MDM9000':
        modem = newtecmodem.TYPE_MDM9000
    else:
        helper.parser.error("Modem type not specified or unknown.")

    snmp_session = netsnmp.Session(**helper.get_snmp_args())
    newtecmodem_health = newtecmodem.NewtecModem(modem, snmp_session)
    newtecmodem_health.check()
    newtecmodem_health.feed_icinga_plugin(helper)
    helper.exit()
