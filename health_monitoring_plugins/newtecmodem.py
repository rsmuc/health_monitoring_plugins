import netsnmp
import pynag

TYPE_MDM6000 = 0
TYPE_MDM9000 = 1

def scale100(snmp_value):
    return float(snmp_value) / 100.

alarms = {
    'ntcAntCtrlAntFailure': {'oid': '.1.3.6.1.4.1.5835.5.2.5700.1.3.3.0', 'text': "Antenna non-functional"},
    'ntcAntCtrlAntFailureStat': {'oid': '.1.3.6.1.4.1.5835.5.2.5700.1.3.1.1.3.1', 'text': "Antenna controller 1 non-functional"},
    'ntcDevAlmHardwareFailure': {'oid': '.1.3.6.1.4.1.5835.5.2.100.1.10.11.0', 'text': "Hardware malfunction"},
    'ntcDevAlmInternalError': {'oid': '.1.3.6.1.4.1.5835.5.2.100.1.10.12.0', 'text': "Internal error"},
    'ntcDevAlmFrontPanelFailure': {'oid': '.1.3.6.1.4.1.5835.5.2.100.1.10.6.0', 'text': "Frontpanel communication failed"},
    'ntcDevAlmGenBootConfigFailure': {'oid': '.1.3.6.1.4.1.5835.5.2.100.1.10.2.0', 'text': "Erroneous boot configuration"},
    'ntcDevAlmGenDeviceAlarm': {'oid': '.1.3.6.1.4.1.5835.5.2.100.1.10.1.0', 'text': "General device failure"},
    'ntcDevAlmHardwareInventory': {'oid': '.1.3.6.1.4.1.5835.5.2.100.1.10.10.0', 'text':  "Hardware inventory no longer matching with production inventory"},
    'ntcDevAlmInvalidLicenseFile': {'oid': '.1.3.6.1.4.1.5835.5.2.100.1.10.5.0', 'text': "License file non-existent or wrongly signed"},
    'ntcDevAlmNtpNoPeerFailure': {'oid': '.1.3.6.1.4.1.5835.5.2.100.1.10.8.0', 'text': "None of the configured NTP servers reachable"},
    'ntcDevAlmUpgradeFailure': {'oid': '.1.3.6.1.4.1.5835.5.2.100.1.10.7.0', 'text': "Software upgrade failed"},
    'ntcEtherAlmMgmtEthInterfaceFail': {'oid': '.1.3.6.1.4.1.5835.5.2.500.1.6.11.0', 'text': "Failure detected on management ethernet interface"},
    'ntcEtherAlmDataEthInterfaceFail': {'oid': '.1.3.6.1.4.1.5835.5.2.500.1.6.12.0', 'text': "Failure is detected on data ethernet interface"},
    'ntcEtherAlmSatEthInterfaceFail': {'oid': '.1.3.6.1.4.1.5835.5.2.500.1.6.17.0', 'text': "Failure is detected on sat ethernet interface"},
    'ntcFanCAlmFanFailure': {'oid': '.1.3.6.1.4.1.5835.5.2.3500.1.1.1.0', 'text': "Fan failure"},
    'ntcIF2LConvCommunication': {'oid': '.1.3.6.1.4.1.5835.5.2.4600.1.1.2.0', 'text': "Converter not working due to communication failures"},
    'ntcIF2LConvHardware': {'oid': '.1.3.6.1.4.1.5835.5.2.4600.1.1.1.0', 'text': "Converter not working due to hardware failures"},
}

metrics = {
    'ntcDevMonPowerSupply': {'oid': '.1.3.6.1.4.1.5835.5.2.100.1.9.2.0', 'label': 'power_v', 'conv': scale100},
    'ntcDevMonTemperature': {'oid': '.1.3.6.1.4.1.5835.5.2.100.1.9.1.0', 'label': 'temp_deg_c', 'conv': float}
}

class NewtecModem(object):
    models = {
        TYPE_MDM6000: {
            'name': "Newtec MDM6000",
            'alarms': ['ntcAntCtrlAntFailure', 'ntcAntCtrlAntFailureStat', 'ntcDevAlmFrontPanelFailure', 'ntcDevAlmGenBootConfigFailure', 'ntcDevAlmGenDeviceAlarm',
                       'ntcDevAlmHardwareInventory', 'ntcDevAlmInvalidLicenseFile', 'ntcDevAlmNtpNoPeerFailure', 'ntcDevAlmUpgradeFailure', 'ntcEtherAlmMgmtEthInterfaceFail',
                       'ntcEtherAlmDataEthInterfaceFail', 'ntcEtherAlmSatEthInterfaceFail', 'ntcFanCAlmFanFailure'],
            'metrics': ['ntcDevMonPowerSupply', 'ntcDevMonTemperature']
        },
        TYPE_MDM9000: {
            'name': "Newtec MDM9000",
            'alarms': ['ntcAntCtrlAntFailure', 'ntcAntCtrlAntFailureStat', 'ntcDevAlmHardwareFailure', 'ntcDevAlmInternalError', 'ntcDevAlmFrontPanelFailure',
                       'ntcDevAlmGenBootConfigFailure', 'ntcDevAlmGenDeviceAlarm', 'ntcDevAlmHardwareInventory', 'ntcDevAlmInvalidLicenseFile', 'ntcDevAlmNtpNoPeerFailure',
                       'ntcDevAlmUpgradeFailure', 'ntcEtherAlmMgmtEthInterfaceFail', 'ntcEtherAlmDataEthInterfaceFail', 'ntcEtherAlmSatEthInterfaceFail', 'ntcFanCAlmFanFailure',
                       'ntcIF2LConvCommunication', 'ntcIF2LConvHardware'],
            'metrics': ['ntcDevMonPowerSupply', 'ntcDevMonTemperature']
        }
    }

    def __init__(self, modem_type, snmp_session):
        self.modem_type = modem_type
        self.snmp_session = snmp_session

    def check(self):
        try:
            (snmp_alarm_data, snmp_metric_data) = self.get_data()
            self.process_alarms(snmp_alarm_data)
            self.process_metrics(snmp_metric_data)
        except (TypeError, KeyError, ValueError):
            self.active_alarms = None
            self.metrics = None

    def get_data(self):
        "Get SNMP values from host"
        alarm_oids = [netsnmp.Varbind(alarms[alarm_id]['oid']) for alarm_id in self.models[self.modem_type]['alarms']]
        metric_oids = [netsnmp.Varbind(metrics[metric_id]['oid']) for metric_id in self.models[self.modem_type]['metrics']]
        response = self.snmp_session.get(netsnmp.VarList(*alarm_oids + metric_oids))
        return (
            response[0:len(alarm_oids)],
            response[len(alarm_oids):]
        )

    def process_alarms(self, snmp_data):
        "Build list with active alarms"
        self.active_alarms = []
        for i in range(0, len(self.models[self.modem_type]['alarms'])):
            if bool(int(snmp_data[i])) == True:
                self.active_alarms.append(self.models[self.modem_type]['alarms'][i])

    def process_metrics(self, snmp_data):
        "Build list with metrics"
        self.metrics = {}
        for i in range(0, len(snmp_data)):
            metric_id = self.models[self.modem_type]['metrics'][i]
            conv = metrics[metric_id]['conv']
            self.metrics[metric_id] = conv(snmp_data[i])

    def health_status(self):
        if self.active_alarms == None or self.metrics == None:
            return pynag.Plugins.unknown
        elif len(self.active_alarms) > 0:
            return pynag.Plugins.critical
        else:
            return pynag.Plugins.ok

    def model_summary(self):
        return self.models[self.modem_type]['name']

    def status_summary(self):
        if len(self.active_alarms) > 0:
            return "Status: {} alarms active.".format(len(self.active_alarms))
        else:
            return "Status: OK."

    def alarm_info(self):
        return ["Alarm: " + alarms[alarm_id]['text'] for alarm_id in self.active_alarms]

    def perfdata(self):
        perfdata = []
        for metric_id in self.metrics:
            perf = {'label': metrics[metric_id]['label'],
                    'value': self.metrics[metric_id]}
            perfdata.append(perf)
        return perfdata

    def feed_icinga_plugin(self, icinga_plugin):
        icinga_plugin.show_status_in_summary = False
        if self.active_alarms is None or self.metrics is None:
            icinga_plugin.show_status_in_summary = True
            icinga_plugin.status(pynag.Plugins.unknown)
            icinga_plugin.add_summary("SNMP response incomplete or invalid")
            return
        icinga_plugin.status(self.health_status())
        icinga_plugin.add_summary(self.model_summary())
        icinga_plugin.add_summary(self.status_summary())
        for alarm_info in self.alarm_info():
            icinga_plugin.add_long_output(alarm_info)
        for perfdata in self.perfdata():
            icinga_plugin.add_metric(**perfdata)
        icinga_plugin.check_all_metrics()
