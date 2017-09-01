# check_snmp_idrac.py

This plugin checks the health of Dell iDRAC.

The following components/statuses are checked:

- global system status
- system LCD status
- global storage status
- system power status
- power unit and its redundancy
- chassis intrusion sensor
- cooling unit
- temperature probes

The plugin requires [pynag]

## Options for check_snmp_idrac.py
```
  -h, --help            show this help message and exit
  -H HOSTNAME           Hostname or ip address
  -C COMMUNITY, --community=COMMUNITY
                        SNMP community of the SNMP service on target host.
  -V VERSION, --snmpversion=VERSION
                        SNMP version. (1 or 2)
```

#### Defaults
```
-C, --community         "public"
-V, --snmpversion       2
```

## Example

```
./check_snmp_idrac.py -H 192.168.2.1
```

Output should look like this:
```
OK - User assigned name: Main System Chassis - Typ: PowerEdge R420xr - Service tag: 1AB2345
Global System status: ok

System LCD status: ok

Global Storage status: ok

System Power status: on

Power unit "System Board PS" status: ok. Redundancy: full

Chassis intrusion sensor "System Board Intrusion" is ok

Cooling unit "System Board Fan" status: ok

Temperature probe at "System Board Inlet" is ok
```



   [pynag]:<https://github.com/pynag/pynag>
