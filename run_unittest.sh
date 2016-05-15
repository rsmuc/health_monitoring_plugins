#/bin/bash

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
