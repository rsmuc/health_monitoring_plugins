## check_snmp_fortinet.py:
---

Check the status a fortinet wificontroller.

The plugin requires pynag (https://github.com/pynag/pynag) and python-netsnmp.

The plugin can check the ressources of the controller (hard drive usage, cpu usage and memory usage). For the ressources there is a definied limit of 90%.
The second option is to check the status of the controller (operational state, alarm state and availability state).
The third option is to check ALL connected access points (operational state, alarm state and availability state). Only failed access points will be shown in the summary. In the long output all connected access points are shown.


### Example:

#### Check the connected accesspoints:
```./check_snmp_fortinet.py -H 172.29.10.110 --type accesspoints```
```
```
=> 
Critical - Access Points Status. ApTest1 Operational State: disabled. ApTest1 Availability State: not installed

AP-1 - Operational: enabled - Availabilty: online - Alarm: no alarm
ApTest1 - Operational: disabled - Availabilty: not installed - Alarm: no alarm
```

#### Check the ressources of the controller:

```./check_snmp_fortinet.py -H 172.29.10.110 --type ressources```
```
=> 
OK - Controller Status | 'CPU'=1%%;0:90;0:90;; 'Memory'=9%%;0:90;0:90;; 'Filesystem'=6%%;0:90;0:90;;

Controller Ressources - CPU: 1%
Memory: 9%
Filesystem: 6%
```


#### Check the controller Status:
```/check_snmp_fortinet.py -H 172.29.10.110 --type controller```
```
=>
OK - Controller Status

Controller Operational State: enabled
Controller Availability State: online
Controller Alarm State: no alarm
```
```
### Options
```
-  -h, --help            show this help message and exit
-  -H HOSTNAME           Hostname or ip address
-  -C COMMUNITY, --community=COMMUNITY
                        SNMP community of the SNMP service on target host.
-  -V VERSION, --snmpversion=VERSION
                        SNMP version. (1 or 2)
-  -t TYPE, --type=TYPE  Check type to execute. Available types are:
                        ressources, controller, accesspoints
```