#!/usr/bin/python
# check_jenkins_api.py - Check the Jenkins queue. If there are jobs for more than X hours, critical will be shown.

# Copyright (C) 2018 rsmuc rsmuc@mailbox.org
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
# along with check_jenkins_api.py.  If not, see <http://www.gnu.org/licenses/>.

# Import PluginHelper and some utility constants from the Plugins module
import sys
import os
import urllib2, json, base64
from datetime import datetime
sys.path.insert(1, os.path.join(sys.path[0], os.pardir))
from pynag.Plugins import PluginHelper, ok, critical

# Create an instance of PluginHelper()
helper = PluginHelper()
helper.parser.add_option('-p', help="the port the Jenkins webserver (default: 80)", dest="port", default="80")
helper.parser.add_option('-H', help="the IP address or hostname of the Jenkins", dest="host", default="127.0.0.1")
helper.parser.add_option('-U', help="the user for the basic authentication)", dest="user", default="user")
helper.parser.add_option('-P', help="the password for the basic authentication)", dest="password", default="password")
helper.parser.add_option('-A', help="the maximum age of a Jenkins job in hours", dest="age", default="5.0")


helper.parse_arguments()

# get the options
port = helper.options.port
host = helper.options.host
user = helper.options.user
password = helper.options.password
age = float(helper.options.age)


# The default return value should be always OK
helper.status(ok)
helper.add_summary("Jenkins")

if __name__ == "__main__":    

    # query the data from the Jenkins JSON API
    url = "http://%s/queue/api/json?pretty=true:%s" % (host, port)

    request = urllib2.Request(url)
    base64string = base64.b64encode('%s:%s' % (user, password))
    request.add_header("Authorization", "Basic %s" % base64string)        
    response = urllib2.urlopen(request)
    data = json.loads(response.read())

    # check every job in the build queue
    for item in data['items']:
        starttime = item['inQueueSince']
        # quick and dirty
        starttime = datetime.fromtimestamp(float(starttime/1000))        
        currenttime = datetime.today()                
        waitingfor = abs(currenttime - starttime).total_seconds() / 3600.0
                
        if waitingfor > age:
                helper.status(critical)
                helper.add_summary("JENKINS JOB WAITING FOR %s hours - CHECK INSTANCES" % (waitingfor))
helper.exit()
