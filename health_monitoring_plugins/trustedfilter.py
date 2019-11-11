#    Copyright (C) 2017-2019 rsmuc <rsmuc@sec-dev.de>

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

from pynag.Plugins import PluginHelper,ok,warning,critical,unknown
import health_monitoring_plugins

# these dicts / definitions we need to get human readable values  
states = {
    1: 'ok',
    2: 'failed',
    3: 'absent',
    4: 'AC off' 
}

activity = {
    1: 'standby',
    2: 'active',
    3: 'error'
}

# OIDs
activity_oid   = '.1.3.6.1.4.1.2566.107.41.1.0'   #   tfDeviceActivityState
logfill_oid    = '.1.3.6.1.4.1.2566.107.31.2.1.0' #   slIpStatusLogFillLevel
ps1_oid        = '.1.3.6.1.4.1.2566.107.31.2.2.0' #   slIpStatusPowerSupplyUnit1
ps2_oid        = '.1.3.6.1.4.1.2566.107.31.2.3.0' #   slIpStatusPowerSupplyUnit2
fan1_oid       = '.1.3.6.1.4.1.2566.107.31.2.4.0' #   slIpStatusPowerFanUnit1
fan2_oid       = '.1.3.6.1.4.1.2566.107.31.2.5.0' #   slIpStatusPowerFanUnit2
bat_oid        = '.1.3.6.1.4.1.2566.107.31.2.7.0' #   slIpStatusInternalVoltage
temp_oid       = '.1.3.6.1.4.1.2566.107.31.2.8.0' #   slIpStatusInternalTemperature
activity_oid   = '.1.3.6.1.4.1.2566.107.41.1.0'   #   tfDeviceActivityState


class TrustedFilter(object):
    def __init__(self, helper, snmp1, snmp2=None):
        self.helper = helper
        self.snmp1 = snmp1
        self.snmp2 = snmp2

    def get_snmp_from_host1(self):
        """
        Get SNMP values from 1st host.
        """
        response = self.snmp1.get_oids(ps1_oid, ps2_oid, fan1_oid, fan2_oid, bat_oid, temp_oid, activity_oid, logfill_oid)
        self.ps1_value = states[int(response[0])]
        self.ps2_value = states[int(response[1])]
        self.fan1_value = states[int(response[2])]
        self.fan2_value = states[int(response[3])]
        self.bat_value = states[int(response[4])]
        self.temp_value = states[int(response[5])]
        self.activity_value1 = activity[int(response[6])]
        self.logfill_value = str(response[7])

    def get_snmp_from_host2(self):
        """
        Get SNMP values from 2nd host.
        """
        if not self.snmp2:
            self.activity_value2 = None
        else:
            response = self.snmp2.get_oids(activity_oid)
            self.activity_value2 = activity[int(response[0])]

    def check(self):
        """
        Evaluate health status from device parameters.
        """
        try:
            self.get_snmp_from_host1()
            self.get_snmp_from_host2()
        except (health_monitoring_plugins.SnmpException, TypeError, KeyError):
            self.helper.status(unknown)
            self.helper.add_summary("SNMP response incomplete or invalid")
            return

        self.helper.add_summary("Filter Status")
        self.helper.add_long_output("Power Supply 1: %s" % self.ps1_value)
        if self.ps1_value != "ok":
            self.helper.status(critical)
            self.helper.add_summary("Power Supply 1: %s" % self.ps1_value)

        self.helper.add_long_output("Power Supply 2: %s" % self.ps2_value)
        if self.ps2_value != "ok":
            self.helper.status(critical)
            self.helper.add_summary("Power Supply 2: %s" % self.ps2_value)

        self.helper.add_long_output("Fan 1: %s" % self.fan1_value)
        if self.fan1_value != "ok":
            self.helper.status(critical)
            self.helper.add_summary("Fan 1: %s" % self.fan1_value)

        self.helper.add_long_output("Fan 2: %s" % self.fan2_value)
        if self.fan2_value != "ok":
            self.helper.status(critical)
            self.helper.add_summary("Fan 2: %s" % self.fan2_value)

        self.helper.add_long_output("Battery: %s" % self.bat_value)
        if self.bat_value != "ok":
            self.helper.status(critical)
            self.helper.add_summary("Battery: %s" % self.bat_value)

        self.helper.add_long_output("Temperature: %s" % self.temp_value)
        if self.temp_value != "ok":
            self.helper.status(critical)
            self.helper.add_summary("Temperature: %s" % self.temp_value)

        self.helper.add_metric(label='logfill',value=self.logfill_value, uom="%%")
        self.helper.add_long_output("Fill Level internal log: %s%%" % self.logfill_value)

        self.helper.add_long_output("Activity State: %s" % self.activity_value1)
        if self.activity_value1 == "error":
            self.helper.status(critical)
            self.helper.add_summary("Activity State: %s" % self.activity_value1)

        if self.activity_value2:
            self.helper.add_long_output("Activity State 2: %s" % self.activity_value2)
            if self.activity_value1 == "active" and self.activity_value2 == "active":
                self.helper.status(critical)
                self.helper.add_summary("Filter 1 and Filter 2 active!")
                    
            if self.activity_value1 == "standby" and self.activity_value2 == "standby":
                self.helper.status(critical)
                self.helper.add_summary("Filter 1 and Filter 2 standby!")

        self.helper.check_all_metrics()
