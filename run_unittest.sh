#/bin/bash

# ok
echo "Test check_meinberg_ntp"
py.test health_monitoring_plugins/check_meinberg_ntp/_unittest.py -v

# fehlt
#echo "Test check_snmp_time2"
#py.test health_monitoring_plugins/check_snmp_time2/_unittest.py -v

# fehlt
#echo "Test check_moxa_6000"
#py.test health_monitoring_plugins/check_moxa_6000/_unittest.py -v

# fehlt
#echo "Test check_snmp_ilo4"
#py.test health_monitoring_plugins/check_snmp_ilo4/_unittest.py -v

# ok
#echo "Test check_snmp_large_storage"
#py.test health_monitoring_plugins/check_snmp_large_storage/_unittest.py -v

# ok
#echo "Test check_snmp_service"
#py.test health_monitoring_plugins/check_snmp_service/_unittest.py -v

# ok
#echo "Test check_snmp_raritan"
#py.test health_monitoring_plugins/check_snmp_raritan/_unittest.py -v

# ok
#echo "Test check_snmp_port"
#py.test health_monitoring_plugins/check_snmp_port/_unittest.py -v
