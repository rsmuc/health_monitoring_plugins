#!/usr/bin/python
# check_api_pihole.py - Check the dns filter pihole via it's json api

# Copyright (C) 2017 rsmuc rsmuc@mailbox.org
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with check_snmp_procurve.py.  If not, see <http://www.gnu.org/licenses/>.

# Import PluginHelper and some utility constants from the Plugins module
import sys
import os
import netsnmp
sys.path.insert(1, os.path.join(sys.path[0], os.pardir))
from snmpSessionBaseClass import verify_host
from pynag.Plugins import PluginHelper, ok, critical, unknown, warning

# Create an instance of PluginHelper()
helper = PluginHelper()
helper.parser.add_option('-p', help="the port the lighthttp webserver (default: 80)", dest="port", default="80")
helper.parser.add_option('-H', help="the IP address or hostname pihole is running)", dest="host", default="127.0.0.1")
helper.parse_arguments()

# get the options
port = helper.options.port
host = helper.options.host


# The default return value should be always OK
helper.status(ok)

if __name__ == "__main__":

    
    import urllib, json
    url = "http://%s:%s/admin/api.php" % (host, port) 
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    percent_today = data['ads_percentage_today']
    domains_blocked = data['domains_being_blocked']
    dns_queries_today = data['dns_queries_today']
    
    helper.add_summary("Blocked Today: %s%%" % percent_today)
    helper.add_metric(label='blocked_today',value=percent_today, uom="%%") 
    
    helper.add_summary("Domains being blocked: %s" % domains_blocked)
    helper.add_metric(label='domains_being_blocked',value=domains_blocked, uom="Domains")
    
    helper.add_summary("DNS queries today: %s" % dns_queries_today)
    helper.add_metric(label='dns_queries_today',value=dns_queries_today)

    # there is only the satellites metric, but we will check all available
    helper.check_all_metrics()

    # Print plugin information and exit nagios-style
    helper.exit()
