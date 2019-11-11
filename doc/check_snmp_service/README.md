# check_snmp_service.py:
---

Icinga / Nagios plugin to check if a Windows service is in running state via SNMP.

It may take some time until Windows updates the status via snmp after starting or stopping a service.

The plugin requires pynag (https://github.com/pynag/pynag) and python-netsnmp.

### Example:

#### Check service "Windows Connection Manager":   
    
    ./check_snmp_service.py -H 192.168.2.1 -s "Windows Connection Manager"

=>

    OK - Status of Service 'Windows Connection Manager' is: RUNNING

=>

    Critical - Status of Service 'Windows Connection Manager' is: NOT RUNNING

#### Show all running services:

    ./check_snmp_service.py -H 192.168.2.1 -S

### Options:

```
  -h, --help            show this help message and exit
  -H HOSTNAME           Hostname or ip address
  -C COMMUNITY, --community=COMMUNITY
                        SNMP community of the SNMP service on target host.
  -V VERSION, --snmpversion=VERSION
                        SNMP version. (1 or 2)
  -s SERVICE            The name of the service you want to monitor (-s scan
                        for scanning)
  -S, --scan            Show all available services
```