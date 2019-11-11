## check_snmp_ubiquiti.py:

Check the status of a Ubiquiti device.

You can check the

- Uptime
- Signal Strength
- CPU usage (1 Minute Average)
- CPU usage (5 Minute Average)
- CPU usage (15 Minute Average)
- Total memory
- Free memory
- Tx Rate
- Rx Rate
The plugin requires pynag (https://github.com/pynag/pynag) and python-netsnmp.

Example:

Get a list of all possible types
```
./check_ubiquiti.py -l
```
Check uL1 with warning(-10:10) and critical(-20:20) metrics (pynag standard confirm):
```
./check_ubiquiti.py -H 192.168.2.12 -t up --th metric=type,warning=-10:10,critical=-20:20
```
Check uL1 without pynag metrics:
```
./check_ubiquiti.py -H 192.168.2.12 -t up
```
Options
```
-h, --help show this help message and exit 
-l, --list lists all possible request types 
-H HOSTNAME, --hostname=HOSTNAME Host name or IP Adress of hte MOXA device. 
-C COMMUNITY, --community=COMMUNITY SNMP community of the SNMP service on target host. 
-V SNMPVERSION, --snmpversion=SNMPVERSION SNMP version. 
-t TYPE, --type=TYPE type of the request 
--th metric=type,warning=WARNING_MIN:WARNING_MAX,critical=CRITICAL_MIN:CRITICAL_MAX add warning and critical values pynag confirm
```
