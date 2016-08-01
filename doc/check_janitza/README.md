## check_janitza.py:
---

Check the status of a Janitza device.

You can check 'uL1', 'uL2', 'uL3', 'iL1', 'iL2', 'iL3', 'iL4', 'iL5', 'iL6', 'pL1', 'pL2', 'pL3', 'qL1', 'qL2', 'qL3',  
  'sL1', 'sL2', 'sL3', 'cosPL1', 'cosPL2', 'cosPL3', 'p3', 'q3', 's3', 'uL1L2', 'uL2L3', 'uL3L1'

The plugin requires pynag (https://github.com/pynag/pynag) and python-netsnmp.


### Example:

#### Get a list of all possible types
```./check_janitza.py -l```

#### Check uL1  with warning(-10:10) and critical(-20:20) metrics (pynag standard confirm):   
```./check_janitza.py -H 192.168.2.12 -t uL1 --th metric=type,warning=-10:10,critical=-20:20```

#### Check uL1 without pynag metrics:   
```./check_janitza.py -H 192.168.2.12 -t uL1```


## Options

-  -h, --help            show this help message and exit

-  -H HOSTNAME, --hostname=HOSTNAME
                        Host name or IP Adress of hte MOXA device.
-  -C COMMUNITY, --community=COMMUNITY
                        SNMP community of the SNMP service on target host.
-  -V SNMPVERSION, --snmpversion=SNMPVERSION
                        SNMP version.
-  -p PORT, --port=PORT  Moxa RS232 port number.
-  -t TYPE, --type=TYPE  Available check types: CTS, DSR, DTR, ErrorCount.
                        Example: -t CTS_ErrorCount.
                        CTS (Clear To Send): DCE (Data Communication
                        Equipment) is ready to accept data from the DTE (Data
                        Terminal Equipment).
                        DSR (Data Set Ready): DCE (Data Communication
                        Equipment) is ready to receive commands or data.
                        DTR (Data Terminal Ready): DTE (Data Terminal
                        Equipment) is ready to receive, initiate, or continue
                        a call.
                        ErrorCount = Show error counts of Frame, Break,
                        Overrun and Parity.
-  -c CRITICAL, --critical=CRITICAL
                        Return CRITICAL if any ErrorCount >= this parameter.
-  -w WARNING, --warning=WARNING
                        Return WARNING if any ErrorCount >= this parameter.


