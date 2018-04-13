from setuptools import setup, find_packages
import sys
import os

if sys.argv[-1] == 'test':
    test_requirements = ['pytest',]
    try:
        modules = map(__import__, test_requirements)
    except ImportError as e:
        err_msg = e.message.replace("No module named ", "")
        msg = "%s is not installed. Install your test requirments." % err_msg
        raise ImportError(msg)
    #os.system('py.test')
    # the current testagent does not support starting and stopping the agent within one testrun, so we need to call the script
    os.system('./run_unittest.sh')
    sys.exit()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='health_monitoring_plugins',
      version='0.0.8',
      description='Health monitoring plugins for icinga/nagios',
      url='https://github.com/rsmuc/health_monitoring_plugins',
      author='rsmuc',
      author_email='rsmuc@mailbox.org',
      license='GPLv2',
      classifiers=[
        "Topic :: System :: Monitoring",
        "Development Status :: 3 - Alpha"],
      packages= find_packages(),
      package_data = {'': ['*.md']},
      long_description=read('README.md'),
      install_requires=['pynag',],
      scripts=['health_monitoring_plugins/check_snmp_raritan/check_snmp_raritan.py',
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
               'health_monitoring_plugins/check_snmp_sencere/check_snmp_sencere.py',
               'health_monitoring_plugins/check_snmp_procurve/check_snmp_procurve.py',
               'health_monitoring_plugins/check_snmp_fortinet/check_snmp_fortinet.py',
               'health_monitoring_plugins/check_jenkins_api/check_jenkins_api.py',
               'health_monitoring_plugins/check_snmp_trusted_filter/check_snmp_trusted_filter.py',
               'health_monitoring_plugins/snmpSessionBaseClass.py',
               ],
      test_suite="test",
      include_package_data=True,
      zip_safe=False)