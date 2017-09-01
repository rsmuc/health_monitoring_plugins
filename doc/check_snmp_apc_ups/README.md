## check_snmp_apc_ups.py
---

Check state of a Schneider APC UPS:
The plugin checks various characteristics of an APC UPS. It gets an SNMP value according to 
the defined check type and compares the returned value against the set thresholds. 

Checkable values:
* input voltage, frequency
* output voltage, current, power, load
* remaining runtime
* remaining battery capacity
* battery state
* environmental temperature

Tested device: None. Just simulated with a snmpwalk of a "Smart-UPS RT 3000 XL"

### Example:

#### Check Input Voltage

    ./check_snmp_apc_ups.py -H 172.29.1.2 -t INPUT_VOLTAGE -w 228:232 -c 226:234
 
=> 

Critical - Input Voltage is 114 VAC | 'INPUT_VOLTAGE'=114VAC;228:232;226:234;;
    

## Parameters
 ```
Options:
  -h, --help            show this help message and exit
  -H HOSTNAME           Hostname or ip address
  -C COMMUNITY, --community=COMMUNITY
                        SNMP community of the SNMP service on target host.
  -V VERSION, --snmpversion=VERSION
                        SNMP version. (1 or 2)
  -t CHECKTYPE          The value you want to monitor 
                        One out of BASIC_BATTERY_STATUS, TIME_ON_BATTERY,
                        BATTERY_CAPACITY, INTERNAL_TEMPERATURE,
                        RUNTIME_REMAINING, BATTERY_REPLACE_INDICATOR,
                        INPUT_VOLTAGE, INPUT_FREQUENCY, OUTPUT_VOLTAGE,
                        OUTPUT_LOAD, OUTPUT_CURRENT, OUTPUT_POWER,
                        LAST_TEST_RESULT, ENVIRONMENT_TEMPERATURE
  -w WARNING_THRESHOLDS Thresholds in icinga threshold range syntax
  -c CRITICAL_THRESHOLDS Thresholds in icinga threshold syntax
 ```