# check_snmp_lband.py
---

This plugin checks the health of Teledyn Paradise Datacom Sattelite Modem.

### Options
```
-h, --help            show this help message and exit
  -H HOSTNAME           Hostname or ip address
  -C COMMUNITY, --community=COMMUNITY
                        SNMP community of the SNMP service on target host.
  -V VERSION, --snmpversion=VERSION
                        SNMP version. (1 or 2)
  -U UNIT, --unit=UNIT  Select the unit you want to monitor, if no unit is
                        selected both units will be monitored

```
```

### Examples


    ./check_snmp_lband.py -H 172.29.1.2 -U 1

=>

    Critical - Unit status is: Alarmed
    
