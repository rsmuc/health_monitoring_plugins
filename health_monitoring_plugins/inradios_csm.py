#    Copyright (C) 2018 - 2019 haxtibal <haxtibal@posteo.de>

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
import pynag.Plugins

class InradiosCsmHealth(object):
    csm_to_icinga_status = {
        0: pynag.Plugins.unknown,
        1: pynag.Plugins.unknown,
        2: pynag.Plugins.ok,
        3: pynag.Plugins.warning,
        4: pynag.Plugins.critical
    }

    csm_to_str = ("Not ready", "Not available", "OK", "Warning", "Alarm")

    def __init__(self, snmp_session, meas_id):
        self.snmp_session = snmp_session
        self.meas_id = meas_id

    def make_meas_varlist(self):
        oid_list = [netsnmp.Varbind('.1.3.6.1.4.1.2566.127.6.1.10.1.1.1.{}.{}'
                                    .format(x, self.meas_id)) for x in range(1, 12)]
        return netsnmp.VarList(*oid_list)

    def check(self):
        try:
            self.snmp_data = self.get_data()
        except (TypeError, KeyError, ValueError):
            self.snmp_data = None

    def get_data(self):
        varlist = self.make_meas_varlist()
        response = self.snmp_session.get(varlist)
        snmp_data = {
            'comment': str(response[0]),
            'value': float(response[1]) if response[1] else None,
            'valueDateTime': str(response[2]) if response[2] else None,
            'parameter': str(response[3]),
            'status': int(response[4]),
            'uom': str(response[5]) if response[5] else None,
            'warn_upper': float(response[6]),
            'alarm_upper': float(response[7]),
            'warn_lower': float(response[8]),
            'alarm_lower': float(response[9]),
            'label': str(response[10]) if response[10] else "Measurement ID {}".format(self.meas_id)
        }
        return snmp_data

    def feed_icinga_plugin(self, icinga_plugin):
        if not self.snmp_data:
            icinga_plugin.show_status_in_summary = True
            icinga_plugin.status(pynag.Plugins.unknown)
            icinga_plugin.add_summary("SNMP response incomplete or invalid")
            return
        icinga_plugin.show_status_in_summary = False
        icinga_plugin.status(self.csm_to_icinga_status[self.snmp_data['status']])
        icinga_plugin.add_summary(self.make_summary())
        for prm_info in self.make_prm_info():
                icinga_plugin.add_long_output(prm_info)
        if self.snmp_data['value']:
            icinga_plugin.add_metric(**self.make_metric())

    def make_summary(self):
        summary_fmt = "{} - {} ({})"
        return summary_fmt.format(self.csm_to_str[self.snmp_data['status']],
                                  self.make_value_str(), self.make_clock_str())

    def make_clock_str(self):
        date_time = "last update: {}"
        if self.snmp_data['valueDateTime']:
            return date_time.format(self.snmp_data['valueDateTime'].split(' ')[-1])
        else:
            return date_time.format("n/a")

    def make_value_str(self):
        value_str = self.snmp_data['label']
        if self.snmp_data['value']:
            value_str += ' = ' + str(self.snmp_data['value'])
            if self.snmp_data['uom']:
                value_str += ' ' + self.snmp_data['uom']
        else:
            value_str += ' = n/a'
        return value_str

    def make_prm_info(self):
        prm_info = []
        for prm in self.snmp_data['parameter'].split(';'):
            if prm:
                prm_info.append(prm.strip())
        if self.snmp_data['valueDateTime']:
            prm_info.append("Last update: " + self.snmp_data['valueDateTime'])
        return prm_info

    def make_metric(self):
        metric = {'label': self.snmp_data['label'],
                   'value': self.snmp_data['value']}
        if self.snmp_data['uom']:
            metric['uom'] = self.snmp_data['uom']
        warn = self.format_perfdata(self.snmp_data.get('warn_lower'), self.snmp_data.get('warn_upper'))
        crit = self.format_perfdata(self.snmp_data.get('alarm_lower'), self.snmp_data.get('alarm_upper'))
        if warn:
            metric['warn'] = warn
        if crit:
            metric['crit'] = crit
        return metric

    def format_perfdata(self, lower, upper):
        neg_inf = float('-inf')
        pos_inf = float('inf')
        # NaN can be tested by testing equality to itself
        if not lower or lower != lower:
            lower = neg_inf
        if not upper or upper != upper:
            upper = pos_inf
        if lower == neg_inf and upper == pos_inf:
            return None
        return "{:.7g}..{:.7g}".format(lower, upper)
