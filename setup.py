#!/usr/bin/python

#    Copyright (C) 2016-2019 rsmuc <rsmuc@sec-dev.de>

#    This file is part of "Health Monitoring Plugins".

#    "Health Monitoring Plugins" is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    "Health Monitoring Plugins" is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <https://www.gnu.org/licenses/>.

import sys
import os
from setuptools import setup, find_packages

if sys.argv[-1] == 'test':
    test_requirements = ['pytest']
    try:
        modules = map(__import__, test_requirements)
    except ImportError as e:
        err_msg = e.message.replace("No module named ", "")
        msg = "%s is not installed. Install your test requirements." % err_msg
        raise ImportError(msg)
    # the current testagent does not support starting and stopping the agent within one testrun,
    # so we need to call the script
    os.system('./run_unittest.sh')
    sys.exit()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='health_monitoring_plugins',
      version='0.2.1',
      description='Health monitoring plugins for icinga/nagios',
      url='https://codeberg.org/status_monitoring_tools/health_monitoring_plugins',
      author='rsmuc',
      author_email='rsmuc@sec-dev.de',
      license='GPLv2',
      classifiers=[
          "Topic :: System :: Monitoring",
          "Development Status :: 5 - Production/Stable"],
      packages=find_packages(),
      package_data={'': ['*.md']},
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      install_requires=['pynag'],
      scripts=[
          'health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py',
          'health_monitoring_plugins/check_meinberg_ntp/check_meinberg_ntp.py',
          'health_monitoring_plugins/check_snmp_apc_ups/check_snmp_apc_ups.py',
          'health_monitoring_plugins/check_snmp_eaton_ups/check_snmp_eaton_ups.py',
          'health_monitoring_plugins/check_moxa_6000/check_moxa_6000.py',
          'health_monitoring_plugins/check_snmp_ilo4/check_snmp_ilo4.py',
          'health_monitoring_plugins/check_snmp_large_storage/check_snmp_large_storage.py',
          'health_monitoring_plugins/check_snmp_port/check_snmp_port.py',
          'health_monitoring_plugins/check_snmp_service/check_snmp_service.py',
          'health_monitoring_plugins/check_snmp_time2/check_snmp_time2.py',
          'health_monitoring_plugins/check_snmp_idrac/check_snmp_idrac.py',
          'health_monitoring_plugins/check_snmp_janitza/check_snmp_janitza.py',
          'health_monitoring_plugins/check_snmp_ubiquiti/check_snmp_ubiquiti.py',
          'health_monitoring_plugins/check_snmp_teledyne/check_snmp_teledyne.py',
          'health_monitoring_plugins/check_snmp_lband/check_snmp_lband.py',
          'health_monitoring_plugins/check_snmp_procurve/check_snmp_procurve.py',
          'health_monitoring_plugins/check_snmp_fortinet/check_snmp_fortinet.py',
          'health_monitoring_plugins/check_local_cpu_temperature/check_local_cpu_temperature.py',
          'health_monitoring_plugins/check_jenkins_api/check_jenkins_api.py',
          'health_monitoring_plugins/check_snmp_trusted_filter/check_snmp_trusted_filter.py',
          'health_monitoring_plugins/check_snmp_inradios_csm/check_snmp_inradios_csm.py',
          'health_monitoring_plugins/check_microwavemodem/check_microwavemodem.py',
          'health_monitoring_plugins/check_newtecmodem/check_newtecmodem.py',
          'health_monitoring_plugins/check_snmp_eps_plus/check_snmp_eps_plus.py',
          'health_monitoring_plugins/check_snmp_cambium_ptp700/check_snmp_cambium_ptp700.py',
          'health_monitoring_plugins/snmpSessionBaseClass.py',
      ],
      test_suite="test",
      include_package_data=True,
      zip_safe=False)
