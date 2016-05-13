#!/usr/bin/env python

__author__ = "Bernhard Rottmar"
__license__ = """
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import argparse, collections, sys, netsnmp, pynag.Plugins
from pynag.Plugins import PluginHelper, ok, warning, critical, unknown

class CHECK_TYPE(enumerate):
    CTS = 0
    DSR = 1
    DTR = 2
    ErrorCountFrame = 3
    ErrorCountBreak = 4
    ErrorCountOverrun = 5
    ErrorCountParity = 6

def genMoxaRS232VarList(port):
    moxaRS232VarList = netsnmp.VarList(
        netsnmp.Varbind('.1.3.6.1.4.1.8691.2.8.1.6.2.1.1.8.' + port),   ##CTS
        netsnmp.Varbind('.1.3.6.1.4.1.8691.2.8.1.6.2.1.1.5.' + port),   ##DSR
        netsnmp.Varbind('.1.3.6.1.4.1.8691.2.8.1.6.2.1.1.6.' + port),   ##DTR
        netsnmp.Varbind('.1.3.6.1.4.1.8691.2.8.1.6.3.1.1.1.' + port),   ##ErrorCountFrame
        netsnmp.Varbind('.1.3.6.1.4.1.8691.2.8.1.6.3.1.1.4.' + port),   ##ErrorCountBreak
        netsnmp.Varbind('.1.3.6.1.4.1.8691.2.8.1.6.3.1.1.3.' + port),   ##ErrorCountOverrun
        netsnmp.Varbind('.1.3.6.1.4.1.8691.2.8.1.6.3.1.1.2.' + port)    ##ErrorCountParity
    )
    return moxaRS232VarList

def append_output(helper, state, short_output_line, long_output_line):
    helper.add_status(state)
    helper.add_summary(short_output_line)
    helper.add_long_output(long_output_line)

def get_state(value, warning_threshold, critical_threshold):
    if value >= critical_threshold:
        return critical
    elif value >= warning_threshold:
        return warning
    else:
        return ok

if __name__ == '__main__':
    helper = PluginHelper()
    helper.parser.add_option('-H', '--hostname', dest='hostname', help='Host name or IP Adress of hte MOXA device.')
    helper.parser.add_option('-C', '--community', dest='community', help='SNMP community of the SNMP service on target host.', default='public')
    helper.parser.add_option('-V', '--snmpversion', dest='snmpversion', help='SNMP version.', default=2, type='int')
    helper.parser.add_option('-p', '--port', dest='port', help='Moxa RS232 port number.', type='str')
    helper.parser.add_option('-t', '--type', dest='type', help= """Available check types: CTS, DSR, DTR, ErrorCount. Example: -t CTS_ErrorCount. 
                                                                CTS (Clear To Send): DCE (Data Communication Equipment) is ready to accept data from the DTE (Data Terminal Equipment). 
                                                                DSR (Data Set Ready): DCE (Data Communication Equipment) is ready to receive commands or data. 
                                                                DTR (Data Terminal Ready): DTE (Data Terminal Equipment) is ready to receive, initiate, or continue a call. 
                                                                ErrorCount = Show error counts of Frame, Break, Overrun and Parity.""" , type='str')
    helper.parser.add_option('-c', '--critical', dest='critical', help='Return CRITICAL if any ErrorCount >= this parameter.', default=sys.maxint, type='int')
    helper.parser.add_option('-w', '--warning', dest='warning', help='Return WARNING if any ErrorCount >= this parameter.', default=1, type='int')
    helper.parse_arguments()

    if not helper.options.hostname:
        helper.parser.error('You must specifiy host ip in order to run this plugin.')
    if not helper.options.port:
        helper.parser.error('You must specifiy moxa rs232 port in order to run this plugin.')

    # create a netsnmp session object that is used for all following snmp operations
    session = netsnmp.Session(DestHost=helper.options.hostname, Community=helper.options.community, Version=helper.options.snmpversion)

    # send OIDs and get results
    moxaRS232VarList = genMoxaRS232VarList(helper.options.port)
    moxa_oid_results = session.get(moxaRS232VarList)
    if not all(moxa_oid_results):
        append_output(helper, unknown, "Can't connect to SNMP agent at application server or RS232 port does not exist.", "")
        helper.exit()

    # process the results: For each parameter, check if user wants to see this result and write output log. Missing t-parameter results in all 

    check_types = helper.options.type

    if not check_types or 'CTS' in check_types:
        if moxa_oid_results[CHECK_TYPE.CTS] == '0':
            append_output(helper, critical, 'CTS NOK', 'CTS (Clear To Send) not ready')
        else:
            append_output(helper, ok, 'CTS OK', 'CTS (Clear To Send) ready')

    if not check_types or 'DSR' in check_types:
        if moxa_oid_results[CHECK_TYPE.DSR] == '0':
            append_output(helper, critical, 'DSR NOK', 'DSR (Data Set Ready) not ready')
        else:
            append_output(helper, ok, 'DSR OK', 'DSR (Data Set Ready) ready')

    if not check_types or 'DTR' in check_types:
        if moxa_oid_results[CHECK_TYPE.DTR] == '0':
            append_output(helper, critical, 'DTR NOK', 'DTR (Data Terminal Ready) not ready')
        else:
            append_output(helper, ok, 'DTR OK', 'DTR (Data Terminal Ready) ready')

    if not check_types or 'ErrorCount' in check_types or 'Error Count' in check_types:

        warning_threshold = helper.options.warning
        critical_threshold = helper.options.critical
        error_frame =   moxa_oid_results[CHECK_TYPE.ErrorCountFrame]
        error_break =   moxa_oid_results[CHECK_TYPE.ErrorCountBreak]
        error_overrun = moxa_oid_results[CHECK_TYPE.ErrorCountOverrun]
        error_parity =  moxa_oid_results[CHECK_TYPE.ErrorCountParity]
     
        append_output(helper, get_state(int(error_frame),   warning_threshold, critical_threshold), 'ErrorCountFrame=' + error_frame, 'Error Count Frame = ' + error_frame)
        append_output(helper, get_state(int(error_break),   warning_threshold, critical_threshold), 'ErrorCountBreak=' + error_break, 'Error Count Break = ' + error_break)
        append_output(helper, get_state(int(error_overrun), warning_threshold, critical_threshold), 'ErrorCountOverrun=' + error_overrun, 'Error Count Overrun = ' + error_overrun)
        append_output(helper, get_state(int(error_parity),  warning_threshold, critical_threshold), 'ErrorCountParity=' + error_parity, 'Error Count Parity = ' + error_parity)

    helper.exit()
