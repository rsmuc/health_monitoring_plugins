"""
Module for cambium
"""
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

from pynag.Plugins import unknown, warning, critical

# OIDS
CONNECTION_OIDS = {
    "search_state": '.1.3.6.1.4.1.17713.9.12.16.0'
}


# STATES

SEARCH_STATE = {
    0: 'registering / connected',
    1: 'searching / not connected',
    2: 'acquiring / connecting'
}

class PTP700(object):

    def __init__(self, session):
        self.sess = session

    @staticmethod
    def get_connection_info(helper, session):
        """ get the infos for the connection """

        value = helper.get_snmp_values_or_exit(session, helper, CONNECTION_OIDS["search_state"])[0]
        try:
            value = int(value)
        except:
            return "N//A"

        status = SEARCH_STATE.get(value, "N/A")
                
        return status


    def process_connection_status(self, helper, session):
        """
        check the status of the connection
        """

        search_state = self.get_connection_info(helper, session)               

        helper.add_summary("Radio is {}".format(search_state))

        if search_state != "registering / connected":
            helper.status(critical)