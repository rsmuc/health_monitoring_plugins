## check_snmp_port.py:
---

Check the status of a tcp/udp port via SNMP. For TCP ports also the status is checked (e.g listen, established).

You could also use for example the check_tcp script. But check_tcp always trys to connect to the port, so we did see a lot of connects and disconncets in the logfile of our database service. And it is also not possible to check the connection status of the port.

If you know snmpnetstat, then you know how the plugin works.

The plugin requires pynag (https://github.com/pynag/pynag) and python-netsnmp.

### Defaults:

- OK:       established, listen
- WARNING:  synSent
- CRITICAL: closed

Possible values are: closed, listen, synSent, synReceived, established, finWait1, finWait2, closeWait, lastAck, closing, timeWait, deleteTCB

### Example:

#### Check TCP Port 80:   
```./check_snmp_port.py -H 192.168.2.1 -t tcp -p 80 -c established -o closed -w listen```
```
=> 
Warning - Current TCP status for port 80 is: listen
```

#### Check UDP Port 68:

```./check_snmp_port.py -H 192.168.2.1 -t udp -p 68```
```
=> 
Critical - Current UDP status for port 68 is: CLOSED
```
```
=> 
OK - Current UDP status for port 67 is: OPEN
```

#### Show all open UDP Ports:
`./check_snmp_port.py -H 192.168.2.1 -t udp -p scan`
```
=> 
All open UDP ports:
UDP: 	53
UDP: 	67
UDP: 	161
UDP: 	1900
UDP: 	5353
UDP: 	45669
UDP: 	5060
UDP: 	35678
UDP: 	45645
UDP: 	47921
UDP: 	48306
UDP: 	55330
```
#### Show all open TCP Ports:
`./check_snmp_port.py -H 192.168.2.1 -t tcp -p scan`
```
=> 
All open TCP ports:
TCP: 	53	 Status: 	listen
TCP: 	515	 Status: 	listen
TCP: 	49152	 Status: 	listen
TCP: 	49153	 Status: 	listen
TCP: 	49154	 Status: 	listen
TCP: 	49155	 Status: 	listen
TCP: 	25661	 Status: 	listen
TCP: 	80	 Status: 	listen
TCP: 	39990	 Status: 	listen
```
### Options
```
-  -h, --help            show this help message and exit
-  -H HOSTNAME           Hostname or ip address
-  --version=VERSION     SNMP version (default: 2)
-  --community=COMMUNITY  SNMP community (default: public)
-  -o OK                 ok values - (possible options: closed, listen,
                        synSent, synReceived, established, finWait1, finWait2,
                        closeWait, lastAck, closing, timeWait, deleteTCB)
-  -w WARNING            warning values
-  -c CRITICAL           critical vales
-  -t TYPE               TCP or UDP
-  -p PORT               The port you want to monitor ('scan' for scanning)
```

### Running the unit tests

To run the unittests for check_snmp_port.py:

    apt-get install python-pytest
    py.test unittest.py -v --capture=sys

It's required that SNMPv2 with read cmmunity public is enabled on the host, that runs the test

### TODO:
* Implement SNMPv3
* It should be possible to enter a list of ports that should be checked

