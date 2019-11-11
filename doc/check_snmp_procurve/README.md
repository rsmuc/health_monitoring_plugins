## check_snmp_procurve.py:
---

Check via SNMP if the sensors for an HP / Aruba Procurve Switch are in good condition. Usually the "Power Supply Sensor" and "Fan Sensor" is available.
The hpicfSensorTable is used to read all available sensors and their status. (MIB: hpicfchassis.mib)


### Example:

#### Failed Power Supply and failed FAN
```./check_snmp_procurve.py -H 192.168.2.1
```
=> 
Critical - Fan Sensor: bad. Power Supply 1 Sensor: good.
```

#### Everything OK
```./check_snmp_procurve.py -H 192.168.2.1
```
=> 
OK - Fan Sensor: good. Power Supply 1 Sensor: good.
```


### Options
```
-  -h, --help            show this help message and exit
-  -H HOSTNAME           Hostname or ip address
-  --version=VERSION     SNMP version (default: 2)
-  --community=COMMUNITY  SNMP community (default: public)
```
