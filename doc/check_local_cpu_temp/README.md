## check_local_cpu_temp.py:
---

Check the local CPU temperature without the usage of "lm-sensors"

The plugin requires pynag (https://github.com/pynag/pynag) and python-netsnmp.

The plugins is able to check the CPU temperature without dependencies to lm-sensors. The check-lm-sensors plugin stopped working for us with the migration to Debian 9.


### Example:

#### CPU Temperature

Reading the temperature from /sys/class/thermal/thermal_zone0/temp


```./check_local_cpu_temp.py -C temp1 --threshold metric=temp,warning=:15,critical=:25```
```
```
=> 
Critical - CPU temperature: 26.8 C. Critical on temp | 'cpu'=26.8;:50;:25;;
```

#### Core temperature

Reading the temperature from /sys/devices/platform/coretemp.0/hwmon/hwmon1/temp2_input

For Core 1: -C "Core 0"
For Core 3: -C "Core 2"

```./check_local_cpu_temp.py -C "Core 0" --threshold metric=temp,warning=:50,critical=:95```
```
```
=> 
OK - Core 0 temperature: 42.0 C | 'temp'=42.0;:50;:95;;
```


### Options
```
 -h, --help            show this help message and exit
 
  -C                    check the component (temp1, "Core 0", "Core 1", "Core x")

```