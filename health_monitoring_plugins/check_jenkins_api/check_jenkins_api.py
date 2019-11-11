#!/usr/bin/python
# check_jenkins_api.py - Check the Jenkins queue. If there are jobs for more than X hours, critical will be shown.

#    Copyright (C) 2018-2019 rsmuc <rsmuc@sec-dev.de>

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
import sys
import os
import urllib2
import json
import base64
from datetime import datetime
sys.path.insert(1, os.path.join(sys.path[0], os.pardir))
from pynag.Plugins import PluginHelper, ok, critical, unknown, warning

# Create an instance of PluginHelper()
helper = PluginHelper()
helper.parser.add_option('-p', help="the port the Jenkins webserver (default: 80)", dest="port", default="80")
helper.parser.add_option('-H', help="the IP address or hostname of the Jenkins", dest="host", default="127.0.0.1")
helper.parser.add_option('-U', help="the user for the basic authentication", dest="user", default="user")
helper.parser.add_option('-P', help="the password for the basic authentication or the API token", dest="password", default="password")
helper.parser.add_option('--PWF', help="a file containing the password", dest="pwf")
helper.parser.add_option('-A', help="the maximum age of a Jenkins job in hours", dest="age")
helper.parser.add_option('-S', help="check if Jenkins is in shudown mode", dest="shutdown", default=False, action='store_true')
helper.parser.add_option('-D', help="check if a Jenkins executor is disconnected", dest="disconnect", default=False, action='store_true')


helper.parse_arguments()

# get the options
port = helper.options.port
host = helper.options.host
user = helper.options.user
password = helper.options.password
if helper.options.age:
    age = float(helper.options.age)
else:
    age = None
shutdown = helper.options.shutdown
disconnect = helper.options.disconnect
pwf = helper.options.pwf

if pwf:
    with open(pwf, 'r') as myfile:
        password=myfile.read().replace('\n', '')

# The default return value should be always OK
helper.status(ok)
helper.add_summary("%s" % host)

if __name__ == "__main__":    

    if age:
        helper.add_summary("job queue:")
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
    
    elif shutdown:
        helper.add_summary("shutdown status:")
        # query the data from the Jenkins JSON API
        url = "http://%s/api/json?pretty=true:%s" % (host, port)

        request = urllib2.Request(url)
        base64string = base64.b64encode('%s:%s' % (user, password))
        request.add_header("Authorization", "Basic %s" % base64string)        
        response = urllib2.urlopen(request)
        data = json.loads(response.read())

        if data["quietingDown"] is True:
            helper.status(warning)
            helper.add_summary("JENKINS IS IN SHUTDOWN MODE")

    elif disconnect:
        helper.add_summary("executor status:")
        # query the data from the Jenkins JSON API
        url = "http://%s/computer/api/json?pretty=true:%s" % (host, port)

        request = urllib2.Request(url)
        base64string = base64.b64encode('%s:%s' % (user, password))
        request.add_header("Authorization", "Basic %s" % base64string)        
        response = urllib2.urlopen(request)
        data = json.loads(response.read())

        for computer in data['computer']:
            
            if computer["temporarilyOffline"] is True:
                helper.status(warning)
                helper.add_summary("Jenkins executor temporarily offline")

            if computer["offline"] is True:
                helper.status(critical)
                helper.add_summary("Jenkins executor temporarily offline")
                
    else:
        helper.status(unknown)
        helper.add_summary("Missing parameter")
helper.exit()
