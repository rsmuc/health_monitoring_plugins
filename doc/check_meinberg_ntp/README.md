## check_meinberg_ntp.py:
---

Check the Meinberg NTP server LANTIME M300.

The plugin checks the current ntp and gps state, shows the current gps position and checks the good satellites.
Tested with firmware version 5.30 and 6.18 (NG).

The plugin requires pynag (https://github.com/pynag/pynag) and python-netsnmp.


### Example:

#### Without threshold:

 ```./check_meinberg_ntp.py -H 172.29.1.118```
 
 ```=> 
OK - GPS Position: 48.1275 11.6126 623m. Good satellites: 10 | 'satellites'=10;;;;
 ```
#### With threshold:

 ```./check_meinberg_ntp.py -H 172.29.1.118 --threshold metric=satellites,warning=8:,critical=2:```
 ``` 
=> 
OK - GPS Position: 48.1275 11.6126 623m. Good satellites: 9 | 'satellites'=9;8:;2:;;
 ```
 ```./check_meinberg_ntp.py -H 172.29.1.118 --threshold metric=satellites,warning=15:,critical=11:```
 ```
=> 
Critical - GPS Position: 48.1275 11.6126 623m. Good satellites: 10. Critical on satellites | 'satellites'=10;15:;11:;;
 ```

#### Check a Meinberg timeserver M300 with firmware version 6 or newer:

 ```./check_meinberg_ntp.py -H 172.29.1.118 -m NG```

## Parameters
 ```
- -H HOSTNAME           Hostname or ip address
-  --version=VERSION     SNMP version (default: 2)
-  --community=COMMUNITY SNMP community (default: public)
-  -m MIB                Version of the MIB (NG = MBG-LANTIME-NG-MIB.mib) 
 ``` 

## TODO:
* Implement SNMPv3
