# check_snmp_raritan.py
---

Check a Raritan Dominition PX PDU (Power Distribution Unit):
    * the outlets (On, Off)
    * the inlet (Power, Current, Voltage)
    * and the connected sensors

* Tested device: PX2-2486
* Tested sensors: Temperature, Humidity, Contact Closure, Air Pressure

The plugin requires pynag (https://github.com/pynag/pynag) and python-netsnmp.


### Example:

#### Check the Inlet Power:

 ```./check_snmp_raritan.py -H 172.29.1.2 -t inlet```
 
 ```=> 
 OK - Inlet. 5.1 A. 230.0 V. 1118.0 W. 1165.0 VA. 0.96. 6904491.0 Wh | 'A'=5.1A;10.4;12.8;; 'V'=230.0V;247.0;254.0;; 'W'=1118.0W;0.0;0.0;; 'VA'=1165.0VA;0.0;0.0;; ''=0.96;0.0;0.0;; 'Wh'=6904491.0Wh;0.0;0.0;;
  ```
#### Monitor Sensor with ID 1:

 ```./check_snmp_raritan.py -H 172.29.1.2 -t sensor -i 1```

 ``` 
=> Critical - Sensor 4 - 'On/Off 1'  is: alarmed

=> OK - Sensor 4 - 'Humidity 1' 18.0% is: normal | 'Humidity 1'=18.0%;70.0;80.0;;

 ```


#### Monitor Outlet with ID 3:

 ```./check_snmp_raritan.py -H 172.29.1.2 -t outlet -i 3```

```
Critical - Outlet 3 - 'Switch HP' is: OFF
```

## Parameters
 ```
Options:
  -h, --help            show this help message and exit
  -H HOSTNAME           Hostname or ip address
  -C COMMUNITY, --community=COMMUNITY
                        SNMP community of the SNMP service on target host.
  -V VERSION, --snmpversion=VERSION
                        SNMP version. (1 or 2)
  -t TYP                The type you want to monitor (inlet, outlet, sensor)
  -i ID                 The id of the outlet / sensor you want to monitor
                        (1-99)
 ``` 

## TODO:
* Implement SNMPv3
* Maybe it should be possible to monitor all services / sensors in one check
* Cleanup the code (don't mix string and int compares)