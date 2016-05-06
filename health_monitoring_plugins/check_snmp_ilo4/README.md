# check_snmp_ilo4.py


This plugin checks the health of HP servers with iLo 4 interface via SNMP.

The following components are checked:

- status of powersupply
- status of physical and logical drives (incl. drive temperatures)
- status of fans
- status of the temperature sensors
- the power state of the server (On or Off)
- status of the memory
- the global health status

The plugin currently does not provide performance data.

For older systems we use the check_ilo2_health.pl plugin. In our opinion the ilo2 plugin does have some disadvantages:

- a username and password for the iLo interface must be provided in the configuration
- the ilo2 plugin is using the xml interface of the ilo interface. The xml file is very large and that causes a lot of network traffic, and a high load on our icinga server. Additonally we had some crashes and timeouts of our old ilo2 interfaces, due to a too fast monitoring interval.

With iLo 4 HP introduced a real SNMP interface for iLo. The SNMP interface is able to get all relevant status information from the server. Including the hard drive status (was missing older iLOs)

Tested with:

- HP DL380 Gen8
- HP DL380 Gen9
- HP DL360p Gen8
- HP DL320e Gen8 v2

The plugin requires [pynag] and python-netsnmp.

## Options for check_snmp_ilo4.py
```
  -h, --help            show this help message and exit
  -H HOSTNAME           Hostname or ip address
  -C COMMUNITY, --community=COMMUNITY
                        SNMP community of the SNMP service on target host.
  -V VERSION, --snmpversion=VERSION
                        SNMP version. (1 or 2)
  -c AMOUNT_DRVS, --drives=AMOUNT_DRVS
                        Amount of physical drives. Requires an integer. (0 to
                        disable the check)
  -p AMOUNT_PWR_SPLY, --ps=AMOUNT_PWR_SPLY
                        Amount of connected power supplies. Requires an
                        integer. (0 to disable the check)
  -f AMOUNT_FANS, --fan=AMOUNT_FANS
                        Amount of fans. Requires an integer. (0 to disable the
                        check)
  --scan                Scan the server if you do not know what is build in
                        (does not return a health status)
  --noStorage           Do not check global storage condition
  --noSystem            Do not check global system state
  --noPowerSupply       Do not check global power supply condition
  --noPowerState        Do not check power state
  --noTemp              Do not check global temperature condition
  --noTempSens          Do not check temperature sensor condition
  --noDriveTemp         Do not check temperature sensor of the hard drives
  --noFan               Do not check global fan condition
  --noMemory            Do not check memory condition
  --noController        Do not check controller condition


      
```

#### Defaults
```
-C, --community         "public"
-V, --snmpversion       2
```


## Examples

### Normal check:
```
./check_snmp_ilo4.py -H 192.168.2.1 --fan 2 --ps 1 --drives 4
```

In this case we excpect that the server does have two fans, one power supply and four hard drives.
The script requires that you enter the correct amount of components. We decided to rely not only on the status of the component, we also want to count the components.
We had one server where a fan was completely dead. So it even did not report a degraded status. It was just completely missing.


```
OK - HP-Server0815  - Serial number:AB1234567C
Global storage status: ok

Global system status: ok

Global power supply status: ok

Server power status: poweredOn

Overall thermal environment status: ok

Temperature sensors status: ok

Fan(s) status: ok

Memory status: ok

Controller 0 status: ok
Controller 1 status: ok

Physical drive 0: ok
Physical drive 1: ok

Temperature of physical drive 0: 35 Celsius (threshold: 60 Celsius)
Temperature of physical drive 1: 33 Celsius (threshold: 60 Celsius)

Logical drive 0 status: ok

Power supply 0: ok

Temperature 0: 22 Celsius (threshold: 42 Celsius)
Temperature 1: 40 Celsius (threshold: 70 Celsius)
Temperature 2: 27 Celsius (threshold: 87 Celsius)
Temperature 3: 35 Celsius (threshold: 60 Celsius)
Temperature 4: 48 Celsius (threshold: 105 Celsius)
Temperature 5: 36 Celsius (threshold: 115 Celsius)
Temperature 6: 28 Celsius (threshold: 65 Celsius)
Temperature 7: 52 Celsius (threshold: 77 Celsius)
Temperature 8: 53 Celsius (threshold: 100 Celsius)
Temperature 9: 42 Celsius (threshold: 68 Celsius)
Temperature 10: 86 Celsius (threshold: 100 Celsius)
Temperature 11: 41 Celsius (threshold: 69 Celsius)
Temperature 12: 44 Celsius (threshold: 73 Celsius)
Temperature 13: 33 Celsius (threshold: 68 Celsius)
Temperature 14: 42 Celsius (threshold: 67 Celsius)

Fan 0: ok
Fan 1: ok
Fan 2: ok
```


### Disable several checks
```
./check_snmp_ilo4.py -H 192.168.2.1 --fan 0 --ps 0 --drives 0 --noSystem --noPowerSupply
```

In this case we don't check the fans, the power supply, the drives, the global system status and the global power supply status.

We added these parameters because some of out HP DL380 G9 report a degraded power supply status, but everything is fine. In this case only one power supply is installed.

    
### Scan
```
./check_snmp_ilo4.py -H 192.168.2.1 --scan 
```

With the scan option you can check how many components are found.



```
Unknown - HP-Server0815  - Serial number:AB1234567C. This is not a health status!
Physical drive 0: ok
Physical drive 1: ok

Power supply 0: ok

Fan 0: ok
Fan 1: ok
Fan 2: ok
```

## ToDo
 - Implement SNMPv3 
 - Code cleanup

  
 

   [pynag]:<https://github.com/pynag/pynag>
