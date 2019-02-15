import netsnmp
import pynag

TYPE_SKIP = 0
TYPE_AX60 = 1

def make_status(snmp_value):
    return Status(snmp_value)

class Status():
    OK = 0
    WARNING = 1
    ALARMS = 2
    ERRORS = 3

    def __init__(self, status_str):
        self.s = int(status_str)

    def as_icinga_status(self):
        to_icinga = { self.OK: pynag.Plugins.ok, self.WARNING: pynag.Plugins.warning,
                     self.ALARMS: pynag.Plugins.critical, self.ERRORS: pynag.Plugins.critical }
        return to_icinga.get(self.s, pynag.Plugins.warning)

    def __str__(self):
        to_str = { self.OK: "Ok", self.WARNING: "Warning", self.ALARMS: "Alarms", self.ERRORS: "Errors" }
        return to_str[self.s]

def scale100(snmp_value):
    return float(snmp_value) / 100.

def scale1000(snmp_value):
    return float(snmp_value) / 1000.

metric_mib = {
    'skipController1Temperature':  {'oid': '.1.3.6.1.4.1.29890.1.6.2.4.3.8.0', 'label': 'temp_ctl1_deg_c', 'conv': float},
    'skipController2Temperature': {'oid': '.1.3.6.1.4.1.29890.1.6.2.4.3.9.0', 'label': 'temp_ctl2_deg_c', 'conv': float},
    'skipDemodulatorCPU1Temperature': {'oid': '.1.3.6.1.4.1.29890.1.6.2.4.3.5.0', 'label': 'temp_cpu1_deg_c', 'conv': float},
    'skipDemodulatorCPU2Temperature': {'oid': '.1.3.6.1.4.1.29890.1.6.2.4.3.6.0', 'label': 'temp_cpu2_deg_c', 'conv': float},
    'skipDemodulatorTemperature': {'oid': '.1.3.6.1.4.1.29890.1.6.2.4.3.4.0', 'label': 'temp_demod_deg_c', 'conv': float},
    'skipFrontpanelTemperature': {'oid': '.1.3.6.1.4.1.29890.1.6.2.4.3.1.0', 'label': 'temp_frontpanel_deg_c', 'conv': float},
    'skipDemodulatorPSUTemperature': {'oid': '.1.3.6.1.4.1.29890.1.6.2.4.3.7.0', 'label': 'temp_demod_psu_deg_c', 'conv': float},
    'skipVoltageDMD1': {'oid': '.1.3.6.1.4.1.29890.1.6.2.4.4.2.1.0', 'label': 'volt_dmd1', 'conv': scale100}, # expected 1.0V
    'skipVoltageDMD2': {'oid': '.1.3.6.1.4.1.29890.1.6.2.4.4.2.2.0', 'label': 'volt_dmd2', 'conv': scale100}, # expected 1.2V
    'skipVoltageDMD3': {'oid': '.1.3.6.1.4.1.29890.1.6.2.4.4.2.3.0', 'label': 'volt_dmd3', 'conv': scale100}, # expected 2.5
    'skipVoltageDMD4': {'oid': '.1.3.6.1.4.1.29890.1.6.2.4.4.2.4.0', 'label': 'volt_dmd4', 'conv': scale100}, # expected 2.5
    'skipVoltageDMD5': {'oid': '.1.3.6.1.4.1.29890.1.6.2.4.4.2.5.0', 'label': 'volt_dmd5', 'conv': scale100}, # expected 3.3
    'skipVoltageDMD6': {'oid': '.1.3.6.1.4.1.29890.1.6.2.4.4.2.6.0', 'label': 'volt_dmd6', 'conv': scale100}, #'expected 5.0
    'skipVoltageDMD7': {'oid': '.1.3.6.1.4.1.29890.1.6.2.4.4.2.7.0', 'label': 'volt_dmd7', 'conv': scale100}, #'expected 9.0
    'ax60TemperatureBridgeBoard': {'oid': '.1.3.6.1.4.1.29890.1.8.1.4.3.7.0', 'label': '', 'conv': scale1000},
    'ax60TemperatureBridgeChip': {'oid': '.1.3.6.1.4.1.29890.1.8.1.4.3.8.0', 'label': 'temp_bridge_chip_deg_c', 'conv': scale1000},
    'ax60TemperatureCPUBoard': {'oid': '.1.3.6.1.4.1.29890.1.8.1.4.3.4.0', 'label': 'temp_cpu_board_deg_c', 'conv': scale1000},
    'ax60TemperatureCPUChip': {'oid': '.1.3.6.1.4.1.29890.1.8.1.4.3.5.0', 'label': 'temp_cpu_deg_c', 'conv': scale1000},
    'ax60TemperatureDemodulatorBoard': {'oid': '.1.3.6.1.4.1.29890.1.8.1.4.3.9.0', 'label': 'temp_demodulator_board_deg_c', 'conv': scale1000},
    'ax60TemperatureDemodulatorChip': {'oid': '.1.3.6.1.4.1.29890.1.8.1.4.3.10.0', 'label': 'temp_demodulator_deg_c', 'conv': scale1000},
    'ax60TemperatureDevice': {'oid': '.1.3.6.1.4.1.29890.1.8.1.4.3.1.0', 'label': 'temp_device_deg_c', 'conv': scale1000},
}

status_mib = {
    'skipStatusDemodulator': {'oid': '.1.3.6.1.4.1.29890.1.6.2.6.2.0', 'text': 'Demodulator status', 'conv': make_status},
    'skipStatusSystem': {'oid': '.1.3.6.1.4.1.29890.1.6.2.6.3.0', 'text': 'System status', 'conv': make_status},
    'ax60GlobalStatus': {'oid': '.1.3.6.1.4.1.29890.1.8.1.6.1.0', 'text': 'Global status', 'conv': make_status},
}

class MicrowaveModem(object):
    models = {
        TYPE_SKIP: {
            'name': "WORK Microwave SK-IP Modem",
            'alarms': ['skipStatusDemodulator', 'skipStatusSystem'],
            'metrics': ['skipController1Temperature', 'skipController2Temperature', 'skipDemodulatorCPU1Temperature',
                        'skipDemodulatorCPU2Temperature', 'skipDemodulatorTemperature', 'skipFrontpanelTemperature',
                        'skipFrontpanelTemperature', 'skipDemodulatorPSUTemperature', 'skipVoltageDMD1',
                        'skipVoltageDMD2', 'skipVoltageDMD3', 'skipVoltageDMD4', 'skipVoltageDMD5',
                        'skipVoltageDMD6', 'skipVoltageDMD7']
        },
        TYPE_AX60: {
            'name': "WORK Microwave AX-60 Modem",
            'alarms': ['ax60GlobalStatus'],
            'metrics': ['ax60TemperatureBridgeBoard', 'ax60TemperatureBridgeChip', 'ax60TemperatureCPUBoard',
                        'ax60TemperatureCPUChip', 'ax60TemperatureDemodulatorBoard', 'ax60TemperatureDemodulatorChip',
                        'ax60TemperatureDevice']
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
        "Return one SNMP response list for all status OIDs, and one list for all metric OIDs."
        alarm_oids = [netsnmp.Varbind(status_mib[alarm_id]['oid']) for alarm_id in self.models[self.modem_type]['alarms']]
        metric_oids = [netsnmp.Varbind(metric_mib[metric_id]['oid']) for metric_id in self.models[self.modem_type]['metrics']]
        response = self.snmp_session.get(netsnmp.VarList(*alarm_oids + metric_oids))
        return (
            response[0:len(alarm_oids)],
            response[len(alarm_oids):]
        )

    def process_alarms(self, snmp_data):
        "Build list with active alarms"
        self.active_alarms = {}
        for i in range(0, len(self.models[self.modem_type]['alarms'])):
            mib_name = self.models[self.modem_type]['alarms'][i]
            conv = status_mib[mib_name]['conv']
            self.active_alarms[mib_name] = conv(snmp_data[i])

    def process_metrics(self, snmp_data):
        "Build list with metrics"
        self.metrics = {}
        for i in range(0, len(snmp_data)):
            mib_name = self.models[self.modem_type]['metrics'][i]
            conv = metric_mib[mib_name]['conv']
            self.metrics[mib_name] = conv(snmp_data[i])

    def health_status(self):
        if self.active_alarms == None or self.metrics == None:
            return pynag.Plugins.unknown
        elif len(self.active_alarms) > 0:
            return pynag.Plugins.critical
        else:
            return pynag.Plugins.ok

    def model_summary(self):
        return self.models[self.modem_type]['name']

    def alarm_summary(self):
        status_msgs = []
        for mib_name in self.active_alarms:
            status_msgs.append("{}: {}.".format(status_mib[mib_name]['text'], str(self.active_alarms[mib_name])))
        return " ".join(status_msgs)

    def perfdata(self):
        perfdata = []
        for mib_name in self.metrics:
            perf = {'label': metric_mib[mib_name]['label'],
                    'value': self.metrics[mib_name]}
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
        alarm_summary = self.alarm_summary()
        if alarm_summary is not None:
            icinga_plugin.add_summary(alarm_summary)
        for perfdata in self.perfdata():
            icinga_plugin.add_metric(**perfdata)
        icinga_plugin.check_all_metrics()
