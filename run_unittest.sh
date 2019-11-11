#/bin/bash

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
#    along with Foobar.  If not, see <https://www.gnu.org/licenses/>.

# exit after error
set -e
set -x

echo "Test check_snmp_time2"
py.test test/test_check_snmp_time2.py -v

echo "Test check_meinberg_ntp"
py.test test/test_check_meinberg_ntp.py -v

echo "Test check_moxa_6000"
py.test test/test_check_moxa_6000.py -v

echo "Test check_snmp_ilo4"
py.test test/test_check_snmp_ilo4.py -v

echo "Test check_snmp_large_storage"
py.test test/test_check_snmp_large_storage.py -v

echo "Test check_snmp_service"
py.test test/test_check_snmp_service.py -v

echo "Test check_snmp_raritan"
py.test test/test_check_snmp_raritan.py -v

echo "Test check_snmp_port"
py.test test/test_check_snmp_port.py -v

echo "Test check_snmp_idrac"
py.test test/test_check_snmp_idrac.py -v

echo "Test check_snmp_teledyne"
py.test test/test_check_snmp_teledyne.py -v

echo "Test check_snmp_janitza"
py.test test/test_check_snmp_janitza.py -v

echo "Test check_snmp_ubiquiti"
py.test test/test_check_snmp_ubiquiti.py -v

echo "Test check_snmp_lband"
py.test test/test_check_snmp_lband.py -v

echo "Test check_snmp_apc_ups"
py.test test/test_check_snmp_apc_ups.py -v

echo "Test check_snmp_eaton_ups"
py.test test/test_check_snmp_eaton_ups.py -v

echo "Test check_snmp_procurve"
py.test test/test_check_snmp_procurve.py -v

echo "Test check_snmp_fortinet"
py.test test/test_check_snmp_fortinet.py -v

echo "Test check_snmp_trusted_filter"
py.test test/test_check_snmp_trusted_filter.py -v

echo "Test check_snmp_eps_plus"
py.test test/test_check_snmp_eps_plus.py -v

echo "Test check_newtecmodem"
py.test test/test_check_newtecmodem.py -v

echo "Test check_microwavemodem"
py.test test/test_check_microwavemodem.py -v

echo "Test check_cambium_ptp700"
py.test test/test_check_smmp_cambium_ptp700.py -v