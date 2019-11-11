# check_snmp_idrac.py

This plugin checks the health of Dell iDRAC.

The following components/statuses are checked:

- global system status
- system LCD status
- global storage status
- system power status
- power unit and its redundancy
- chassis intrusion sensor
- cooling unit
- temperature probes

The plugin requires [pynag]

## Options for check_snmp_idrac.py
```
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname=HOSTNAME
                        Hostname or ip address
  -C COMMUNITY, --community=COMMUNITY
                        SNMP community of the SNMP service on target host.
  -V SNMPVERSION, --snmpversion=SNMPVERSION
                        SNMP version. (1 or 2)
  --retries=RETRIES     Number of SNMP retries.
  --snmptimeout=SNMPTIMEOUT
                        The timeout for one snmp get (Default: 5 seconds)
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
  --no-system           Do not check the global system status
  --no-power            Do not check the power status
  --no-storage          Do not check the storage status
  --no-disks            Do not check the disks
  --no-predictive       Do not check the predictive status of the disks
  --no-lcd              Do not check the lcd status
  --no-power_unit       Do not check the power unit
  --no-redundancy       Do not check the power unit redundancy
  --no-intrusion        Do not check the intrusion sensor
  --no-cooling          Do not check the cooling unit
  --no-temperature      Do not check the temperature


```

#### Defaults
```
-C, --community         "public"
-V, --snmpversion       2
```

## Example

```
./check_snmp_idrac.py -H 192.168.2.1
```

Output should look like this:
```
OK - User assigned name: Main System Chassis - Typ: PowerEdge R420xr - Service tag: 1AB2345
Global System status: ok

System LCD status: ok

Global Storage status: ok

System Power status: on

Power unit "System Board PS" status: ok. Redundancy: full

Chassis intrusion sensor "System Board Intrusion" is ok

Cooling unit "System Board Fan" status: ok

Temperature probe at "System Board Inlet" is ok
```

## SNMPv3 Example:

```
./check_snmp_idrac/check_snmp_idrac.py -H 172.29.12.130 -V 3 -u snmpuser -l AuthPriv -a SHA -A snmppassword -x AES -X snmppassword
```

## Troubleshooting:

```
Unknown - No response from device for drive (.1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.4)

````

If you receive a no response message, the idrac interface does not respond to the snmp request.
Just disable the dedicated check: In this case use --no-disk option.



   [pynag]:<https://github.com/pynag/pynag>
