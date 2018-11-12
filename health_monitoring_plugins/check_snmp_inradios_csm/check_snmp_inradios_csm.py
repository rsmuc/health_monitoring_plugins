#!/usr/bin/env python

# Copyright (C) 2018 haxtibal haxtibal@posteo.de

import netsnmp
import health_monitoring_plugins.inradios_csm

if __name__ == '__main__':
    helper = health_monitoring_plugins.SnmpHelper()
    helper.parser.add_option('-i', '--id', dest='id', type="int",
                             help='Identify a measurement. See description of INRADIOS::csmMonitoringTableIndex.')
    helper.parse_arguments()
    if (not helper.options.hostname):
        helper.parser.error("Server not specified.")
    if (not helper.options.id):
        helper.parser.error("Measurement id not specified.")
    snmp_session = netsnmp.Session(**helper.get_snmp_args())
    inradios_health = health_monitoring_plugins.inradios_csm.InradiosCsmHealth(snmp_session, helper.options.id)
    inradios_health.check()
    inradios_health.feed_icinga_plugin(helper)
    helper.exit()