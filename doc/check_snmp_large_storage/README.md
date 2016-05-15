
# check_snmp_large_storage.py:
---

Check the used / free disk space of a device via SNMP (using the HOST-RESOURCES-MIB hrStorageSize).
There are already script doing that like http://nagios.manubulon.com/snmp_storage.html . But these check script have a big problem with large storage systems. 

In our case we want to monitor a Microsoft Windows Server 2012 R2 with an 10 TB partition and one Server with an 25 TB partition. The problem all scripts have, that the SNMP counter hrStorageSize is a 32 Bits
Integer counter. If you have a storage that is larger then 8 TB you will have the issue, that the conuter overruns and will return a negative integer value.

This script will handle the negative integer values and will calculate the proper size. That will only work if the counter overruns once.

The plugin requires pynag (https://github.com/pynag/pynag) and python-netsnmp.

### Calculation example
``` 
hrStorageAllocationUnits        => 8192 (this value is depending on your file system configuration)
hrStorageSize                   => -1149438977 (32Bit overrun)
Maximum possible integer value  => (2^32 / 2) - 1 = 2147483647
Real Storage Size               => (1149438977 + 2147483647) * 8192 = 27008390135808 Bytes
Real Storage Size in GB         => 27008390135808 Bytes / 1024 / 1024 / 1024 = 25153,52 GB
``` 


### Example:

#### Check without threshold:   
``` 
./check_snmp_large_storage.py -H 192.168.2.1 -d "E" -u TB 
``` 

``` 
=> 
OK - 38.82% used (9.54TB of 24.56TB) at E:\ Label:NAS  Serial Number e95e16d | 'percent used'=38.82;;;;
``` 

#### Check with threshold:
 
``` 
./check_snmp_large_storage.py -H 192.168.2.1 -d "E" -u TB  --threshold metric="percent used",warning=10..inf,critical=95..inf```
``` 

``` 
=> 
Critical - 38.82% used (9.54TB of 24.56TB) at E:\ Label:NAS  Serial Number e95e1f. Critical on percent used | 'percent used'=38.82;~:10;~:15;;
``` 

#### Show all available drive names:
`./check_snmp_large_storage.py -H 192.168.2.1 -d scan

### Options
```
  -h, --help            show this help message and exit
  -H HOSTNAME           Hostname or ip address
  -C COMMUNITY, --community=COMMUNITY
                        SNMP community of the SNMP service on target host.
  -V VERSION, --snmpversion=VERSION
                        SNMP version. (1 or 2)
  -p PARTITION, --partition=PARTITION
                        The disk / partition you want to monitor (scan for
                        scanning)
  -u TARGETUNIT, --unit=TARGETUNIT
                        The unit you want to have (MB, GB, TB)

```

### TODO:
* Implement SNMPv3
* It should be possible to enter a list of disks that should be checked

