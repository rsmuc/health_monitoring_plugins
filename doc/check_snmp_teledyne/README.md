# check_snmp_teledyne.py
---

This plugin checks the health of Teledyn Paradise Datacom Sattelite Modem.

### Options
```
  -h, --help            show this help message and exit
  -H                    Hostname or ip address
  -C, --community       SNMP community of the SNMP service on target host.
  -V, --snmpversion     SNMP version. (1 or 2)
```
```

### Examples


    ./check_snmp_teledyne.py -H 172.29.1.2 

=>

    OK - Fault Summary: No Fault. Power Supply 1: No Fault. Power Supply 2: No Fault. RF Switch 1: No Fault. RF Switch 2: No Fault. Unit 1: No Fault. Unit 2: No Fault. Unit 3: No Fault
    Critical - Fault Summary: Fault. Power Supply 1: Fault. Power Supply 2: Fault. RF Switch 1: Fault. RF Switch 2: Fault. Unit 1: Fault. Unit 2: Fault. Unit 3: Fault
