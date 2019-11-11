## check_snmp_eaton_ups.py:

---

Check state of an Eaton UPS.
The plugin checks various characteristics of an Eaton UPS. It gets a SNMP value according to 
the defined check type and compares the returned value against the set thresholds. 

Checkable values:

* input voltage, frequency
* output voltage, current, power, load
* time on battery
* remaining runtime
* remaining battery capacity
* alarms
* ~~battery test summary and details (not available for Eaton 9SX)~~
* ~~battery state (low, replacement, fault) (not available for Eaton 9SX)~~
* internal and environmental temperature

### Example:

#### Check remaining battery capacity

    ./check_snmp_eaton_ups.py -H 172.29.1.118 -t battery_capacity --threshold metric=battery_capacity,warning=20:,critical=10:

=> 

OK - Remaining Battery Capacity 100 % | 'battery_capacity'=100%;20:;10:;;

#### Check UPS alarms

```
./check_snmp_eaton_ups.py -H 172.29.1.118 -t alarms
```

=>

OK - 0 active alarms

## Parameters

```
 Options:
  -h, --help            show this help message and exit
  -H HOSTNAME           Hostname or ip address
  -C COMMUNITY, --community=COMMUNITY
                        SNMP community of the SNMP service on target host.
  -V VERSION, --snmpversion=VERSION
                        SNMP version. (1, 2 or 3)
  -t TYPE, --type=TYPE  Check type to execute. Available types are:
                        on_battery, remaining_battery_time, input_frequency,
                        input_voltage, output_voltage, output_current,
                        output_power, output_load, alarms, battery_capacity,
                        environment_temperature,
                        external_environment_temperature
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
    --legacy            Deprecated, do not use

```
