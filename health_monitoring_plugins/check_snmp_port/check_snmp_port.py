#!/usr/bin/python
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
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown
import netsnmp

def get_data(host, version, community, oid):
    """
    function for snmp get
    """
    var = netsnmp.Varbind(oid)
    data = netsnmp.snmpget(var, Version=version, DestHost=host, Community=community)
    value = data[0]
    return value

def walk_data(host, version, community, oid):
    """
    function for snmp walk
    """
    var = netsnmp.Varbind(oid)
    data = netsnmp.snmpwalk(var, Version=version, DestHost=host, Community=community)
    return data

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
        if port != "scan":
            helper.exit(summary="Port (-p) must be a integer value or 'scan'.", exit_code=unknown, perfdata='')

def check_udp(helper, host, version, community, port):
    """
    the check logic for UDP ports
    """
    open_ports = walk_data(host, version, community, ".1.3.6.1.2.1.7.5.1.2") # the udpLocaLPort from UDP-MIB.mib (deprecated)
    
    # here we show all open UDP ports
    if port == "scan":
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

def check_tcp(helper, host, version, community, port, warning_param, critical_param):
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
    open_ports = walk_data(host, version, community, ".1.3.6.1.2.1.6.13.1.3") #tcpConnLocalPort from TCP-MIB (deprecated)
    # collect all status information about the open ports
    port_status = walk_data(host, version, community, ".1.3.6.1.2.1.6.13.1.1") #tcpConnState from TCP-MIB (deprecated)
    # make a dict out of the two lists
    port_and_status = dict(zip(open_ports, port_status))
    
    # here we show all open TCP ports and it's status
    if port == "scan":
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
            
# Create an instance of PluginHelper()
helper = PluginHelper()

if __name__ == "__main__":
    # Add command line parameters
    helper.parser.add_option('-H', dest="hostname", help="Hostname or ip address", default="localhost")
    helper.parser.add_option('-C', '--community', dest="community",  help='SNMP community of the SNMP service on target host.', default='public')
    helper.parser.add_option('-V', '--snmpversion', dest='version', help='SNMP version. (1 or 2)', default=2, type='int')
    helper.parser.add_option('-p', '--port', dest='port', help='The port you want to monitor (scan for scanning)', type='str', default='scan')
    helper.parser.add_option('-t', '--type', dest="type", help="TCP or UDP", default="udp")
    helper.parser.add_option('-w', dest="warning", help="warning values", default="synSent")
    helper.parser.add_option('-c', dest="critical", help="critical vales",default="closed")

    helper.parse_arguments()    

    # get the options
    typ = helper.options.type.lower()
    port = helper.options.port
    host = helper.options.hostname
    version = helper.options.version
    community = helper.options.community
    warning_param = helper.options.warning
    critical_param = helper.options.critical

    check_typ(helper, typ) 

    check_port(helper, port)

    # The default return value should be always OK
    helper.status(ok)

    #############
    # Check UDP
    #############

    if typ == "udp":
        helper.add_summary(check_udp(helper, host, version, community, port))

    # ############
    # # here we now want to check TCP ports
    # ############
   
    if typ == "tcp":
        helper.add_summary(check_tcp(helper, host, version, community, port, warning_param, critical_param))
     
    # Print out plugin information and exit nagios-style
    helper.exit()