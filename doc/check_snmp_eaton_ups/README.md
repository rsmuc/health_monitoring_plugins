## check_snmp_eaton_ups.py:
---

Check state of an Eaton UPS.
The plugin checks various characteristics of an Eaton UPS. It gets an SNMP value according to 
the defined check type and compares the returned value against the set thresholds. 

Checkable values:
* input voltage, frequency
* output voltage, current, power, load
* time on battery
* remaining runtime
* remaining battery capacity
* alarms
* battery test summary and details
* battery state
* internal and environmental temperature

### Example:

#### Check remaining battery capacity

    ./check_snmp_eaton_ups.py -H 172.29.1.118 -t BATTERY_CAPACITY -w 20: -c 10:

=> 

OK - Remaining Battery Capacity 100 % | 'BATTERY_CAPACITY'=100%;20:;10:;;


    
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
                        One out of 
                        ON_BATTERY, REMAINING_BATTERY_TIME, INPUT_FREQUENCY,
                        INPUT_VOLTAGE, OUTPUT_VOLTAGE, OUTPUT_CURRENT,
                        OUTPUT_POWER, OUTPUT_LOAD, ALARMS,
                        BATTERY_TEST_SUMMARY, BATTERY_TEST_DETAIL,
                        BATTERY_CAPACITY, ENVIRONMENT_TEMPERATURE,
                        EXTERNAL_ENVIRONMENT_TEMPERATURE, BATTERY_LOW_WARNING,
                        BATTERY_REPLACEMENT_WARNING, BATTERY_FAULT_WARNING
  -w WARNING_THRESHOLDS Thresholds in icinga threshold range syntax
  -c CRITICAL_THRESHOLDS Thresholds in icinga threshold syntax
 ```
