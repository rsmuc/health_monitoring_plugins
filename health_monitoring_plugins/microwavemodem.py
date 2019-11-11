import netsnmp
import pynag

TYPE_SKIP = 0
TYPE_AX60 = 1

class Ax60Status(object):
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

    def detailed_lines(self):
        return []

    def __str__(self):
        to_str = { self.OK: "Ok", self.WARNING: "Warning", self.ALARMS: "Alarms", self.ERRORS: "Errors" }
        return to_str[self.s]

class SkipStatus(object):
    def __init__(self, status_str):
        status_mask = int(status_str.replace(' ', ''), 16)
        self.status_bits = [bit for bit in range(32) if status_mask >> bit & 1 == True]
        self.info_bits = [bit for bit in self.INFOS if bit in self.status_bits]
        self.warning_bits = [bit for bit in self.WARNINGS if bit in self.status_bits]
        self.alarm_bits = [bit for bit in self.ALARMS if bit in self.status_bits]

    def as_icinga_status(self):
        if len(self.alarm_bits) > 0:
            return pynag.Plugins.critical
        elif len(self.warning_bits) > 0:
            return pynag.Plugins.warning
        return pynag.Plugins.ok

    def detailed_lines(self):
        return [self.COMPONENT + ": " + self.TEXT[bit] for bit in self.status_bits]

    def __str__(self):
        if len(self.info_bits) == 0 and len(self.warning_bits) == 0 and len(self.alarm_bits) == 0:
            return "Ok"
        msg = []
        if len(self.info_bits) > 0:
            msg.append("{} note(s)".format(len(self.info_bits)))
        if len(self.warning_bits) > 0:
            msg.append("{} warning(s)".format(len(self.warning_bits)))
        if len(self.alarm_bits) > 0:
            msg.append("{} error(s)".format(len(self.alarm_bits)))
        return ", ".join(msg)

class SkipSystemStatus(SkipStatus):
    COMPONENT = "System"
    TEXT = {
            0: 'Mod. communication alarm',
            1: 'Demod. communication alarm',
            2: 'External mute input warning',
            3: 'Auto TX Off warning',
            4: 'Alarm Relay disabled warning',
            5: 'Alarm Relay test warning',
            16: 'Temperature sensor warning',
            17: 'Key warning',
            18: 'RTC warning',
            19: 'LCD warning',
            20: 'Ethernet warning',
            21: 'EEPROM warning',
            22: 'Temperature high warning',
            23: 'Temperature low warning',
            24: 'Webserver warning',
            25: 'SNMP warning',
            26: 'Webctl warning',
            27: 'Messagebus warning',
            28: 'NTP communication warning',
            29: 'Memory warning',
            31: 'Summary alarm'
        }
    INFOS = []
    WARNINGS = [2, 3, 4, 5, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31]
    ALARMS = [0, 1, 31]

class SkipDemodulatorStatus(SkipStatus):
    COMPONENT = "Demodulator"
    TEXT = {
            0: 'RAM error alarm',
            1: 'Interpolator alarm',
            2: 'Clock PLL overload alarm',
            3: 'Shutdown by security device',
            4: 'FIFO full warning',
            5: 'Clock oscillator alarm',
            6: 'Local oscillator alarm',
            7: 'Clock PLL lock warning',
            8: 'Converter alarms',
            9: 'Reference alarm (converter)',
            11: 'DVB communication alarm',
            12: 'TS clock oscillator alarm',
            13: 'TX Output off',
            13: 'TX Output off',
            14: 'External mute active',
            15: 'OCXO oven cold warning',
            16: 'DVB input not in sync',
            17: 'ASI B signal low warning',
            18: 'PCR Memory full warning',
            19: 'Invalid configuration',
            20: '24 V DC shorted warning',
            21: 'Converter PLO alarm',
            22: 'BISS code activation delayed',
            23: 'Test Mode',
            28: 'BIAS TEE module short circuit',
            29: 'BIAS TEE module DC loss'
        }
    INFOS = [3, 13, 14, 23]
    WARNINGS = [4, 7, 15, 16, 17, 18, 19, 20, 22]
    ALARMS = [0, 1, 2, 5, 6, 8, 9, 11, 12, 13, 21, 28, 29]

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
    'ax60TemperatureBridgeBoard': {'oid': '.1.3.6.1.4.1.29890.1.8.1.4.3.7.0', 'label': 'temp_bridge_board_deg_c', 'conv': scale1000},
    'ax60TemperatureBridgeChip': {'oid': '.1.3.6.1.4.1.29890.1.8.1.4.3.8.0', 'label': 'temp_bridge_chip_deg_c', 'conv': scale1000},
    'ax60TemperatureCPUBoard': {'oid': '.1.3.6.1.4.1.29890.1.8.1.4.3.4.0', 'label': 'temp_cpu_board_deg_c', 'conv': scale1000},
    'ax60TemperatureCPUChip': {'oid': '.1.3.6.1.4.1.29890.1.8.1.4.3.5.0', 'label': 'temp_cpu_deg_c', 'conv': scale1000},
    'ax60TemperatureDemodulatorBoard': {'oid': '.1.3.6.1.4.1.29890.1.8.1.4.3.9.0', 'label': 'temp_demodulator_board_deg_c', 'conv': scale1000},
    'ax60TemperatureDemodulatorChip': {'oid': '.1.3.6.1.4.1.29890.1.8.1.4.3.10.0', 'label': 'temp_demodulator_deg_c', 'conv': scale1000},
    'ax60TemperatureDevice': {'oid': '.1.3.6.1.4.1.29890.1.8.1.4.3.1.0', 'label': 'temp_device_deg_c', 'conv': scale1000},
}

status_mib = {
    'skipStatusDemodulator': {'oid': '.1.3.6.1.4.1.29890.1.6.2.6.2.0', 'text': 'Demodulator status', 'conv': SkipDemodulatorStatus},
    'skipStatusSystem': {'oid': '.1.3.6.1.4.1.29890.1.6.2.6.3.0', 'text': 'System status', 'conv': SkipSystemStatus},
    'ax60GlobalStatus': {'oid': '.1.3.6.1.4.1.29890.1.8.1.6.1.0', 'text': 'Global status', 'conv': Ax60Status},
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
            self.process_status(snmp_alarm_data)
            self.process_metrics(snmp_metric_data)
        except (TypeError, KeyError, ValueError):
            self.status = None
            self.metrics = None

    def get_data(self):
        "Return one SNMP response list for all status OIDs, and one list for all metric OIDs."
        status_oids = [netsnmp.Varbind(status_mib[tag]['oid']) for tag in self.models[self.modem_type]['alarms']]
        metric_oids = [netsnmp.Varbind(metric_mib[tag]['oid']) for tag in self.models[self.modem_type]['metrics']]
        response = self.snmp_session.get(netsnmp.VarList(*status_oids + metric_oids))
        return (
            response[0:len(status_oids)],
            response[len(status_oids):]
        )

    def process_status(self, snmp_data):
        "Build list with active alarms"
        self.status = {}
        for i in range(0, len(self.models[self.modem_type]['alarms'])):
            mib_name = self.models[self.modem_type]['alarms'][i]
            conv = status_mib[mib_name]['conv']
            self.status[mib_name] = conv(snmp_data[i])

    def process_metrics(self, snmp_data):
        "Build list with metrics"
        self.metrics = {}
        for i in range(0, len(snmp_data)):
            mib_name = self.models[self.modem_type]['metrics'][i]
            conv = metric_mib[mib_name]['conv']
            self.metrics[mib_name] = conv(snmp_data[i])

    def health_status(self):
        if self.status == None or self.metrics == None:
            return pynag.Plugins.unknown
        elif len(self.status) > 0:
            return pynag.Plugins.critical
        else:
            return pynag.Plugins.ok

    def model_summary(self):
        return self.models[self.modem_type]['name']

    def status_summary(self):
        status_msgs = []
        for mib_name in self.status:
            status_msgs.append("{}: {}.".format(status_mib[mib_name]['text'], str(self.status[mib_name])))
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
        if self.status is None or self.metrics is None:
            icinga_plugin.show_status_in_summary = True
            icinga_plugin.status(pynag.Plugins.unknown)
            icinga_plugin.add_summary("SNMP response incomplete or invalid")
            return
        icinga_plugin.status(pynag.Plugins.ok)
        icinga_plugin.add_summary(self.model_summary())
        status_summary = self.status_summary()
        if status_summary is not None:
            icinga_plugin.add_summary(status_summary)
        for oid in self.status.keys():
            status = self.status[oid]
            icinga_plugin.add_status(status.as_icinga_status())
            for detailed_line in status.detailed_lines():
                icinga_plugin.add_long_output(detailed_line)
        for perfdata in self.perfdata():
            icinga_plugin.add_metric(**perfdata)
        icinga_plugin.check_all_metrics()
