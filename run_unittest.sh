#/bin/bash
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

echo "Test check_snmp_sencere"
py.test test/test_check_snmp_sencere.py -v

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