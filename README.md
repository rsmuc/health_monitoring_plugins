# health monitoring plugins:
---

This is the main readme file for the health montiroing plugins project. In this project we pubish all our plugins we write for icinga / nagios.
In every single plugin folder, you will find a readme file, that describes the details of the plugin.

All plugins are released under the GPLv2.


## Plugins

- [check_meinberg_ntp](doc/check_meinberg_ntp/README.md)
- [check_moxa_6000](doc/check_moxa_6000/README.md)
- [check_snmp_ilo4](doc/check_snmp_ilo4/README.md)
- [check_snmp_large_storage](doc/check_snmp_large_storage/README.md)
- [check_snmp_port](doc/check_snmp_port/README.md)
- [check_nmp_raritan](doc/check_nmp_raritan/README.md)
- [check_snmp_service](doc/check_snmp_service/README.md)
- [check_snmp_time](doc/check_snmp_time/README.md)

A detailed description can be found in the README.md in folder of the corresponding plugin.

#### check_meinberg_ntp

Check the Meinberg NTP server LANTIME M300.

The plugin checks the current ntp and gps state, shows the current gps position and checks the good satellites.
Tested with firmware version 5.30 and 6.18 (NG).

#### check_moxa_6000

Check the status of a Moxa NPORT 6000 RS232 to LAN converter.  
You can check each port for the CTS, DSR, DTR and Error count.

#### check_snmp_ilo4

This plugin checks the health of HP servers with iLo 4 interface via SNMP.

The following components are checked:

- status of powersupply
- status of physical and logical drives (incl. drive temperatures)
- status of fans
- status of the temperature sensors
- the power state of the server (On or Off)
- status of the memory
- the global health status


#### check_snmp_large_storage

Check the used / free disk space of a device via SNMP (using the HOST-RESOURCES-MIB hrStorageSize).
There are already script doing that like http://nagios.manubulon.com/snmp_storage.html . But these check script have a big problem with large storage systems. 

In our case we want to monitor a Microsoft Windows Server 2012 R2 with an 10 TB partition and one Server with an 25 TB partition. The problem all scripts have, that the SNMP counter hrStorageSize is a 32 Bits
Integer counter. If you have a storage that is larger then 8 TB you will have the issue, that the conuter overruns and will return a negative integer value.

This script will handle the negative integer values and will calculate the proper size. That will only work if the counter overruns once.

#### check_snmp_port

Check the status of a tcp/udp port via SNMP. For TCP ports also the status is checked (e.g listen, established).

You could also use for example the check_tcp script. But check_tcp always trys to connect to the port, so we did see a lot of connects and disconncets in the logfile of our database service. And it is also not possible to check the connection status of the port.

If you know snmpnetstat, then you know how the plugin works.


#### check_snmp_raritan

Check a Raritan Dominition PX PDU (Power Distribution Unit):
* outlets (On, Off)
* inlet (Power, Current, Voltage)
* connected sensors

Tested device: PX2-2486  
Tested sensors: Temperature, Humidity, Contact Closure, Air Pressure


#### check_snmp_service

Icinga / Nagios plugin to check if a Windows service is in running state via SNMP.

It may take some time until Windows updates the status via snmp after starting or stopping a service.


#### check_snmp_time2

This plugin compares the time of the icinga/nagios machine with the time of a remote device.


## Installation

###  pip (recommended)

The complete plugin package is available at [PyPI](https://pypi.python.org/pypi/health_monitoring_plugins)

If your Linux machine is directly connected to the internet, you can use pip to install the package.
Just run:

    pip install health_monitoring_plugins
    
The plugins will be installed in your PATH. So the scripts can be executed directly.

If you are behind a firewall or not connected to the internet, you can download the tar.hz from PyPI and install it with

    health_monitoring_plugins-<version>.tar.gz
    
To uninstall the package you can run:

    pip uninstall health_monitoring_plugins

### setup.py

You can download the source package from [PyPI](https://pypi.python.org/pypi/health_monitoring_plugins)

To install the package from source with setup.py, you can run

    tar xfvz health_monitoring_plugins-<version>.tar.gz
    cd health_monitoring_plugins
    python setup.py install

### manual

You can download the source package from [PyPI](https://pypi.python.org/pypi/health_monitoring_plugins) or from [Github](https://github.com/rsmuc/health_monitoring_plugins)

You can copy each single check script in your plugins folder to install the plugins.
Ensure that you installed the pynag package.

## Run the unittests

To run the unittests just execute:

    python setup.py test

The unittests require pytest.

## Changelog

###### Version 0.0.2

* Added unittests for all plugins
* Fixed a bug in check_snmp_raritan Inlet check
* Cleaned up some parts of the code
* Better package structure

###### Version 0.0.1

* The first testing release including all developed check plugins

## TODO

* get_data and walk_data should be harmonized
* harmonized unittests for walk and get
* harmonize snmp settings
* Implement SNMPv3 support for all plugins
* fix --scan at check_ilo
* fix smart status for check_ilo
* fix redundancy status for check_ilo
* add a default threshold to check_snmp_time2
* check_snmp_time2: add leading 0 at the time
* Add examples for commands.cfg and service configuration
* Code cleanup