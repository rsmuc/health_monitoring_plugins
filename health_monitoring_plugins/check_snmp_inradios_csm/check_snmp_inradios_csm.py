#!/usr/bin/env python

#    Copyright (C) 2018-2019 haxtibal haxtibal@posteo.de

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