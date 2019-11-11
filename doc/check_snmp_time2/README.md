# check_snmp_time2.py
---

This plugin compares the time of the icinga/nagios machine with the time of a remote device.

### Differences to check_snmp_time.pl

Up to now we used the check_snmp_time.pl plugin, but we had problems with the daylight saving time.

- does not need a reconfiguration for summer and wintertime anymore
- works for windows and linux installations 
- normally an offset is now unnecessary (so set --tzoffset to 0 or delete it) 
- warnings and criticals are now adapted to icinga standard 

### Options
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

### Examples


#### check with custom warning and critical threshold

    ./check_snmp_time2.py -H 192.168.2.1 --th metric=offset,warning=-5:5,critical=-15:15 

=>

    OK - Remote UTC: 20:23:49. Offset = 0 s | 'offset'=0.0s;;;;


#### forced check with localtime 

    ./check_snmp_time2.py -H 192.168.2.1 -l

Not all devices return the time as UTC time. For example Windows return the local time.
With this parameter the script compares the time from the remote device, with the local time (instead of UTC) of the nagios/icinga machine.

