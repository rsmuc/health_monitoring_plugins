#/bin/bash
echo "Test check_snmp_large_storage"
py.test health_monitoring_plugins/check_snmp_large_storage/_unittest.py -v

#echo "Test check_snmp_time2"
#py.test health_monitoring_plugins/check_snmp_time2/_unittest.py -v

echo "Test check_snmp_service"
py.test health_monitoring_plugins/check_snmp_service/_unittest.py -v

echo "Test check_snmp_raritan"
py.test health_monitoring_plugins/check_snmp_raritan/_unittest.py -v

echo "Test check_snmp_port"
py.test health_monitoring_plugins/check_snmp_port/_unittest.py -v
