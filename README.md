# health monitoring plugins:
---

This is the main readme file for the health montiroing plugins project. In this project we pubish all our plugins we write for icinga / nagios.
The plugins are provided on pypi as python package.

All plugins are released under the GPLv2.

[![Code Health](https://landscape.io/github/rsmuc/health_monitoring_plugins/master/landscape.svg?style=flat)](https://landscape.io/github/rsmuc/health_monitoring_plugins/master)
[![Code Climate](https://codeclimate.com/github/rsmuc/health_monitoring_plugins/badges/gpa.svg)](https://codeclimate.com/github/rsmuc/health_monitoring_plugins)
[![Issue Count](https://codeclimate.com/github/rsmuc/health_monitoring_plugins/badges/issue_count.svg)](https://codeclimate.com/github/rsmuc/health_monitoring_plugins)
[![PyPI version](https://badge.fury.io/py/health_monitoring_plugins.svg)](https://badge.fury.io/py/health_monitoring_plugins)

## Plugins

A detailed description can be found in the README in the doc folder.

#### [check_snmp_apc_ups](doc/check_snmp_apc_ups/README.md)

Monitor an UPS from APC via SNMP.

#### [check_snmp_eaton_ups](doc/check_snmp_eaton_ups/README.md)

Monitor an UPS from Eaton via SNMP. Requires the built in Eaton network card.

#### [check_snmp_lband](doc/check_snmp_lband/README.md)

Check the status of the CROSS TECHNOLOGIES redundancy controller 2082-141.
Implemented against MIB 2082-141.mib

#### [check_meinberg_ntp](doc/check_meinberg_ntp/README.md)

Check the Meinberg NTP server LANTIME M300.

The plugin checks the current ntp and gps state, shows the current gps position and checks the good satellites.
Tested with firmware version 5.30 and 6.18 (NG).

#### [check_moxa_6000](doc/check_moxa_6000/README.md)

Check the status of a Moxa NPORT 6000 RS232 to LAN converter.  
You can check each port for the CTS, DSR, DTR and Error count.


#### [check_snmp_ilo4](doc/check_snmp_ilo4/README.md)

This plugin checks the health of HP servers with iLo 4 interface via SNMP.

The following components are checked:

- status of powersupply
- status of physical and logical drives (incl. drive temperatures)
- status of fans
- status of the temperature sensors
- the power state of the server (On or Off)
- status of the memory
- the global health status


#### [check_snmp_janitza](doc/check_snmp_janitza/README.md)
Check the status of a Janitza 604 device.

You can check: 
- uL1 - 3               Voltage Phases
- iL1 - 6               Current Phases
- pL1 - 3                Real Power
- qL1 - 3               Reaktiv Power
- sL1 - 3               Power
- cosPL1 - 3            Cos(Phi)
- p3                    Real Power Summe
- q3                    Reaktiv Power Summe
- s3                    Power Summe
- uL1L2,uL2L3,uL3L3     Voltage deltas between Phases


#### [check_snmp_large_storage](doc/check_snmp_large_storage/README.md)

Check the used / free disk space of a device via SNMP (using the HOST-RESOURCES-MIB hrStorageSize).
There are already script doing that like http://nagios.manubulon.com/snmp_storage.html . But these check script have a big problem with large storage systems. 

In our case we want to monitor a Microsoft Windows Server 2012 R2 with an 10 TB partition and one Server with an 25 TB partition. The problem all scripts have, that the SNMP counter hrStorageSize is a 32 Bits
Integer counter. If you have a storage that is larger then 8 TB you will have the issue, that the conuter overruns and will return a negative integer value.

This script will handle the negative integer values and will calculate the proper size. That will only work if the counter overruns once.

#### [check_snmp_port](doc/check_snmp_port/README.md)

Check the status of a tcp/udp port via SNMP. For TCP ports also the status is checked (e.g listen, established).

You could also use for example the check_tcp script. But check_tcp always trys to connect to the port, so we did see a lot of connects and disconncets in the logfile of our database service. And it is also not possible to check the connection status of the port.

If you know snmpnetstat, then you know how the plugin works.


#### [check_snmp_raritan](doc/check_snmp_raritan/README.md)

Check a Raritan Dominition PX PDU (Power Distribution Unit):
* outlets (On, Off)
* inlet (Power, Current, Voltage)
* connected sensors

Tested device: PX2-2486  
Tested sensors: Temperature, Humidity, Contact Closure, Air Pressure


#### [check_snmp_service](doc/check_snmp_service/README.md)

Icinga / Nagios plugin to check if a Windows service is in running state via SNMP.

It may take some time until Windows updates the status via snmp after starting or stopping a service.


#### [check_snmp_time2](doc/check_snmp_time2/README.md)

This plugin compares the time of the icinga/nagios machine with the time of a remote device.

#### [check_snmp_idrac](doc/check_snmp_idrac/README.md)

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


#### [check_snmp_teledyne](doc/check_snmp_teledyne/README.md)

This plugin checks the health of Teledyn Paradise Datacom Sattelite Modem.



#### [check_snmp_ubiquiti](doc/check_snmp_ubiquiti/README.md)

Check the status of a Ubiquiti airMax device.

You can check the:
- Uptime
- Signal Strength
- CPU usage (1 Minute Average)
- CPU usage (5 Minute Average)
- CPU usage (15 Minute Average)
- Total memory
- Free memory
- Tx Rate
- Rx Rate


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

## Run the unittests

To run the unittests just execute:

    python setup.py test

The unittests require pytest. For the unittests we use the testagent from [haxtibal](https://github.com/haxtibal).

## Changelog

###### Version 0.0.7

* Added check_snmp_procurve
* Added check_snmp_lband
* Added check_snmp_eaton_ups
* Added check_snmp_apc_ups
* Several bugfixes and code improvements


###### Version 0.0.6

* Fixed segfault, if there is no route to host

###### Version 0.0.5

* Added check_snmp_teledyne, check_snmp_janitza, check_snmp_ubiquiti

* Several bugfixes

###### Version 0.0.4

* Fixed bug in check_snmp_time2

* Added check_snmp_idrac

###### Version 0.0.3

* Several bugfixes and code cleanup

###### Version 0.0.2

* Several bugfixes and code cleanup

###### Version 0.0.2

* Added unittests for all plugins
* Fixed a bug in check_snmp_raritan Inlet check
* Cleaned up some parts of the code
* Better package structure

###### Version 0.0.1

* The first testing release including all developed check plugins

## TODO

* Implement SNMPv3 support for all plugins

Maybe:

* add a default threshold to check_snmp_time2
* check_snmp_raritan: It should be possible to monitor all outlets / sensors in one service
* check_snmp_large_stroage: Check a list of storages