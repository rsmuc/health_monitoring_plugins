#!/usr/bin/env python

# Copyright (C) 2019 haxtibal haxtibal@posteo.de

import netsnmp
import health_monitoring_plugins
import health_monitoring_plugins.microwavemodem as microwavemodem

if __name__ == '__main__':
    helper = health_monitoring_plugins.SnmpHelper()
    helper.parser.add_option('-m', '--modem', type='choice', choices=['SK-IP', 'AX-60'], help="Select modem model.")
    helper.parse_arguments()

    if (not helper.options.hostname):
        helper.parser.error("Host not specified.")
    if helper.options.modem == 'SK-IP':
        modem = microwavemodem.TYPE_SKIP
    elif helper.options.modem == 'AX-60':
        modem = microwavemodem.TYPE_AX60
    else:
        helper.parser.error("Modem type not specified or unknown.")

    snmp_session = netsnmp.Session(**helper.get_snmp_args())
    microwavemodem = microwavemodem.MicrowaveModem(modem, snmp_session)
    microwavemodem.check()
    microwavemodem.feed_icinga_plugin(helper)
    helper.exit()
