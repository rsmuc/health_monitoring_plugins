# check_snmp_time2.py

This plugin compares the time of the icinga/nagios machine with the time of a remote device.

The plugin requires [pynag] and python-netsnmp.


## Differences to check_snmp_time.pl

Up to now we used the check_snmp_time.pl plugin, but we had problems with the daylight saving time.

- does not need a reconfiguration for summer and wintertime anymore
- works for windows and linux installations 
- normally an offset is now unnecessary (so set --tzoffset to 0 or delete it) 
- warnings and criticals are now adapted to icinga standard 

## Options
```
  -h, --help            show this help message and exit
  -H                    Hostname or ip address
  -C, --community       SNMP community of the SNMP service on target host.
  -V, --snmpversion     SNMP version. (1 or 2)
  -o, --tzoffset        the local systems utc offset to the servers utc, in minutes (use only if your
                        remote device is in a different timezone)
  -l, --localtime       force to use local time (only recommended if you have a non Windows OS remote device,   
                        that returns localtime and not utc)
  --th, --threshold     threshold configuration for warning- and critical-threshold to the metric offset
```
#### Defaults
```
-C, --community         "public"
-V, --snmpversion       2
-o, --tzoffset          0
```

## Status
Plugin sets:
-  OK: offset <= [warning] seconds
- WARNING: [warning] seconds < offset <= [critical] seconds
- CRITICAL: [critical] seconds < offset   

> [critical] and [warning] can be modified with threshold-parameters on commandline   
> offset is applied to be an absolute value in this treatment

## Examples


#### check with custom warning and critical threshold
```
./check_snmp_time2.py -H 192.168.2.1 --th metric=offset,warning=-5:5,critical=-15:15 
```
Status is set to:   
WARNING:  offset is between 5 and 15 seconds or -5 and -15 seconds   
CRITICAL: offset is above 15 seconds or below -15 seconds


#### forced check with localtime 
```
./check_snmp_time2.py -H 192.168.2.1 -l
```
Not all devices return the time as UTC time. For example Windows return the local time.
With this parameter the script compares the time from the remote device, with the local time (instead of UTC) of the nagios/icinga machine.

   
#### return can look like this
```
OK - Offset = 0 s
```
or this
```
Critical - Critical on Offset. Offset = 720 s
```

## ToDo

 - Clean the names of some variables
 - Implement SNMPv3 
 - If you think, the check, if the remote device uses windows, is not elegant enough, you are welcome to serve me a better way 
 - Long term testing (still waiting for bugs)


   [pynag]:<https://github.com/pynag/pynag>
