## check_snmp_service.py:
---

Icinga / Nagios plugin to check if a Windows service is in running state via SNMP.

It may take some time until Windows updates the status via snmp after starting or stopping a service.

The plugin requires pynag (https://github.com/pynag/pynag) and python-netsnmp.

### Example:

#### Check service "Windows Connection Manager":   
`./check_snmp_service.py -H 192.168.2.1 -s "Windows Connection Manager"`

=> 
`OK - Status of Service 'Windows Connection Manager' is: RUNNING`

=> `Critical - Status of Service 'Windows Connection Manager' is: NOT RUNNING`

#### Show all running services:
`./check_snmp_service.py -H 192.168.2.1 -s scan`

### Options:

```
-  -h, --help            show this help message and exit
-  -H HOSTNAME           Hostname or ip address
-  --version=VERSION     SNMP version (default: 2)
-  --community=COMMUNITY  SNMP community (default: public)
-  -s Service            The name of the service that should be monitored ("scan" for showing all available services)
```

### TODO:
* Implement SNMPv3
* Use the netsnmp function to convert the name of the service to a OID
