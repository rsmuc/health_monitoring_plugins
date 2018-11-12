#!/usr/bin/env python
# check_snmp_trusted_filter.py - Check a trusted filter

# Copyright (C) 2017 rsmuc <rsmuc@mailbox.org>

import netsnmp
import pynag.Plugins
import health_monitoring_plugins.trustedfilter

if __name__ == "__main__":
    helper = health_monitoring_plugins.SnmpHelper()
    helper.parser.add_option('-s', '--secondhost', dest='secondhost', type='str',
                             help = "Enter a second host to be checked for ActivityState")
    helper.parse_arguments()
    helper.status(pynag.Plugins.ok)

    snmp_args = helper.get_snmp_args()
    snmp1 = health_monitoring_plugins.SnmpSession(**snmp_args)
    if helper.options.secondhost:
        snmp_args['DestHost'] = helper.options.secondhost
        snmp2 = health_monitoring_plugins.SnmpSession(**snmp_args)
    else:
        snmp2 = None

    trustedFilter = health_monitoring_plugins.trustedfilter.TrustedFilter(helper, snmp1, snmp2)
    trustedFilter.check()

    helper.exit()