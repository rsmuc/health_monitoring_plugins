"""
Module for check_snmp_eaton_ups
"""

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


from __future__ import division
from pynag.Plugins import ok, unknown, critical, new_threshold_syntax

INDEX_SCALAR = 0
INDEX_INOUT_LINES = 1

# Eaton puts both L-N and L-L values into their tables, so we can't apply one single threshold to the whole table.
# Only consider first three rows (all L-N) for now.
MAX_INOUT_LINES_ENTRIES = 3


def available_types():
    return GENERIC_STATES.keys()


def calc_frequency(the_snmp_value):
    """calculate the frequency"""
    return int(the_snmp_value) / 10


def calc_output_current(the_snmp_value):
    """calculate the current"""
    return int(the_snmp_value) / 10


GENERIC_STATES = {

    "on_battery": {"oid": ".1.3.6.1.2.1.33.1.2.2.0",
                   "unit": "s",
                   "message": "time running on battery",
                   "indexing": INDEX_SCALAR},

    "remaining_battery_time": {"oid": ".1.3.6.1.2.1.33.1.2.3.0",
                               "unit": "min",
                               "message": "time remaining on battery",
                               "indexing": INDEX_SCALAR},

    "input_frequency": {"oid": ".1.3.6.1.2.1.33.1.3.3.1.2",
                        "unit": "Hz",
                        "message": "input frequency",
                        "indexing": INDEX_INOUT_LINES,
                        "converter": calc_frequency},

    "input_voltage": {"oid": ".1.3.6.1.2.1.33.1.3.3.1.3",
                      "unit": "VAC",
                      "message": "input voltage",
                      "indexing": INDEX_INOUT_LINES},

    "output_voltage": {"oid": ".1.3.6.1.2.1.33.1.4.4.1.2",
                       "unit": "VAC",
                       "message": "output voltage",
                       "indexing": INDEX_INOUT_LINES},

    "output_current": {"oid": ".1.3.6.1.2.1.33.1.4.4.1.3",
                       "unit": "A",
                       "message": "output current",
                       "indexing": INDEX_INOUT_LINES,
                       "converter": calc_output_current},

    "output_power": {"oid": ".1.3.6.1.2.1.33.1.4.4.1.4",
                     "unit": "W",
                     "message": "output power",
                     "indexing": INDEX_INOUT_LINES},

    "output_load": {"oid": ".1.3.6.1.2.1.33.1.4.4.1.5",
                    "unit": "%",
                    "message": "output load",
                    "indexing": INDEX_INOUT_LINES},

    "alarms": {"oid": ".1.3.6.1.2.1.33.1.6.1.0",
               "unit": "",
               "message": "active alarms",
               "indexing": INDEX_SCALAR},

    "battery_capacity": {"oid": ".1.3.6.1.4.1.534.1.2.4.0",
                         "unit": "%",
                         "message": "remaining battery capacity",
                         "indexing": INDEX_SCALAR},

    "environment_temperature": {"oid": ".1.3.6.1.4.1.534.1.6.1.0",
                                "unit": "deg C",
                                "message": "environment temperature",
                                "indexing": INDEX_SCALAR},

    "external_environment_temperature": {"oid": ".1.3.6.1.4.1.534.1.6.5.0",
                                         "unit": "deg C",
                                         "message": "external environment temperature",
                                         "indexing": INDEX_SCALAR},
}


class EatonUPS(object):
    """Check logic for various Eaton UPS devices based on UPS-MIB and XUPS-MIB"""

    def __init__(self, session, helper):
        self.session = session
        self.helper = helper
        self.helper.status(ok)
        self.helper.options.type = helper.options.type.lower()

    def get_threshold(self):
        "Get threshold passed with '--thresholds' as new style threshold object."
        threshold = None
        for cmdline_threshold in self.helper.thresholds:
            parsed_threshold = new_threshold_syntax.parse_threshold(cmdline_threshold)
            if parsed_threshold['metric'] == self.helper.options.type:
                threshold = parsed_threshold['thresholds']
        return threshold

    def check_all_metrics(self, values, threshold):
        """Check given values against a threshold.

        If there's more than one value in values,
        append ascending numbers starting at 1 to label and message.
        """
        summaries = []
        if len(values) > 1:
            suffix = " {}"
        else:
            suffix = ""
        for index, value in enumerate(values, 1):
            metric_name = (self.helper.options.type + suffix).format(index)
            metric_message = (GENERIC_STATES[self.helper.options.type]["message"] + suffix).format(index)
            uom = GENERIC_STATES[self.helper.options.type]["unit"]
            self.helper.add_metric(
                label=metric_name,
                value=value,
                uom=uom)
            if self.helper.options.type == "alarms":
                if value != "0":
                    self.helper.status(critical)
            elif threshold:
                self.helper.check_metric(metric_name, threshold)
            summaries.append("{} = {} {}".format(metric_message, value, uom))
        for summary in summaries:
            self.helper.add_summary(summary)

    def check_generic_status(self):
        """ check a generic status of the UPS"""
        indexing = GENERIC_STATES[self.helper.options.type]["indexing"]
        if indexing == INDEX_SCALAR:
            values = []
            value = self.helper.get_snmp_value_or_exit(
                self.session, self.helper, GENERIC_STATES[self.helper.options.type]["oid"])
            if value:
                values.append(value)
        elif indexing == INDEX_INOUT_LINES:
            values = self.helper.walk_snmp_values_or_exit(
                self.session, self.helper, GENERIC_STATES[self.helper.options.type]["oid"],
                GENERIC_STATES[self.helper.options.type]["message"])
            values = values[:MAX_INOUT_LINES_ENTRIES]
        if not values:
            self.helper.exit(summary="No response from device ", exit_code=unknown,
                             perfdata='')
        if 'converter' in GENERIC_STATES[self.helper.options.type]:
            values = [GENERIC_STATES[self.helper.options.type]['converter'](value) for value in values]
        self.check_all_metrics(values, self.get_threshold())