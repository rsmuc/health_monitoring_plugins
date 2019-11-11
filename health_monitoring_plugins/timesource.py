"""
Module for check_snmp_tim2
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

from __future__ import absolute_import, division, print_function
import time
import datetime
import struct
from pynag.Plugins import unknown

# The OIDs we need from HOST-RESOURCES-MIB
OID_TIME = ".1.3.6.1.2.1.25.1.2.0"
OID_DESCR = ".1.3.6.1.2.1.1.1.0"


class Timesource(object):
    """Class for check_snmp_time2"""

    def __init__(self, session):
        self.sess = session

    @staticmethod
    def is_windows(helper, session):
        """ check if the remote operating system is windows or not """
        # get the description (operating system)
        descr = helper.get_snmp_value_or_exit(session, helper, OID_DESCR)

        if str(descr).find('Windows') != -1:
            return True

        return False

    def get_local_timestamp(self, helper, session):
        """ return the local timestamp, depending on the remote device (UTC or not)"""

        if self.is_windows(helper, session) or helper.options.time_flag:
            # Windows will return the local time (not UTC),
            # so we need to use the local time to compare
            # Force this this if '-l' or '--localtime' is set in commandline
            local_timestamp = datetime.datetime.now()
            time_type = 'Remote (Local)'

        else:
            # usually the we need the UTC time
            local_timestamp = datetime.datetime.utcnow()
            time_type = 'Remote (UTC)'

        return local_timestamp, time_type

    @staticmethod
    def get_remote_timestamp(helper, session):
        """
        get the timestamp of the remote system
        """

        # get the remote time
        remote_time = helper.get_snmp_value_or_exit(session, helper, OID_TIME)

        # Extracting the remote time data from the OID
        # Value can be either 8 or 11 octets long

        if len(remote_time) == 11:
            # unpack returns: year(first octet)|year(second
            # octet)|month|day|hour|minute|second|deci-seconds|direction from UTC|hours from
            # UTC|minutes from UTC e.g.: 07|224|04|09|13|04|43|00|+|02|00 you have to convert the
            # first two octets to get the year e.g.: 0x07|0xE0 => 0x07=7, 0xE0=224 =>
            # 07*256=1792, 1762+224=2016
            remote_time = struct.unpack('BBBBBBBBcBB', remote_time)

        elif len(remote_time) == 8:
            # unpack returns: year|year|month|day|hour|minute|second|deci-seconds
            # e.g.:07|224|04|09|13|04|43|00 you have to convert the first two octets to get the
            # year e.g.: 0x07|0xE0 => 0x07=7, 0xE0=224 => 07*256=1792, 1762+224=2016
            remote_time = struct.unpack('BBBBBBBB', remote_time)

        else:
            helper.exit(summary='remote device does not return a time value', exit_code=unknown,
                        perfdata='')

        remote_time_year = (remote_time[0] * 256) + remote_time[1]  # year
        remote_time_month = remote_time[2]  # month
        remote_time_day = remote_time[3]  # day
        remote_time_hours = remote_time[4]  # hours
        remote_time_minutes = remote_time[5]  # minutes
        remote_time_seconds = remote_time[6]  # seconds

        # Format remote_time into timestamp
        remote_timestamp = datetime.datetime(remote_time_year, remote_time_month, remote_time_day,
                                             remote_time_hours,
                                             remote_time_minutes, remote_time_seconds)

        if len(remote_time) == 11:
            # in case we receive 11 values from unpack (depending on the remote device), we must
            # calculate the UTC time with the offset
            remote_time_utc_dir = remote_time[8]  # + or -
            remote_time_hours_offset = remote_time[9]  # offset to UTC hours
            remote_time_minutes_offset = remote_time[10]  # offset to UTC minutes

            # Calculate UTC-time from local-time
            if remote_time_utc_dir == '+':
                remote_timestamp -= datetime.timedelta(hours=remote_time_hours_offset,
                                                       minutes=remote_time_minutes_offset)

            elif remote_time_utc_dir == '-':
                remote_timestamp += datetime.timedelta(hours=remote_time_hours_offset,
                                                       minutes=remote_time_minutes_offset)

        return remote_timestamp

    def check_time(self, helper, session):
        """ check the time """

        remote_timestamp = self.get_remote_timestamp(helper, session)

        local_timestamp = self.get_local_timestamp(helper, session)[0]
        time_type = self.get_local_timestamp(helper, session)[1]

        # Calculate the offset between local and remote time
        offset = time.mktime(local_timestamp.timetuple()) \
                 - time.mktime(remote_timestamp.timetuple()) \
                 + 60 \
                 * helper.options.tzoffset

        helper.add_metric(label='offset', value=offset)

        helper.add_summary(
            '%s: ' % time_type + datetime.datetime.fromtimestamp(
                time.mktime(remote_timestamp.timetuple())).strftime(
                    '%H:%M:%S') + '. Offset = %d s' % offset)

        helper.add_long_output(
            '%s: ' % time_type + datetime.datetime.fromtimestamp(
                time.mktime(remote_timestamp.timetuple())).strftime(
                    '%Y.%m.%d %H:%M:%S'))
