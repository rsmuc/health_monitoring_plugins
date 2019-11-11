## check_snmp_eps_plus.py:

---

Check state of an ePowerSwitch (8XM+)
This plugin is able to check the analog sensors (Temperature and Humidity) and the status of the outlets

### Example:

#### Check the first outlet of the master

    ./check_snmp_eps_plus.py -H 172.1.2.3 --device 0 --outlet 0

=> 

OK - SYS0X-EPS-M01 - SYS0X-Outlet1: On


#### Check the Temperature Sensor

```
./check_snmp_eps_plus.py -H 172.1.2.3 --sensor T1 --threshold metric="temperature sensor (in deg. c)",warning=:20,critical=:30
```

=>

Warning - TEMPERATURE SENSOR: 23 deg. C. Warning on temperature sensor (in deg. c) | 'temperature sensor (in deg. c)'=23;:20;:30;;

## Parameters

```
 Options:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname=HOSTNAME
                        Hostname or ip address
  -C COMMUNITY, --community=COMMUNITY
                        SNMP community of the SNMP service on target host.
  -V SNMPVERSION, --snmpversion=SNMPVERSION
                        SNMP version. (1 or 2)
  --retries=RETRIES     Number of SNMP retries.
  -U SECNAME, --securityname=SECNAME
                        SNMPv3: security name (e.g. bert)
  -L SECLEVEL, --securitylevel=SECLEVEL
                        SNMPv3: security level (noAuthNoPriv, authNoPriv,
                        authPriv)
  -a AUTHPROTO, --authprotocol=AUTHPROTO
                        SNMPv3: authentication protocol (MD5|SHA)
  -A AUTHPASS, --authpass=AUTHPASS
                        SNMPv3: authentication protocol pass phrase
  -x PRIVPROTO, --privproto=PRIVPROTO
                        SNMPv3: privacy protocol (DES|AES)
  -X PRIVPASS, --privpass=PRIVPASS
                        SNMPv3: privacy protocol pass phrase
  --device=DEVICE       Select the device whose outlet shall be monitored (0 =
                        master, 1 = first slave, 2 = second slave)
  --expected=EXPECTED   Define if On or Off shall be the OK sate (On, Off)
  --outlet=OUTLET       Select the outlet which shall be monitored (0 = first
                        outlet)
  --sensor=SENSOR       Select the sensor which shall be monitored (T1, T2,
                        Tx, H1, H2, Hx)

  Generic Options:
    --timeout=50        Exit plugin with unknown status after x seconds
    --threshold=range   Thresholds in standard nagios threshold format
    --th=range          Same as --threshold
    --extra-opts=@file  Read options from an ini file. See
                        http://nagiosplugins.org/extra-opts
    -d, --debug         Print debug info

  Display Options:
    -v, --verbose       Print more verbose info
    --no-perfdata       Dont show any performance data
    --no-longoutput     Hide longoutput from the plugin output (i.e. only
                        display first line of the output)
    --no-summary        Hide summary from plugin output
    --get-metrics       Print all available metrics and exit (can be combined
                        with --verbose)
    --legacy            Deprecated, do not us

```
