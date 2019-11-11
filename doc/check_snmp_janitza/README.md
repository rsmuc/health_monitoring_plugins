## check_snmp_janitza.py:
---

Check the status of a Janitza 604 device.

You can check 'uL1', 'uL2', 'uL3', 'iL1', 'iL2', 'iL3', 'iL4', 'iL5', 'iL6', 'pL1', 'pL2', 'pL3', 'qL1', 'qL2', 'qL3',  
  'sL1', 'sL2', 'sL3', 'cosPL1', 'cosPL2', 'cosPL3', 'p3', 'q3', 's3', 'uL1L2', 'uL2L3', 'uL3L1'

The plugin requires pynag (https://github.com/pynag/pynag) and python-netsnmp.


### Example:

#### Get a list of all possible types
```./check_snmp_janitza.py -l```

#### Check uL1  with warning(-10:10) and critical(-20:20) metrics (pynag standard confirm):   
```./check_snmp_janitza.py -H 192.168.2.12 -t uL1 --th metric=type,warning=-10:10,critical=-20:20```

#### Check uL1 without pynag metrics:   
```./check_snmp_janitza.py -H 192.168.2.12 -t uL1```


## Options

-  -h, --help            show this help message and exit
-  -l, --list             lists all possible request types
-  -H HOSTNAME, --hostname=HOSTNAME
                        Host name or IP Adress of hte MOXA device.
-  -C COMMUNITY, --community=COMMUNITY
                        SNMP community of the SNMP service on target host.
-  -V SNMPVERSION, --snmpversion=SNMPVERSION
                        SNMP version.
-  -t TYPE, --type=TYPE      type of the request 
-  --th metric=type,warning=WARNING_MIN:WARNING_MAX,critical=CRITICAL_MIN:CRITICAL_MAX
                       add warning and critical values pynag confirm 


