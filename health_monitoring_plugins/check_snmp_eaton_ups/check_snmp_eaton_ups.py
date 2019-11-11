#!/usr/bin/env python

# check_snmp_apc_ups.py - Check a Eaton APC UPS health state via SNMP
# implementing upsMIB and xupsMIB

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


# Import PluginHelper and some utility constants from the Plugins module
from pynag.Plugins import unknown
import health_monitoring_plugins.eaton

if __name__ == "__main__":

    # pylint: disable=C0103

    helper = health_monitoring_plugins.SnmpHelper()
    helper.parser.add_option('-t', '--type', dest='type',
                             help="Check type to execute. Available types are: {}".format(
                                 ', '.join(health_monitoring_plugins.eaton.available_types())),
                             type='str')
    helper.parse_arguments()
    sess = health_monitoring_plugins.SnmpSession(**helper.get_snmp_args())
    eaton_ups = health_monitoring_plugins.eaton.EatonUPS(sess, helper)
    if helper.options.type in health_monitoring_plugins.eaton.available_types():
        eaton_ups.check_generic_status()
    else:
        helper.exit(
            summary="Invalid check type {} specified or not available".format(helper.options.type),
            exit_code=unknown,
            perfdata='')
    helper.exit()
