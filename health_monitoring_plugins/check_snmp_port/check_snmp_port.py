#!/usr/bin/env python
# check_snmp_port.py - Check the status of a tcp/udp port via SNMP. For TCP port also the status is checked.

# Copyright (C) 2016 rsmuc <rsmuc@mailbox.org>
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
# along with check_snmp_port.py.  If not, see <http://www.gnu.org/licenses/>.

# Import PluginHelper and some utility constants from the Plugins module
import sys
import os
import netsnmp
sys.path.insert(1, os.path.join(sys.path[0], os.pardir)) 
from snmpSessionBaseClass import add_common_options, get_common_options, verify_host, walk_data
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown


# Create an instance of PluginHelper()
helper = PluginHelper()

# Add command line parameters
add_common_options(helper)
helper.parser.add_option('-p', '--port', dest='port', help='The port you want to monitor', type='str', default='')
helper.parser.add_option('-s', '--scan',   dest  = 'scan_flag', default   = False,    action = "store_true", help      = 'Show all open ports')
helper.parser.add_option('-t', '--type', dest="type", help="TCP or UDP", default="udp")
helper.parser.add_option('-w', dest="warning", help="warning values", default="synSent")
helper.parser.add_option('-c', dest="critical", help="critical vales",default="closed")
helper.parse_arguments()    

# get the options
typ = helper.options.type.lower()
port = helper.options.port
scan = helper.options.scan_flag
host, version, community = get_common_options(helper)
warning_param = helper.options.warning
critical_param = helper.options.critical

def check_typ(helper, typ):
    """
    check if typ parameter is TCP or UDP
    """
    if typ != "tcp" and typ != "udp":
        helper.exit(summary="Type (-t) must be udp or tcp.", exit_code=unknown, perfdata='')

def check_port(helper, port):
    """
    check if the port parameter is really a port or "scan"
    """
    try:
        int(port)
    except ValueError:
        helper.exit(summary="Port (-p) must be a integer value.", exit_code=unknown, perfdata='')

def check_udp(helper, host, port, session):
    """
    the check logic for UDP ports
    """
    open_ports = walk_data(session, '.1.3.6.1.2.1.7.5.1.2', helper)[0] # the udpLocaLPort from UDP-MIB.mib (deprecated)
    
    # here we show all open UDP ports
    if scan:
        print "All open UDP ports at host " + host
        for port in open_ports:
            print "UDP: \t" + port
        quit()
    
    if port in open_ports:        
        udp_status = "OPEN"
    else:
        udp_status = "CLOSED"
        helper.status(critical)
    return ("Current status for UDP port " + port + " is: " + udp_status)

def check_tcp(helper, host, port, warning_param, critical_param, session):
    """
    the check logic for check TCP ports
    """
    
    # from tcpConnState from TCP-MIB
    tcp_translate = {
    
    "1" :   "closed",
    "2" :   "listen",
    "3" :   "synSent",
    "4" :   "synReceived",
    "5" :   "established",
    "6" :   "finWait1",
    "7" :   "finWait2",
    "8" :   "closeWait",
    "9" :   "lastAck",
    "10":   "closing",
    "11":   "timeWait",
    "12":   "deleteTCB"

    }

    # collect all open local ports
    open_ports = walk_data(session, '.1.3.6.1.2.1.6.13.1.3', helper)[0] #tcpConnLocalPort from TCP-MIB (deprecated)
    # collect all status information about the open ports
    port_status = walk_data(session, '.1.3.6.1.2.1.6.13.1.1', helper)[0] #tcpConnState from TCP-MIB (deprecated)
    # make a dict out of the two lists
    port_and_status = dict(zip(open_ports, port_status))
    
    # here we show all open TCP ports and it's status
    if scan:
        print "All open TCP ports: " + host
        for port in open_ports:
            tcp_status = port_and_status[port]
            tcp_status = tcp_translate[tcp_status]
            print "TCP: \t" + port + "\t Status: \t" + tcp_status
        quit()
    
    #here we have the real check logic for TCP ports
    if port in open_ports:
        # if the port is available in the list of open_ports, then extract the status
        tcp_status = port_and_status[port]
        # translate the status from the integer value to a human readable string
        tcp_status = tcp_translate[tcp_status]
             
        # now let's set the status according to the warning / critical "threshold" parameter        
        if tcp_status in warning_param:
            helper.status(warning)
        elif tcp_status in critical_param:
            helper.status(critical)
        else:
            helper.status(ok)    
    else:
        # if there is no value in the list => the port is closed for sure
        tcp_status = "CLOSED"
        helper.status(critical)
        
    return ("Current status for TCP port " + port + " is: " + tcp_status)
            
if __name__ == "__main__":

    # verify that a hostname is set
    verify_host(host, helper)

    sess = netsnmp.Session(Version=version, DestHost=host, Community=community)

    # if no port is set, we will do a scan
    if port == "" or port is None:
        scan = True
    else:
        check_port(helper, port)

    check_typ(helper, typ) 

    # The default return value should be always OK
    helper.status(ok)

    #############
    # Check UDP
    #############

    if typ == "udp":
        helper.add_summary(check_udp(helper, host, port, sess))

    # ############
    # Check TCP
    # ############
   
    if typ == "tcp":
        helper.add_summary(check_tcp(helper, host, port, warning_param, critical_param, sess))
     
    # Print out plugin information and exit nagios-style
    helper.exit()
