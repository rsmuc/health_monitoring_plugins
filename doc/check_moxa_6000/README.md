## check_moxa_6000.py:
---

Check the status of a Moxa NPORT 6000 RS232 to LAN converter.

You can check each port for the CTS, DSR, DTR and Error count.

The plugin requires pynag (https://github.com/pynag/pynag) and python-netsnmp.


### Example:

#### Check Port 1:   
```./check_moxa_6000.py -H 192.168.2.12 -p 1```


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

