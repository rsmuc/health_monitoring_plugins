import pynag
import netsnmp

netsnmp.verbose = 0

class SnmpException(Exception):
    """SNMP Errors being detected:
    -DNS resolution for host name during Session.__init__ fails
    -SNMP set failed with SNMP standard error code
    -SNMP getbulk error during netsnmptable.get_entries
    -Received data can't be parsed into expected type
    """
    pass

class SnmpHelper(pynag.Plugins.PluginHelper):
    def __init__(self, *args, **kwargs):
        pynag.Plugins.PluginHelper.__init__(self, *args, **kwargs)
        self.parser.add_option('-H', '--hostname', help="Hostname or ip address")
        self.parser.add_option('-C', '--community', help='SNMP community of the SNMP service on target host.', default='public')
        self.parser.add_option('-V', '--snmpversion', help='SNMP version. (1 or 2)', default=2, type='int')
        self.parser.add_option('--retries', help='Number of SNMP retries.', default=0, type='int')

    def parse_arguments(self):
        pynag.Plugins.PluginHelper.parse_arguments(self)
        if not self.options.hostname:
            self.parser.error(
                "Hostname must be specified")

    def get_snmp_args(self):
        args = {'DestHost': self.options.hostname,
                'Version': self.options.snmpversion,
                'Community': self.options.community,
                'Retries': self.options.retries}
        if self.options.timeout:
            args['Timeout'] = self.options.timeout * 1000
        return args

class SnmpSession(netsnmp.Session):
    """Wrap netsnmp.Session to workaround some shortcomings there"""

    def __init__(self, *args, **kwargs):
        super(SnmpSession, self).__init__(*args, **kwargs)
        if self.sess_ptr == 0:
            raise SnmpException("DNS resolution for SNMP host failed")

    def get_oids(self, *oids):
        varlist = netsnmp.VarList(*oids)
        response = self.get(varlist)
        if not response or len(response) != len(oids):
            raise SnmpException("SNMP get response incomplete")
        return response

    def walk_oid(self, oid):
        """Get a list of SNMP varbinds in response to a walk for oid.
        
        Each varbind in response list has a tag, iid, val and type attribute."""
        var = netsnmp.Varbind(oid)
        varlist = netsnmp.VarList(var)
        data = self.walk(varlist)
        if len(data) == 0:
            raise SnmpException("SNMP walk response incomplete")
        return varlist

    def set(self, *args, **kwargs):
        # Python bindings prior to netsnmp 5.4.4 have a bug where they don't return error codes.
        # We can't do anything if older netsnmp is used.
        # See https://sourceforge.net/p/net-snmp/code/ci/9ea6d4d870ee537ee29283bec6c4308d9048351c,
        # https://sourceforge.net/p/net-snmp/mailman/message/25846001/.
        result = super(SnmpSession, self).set(*args, **kwargs)
        if result != 1:
            raise SnmpException("SNMP set failed")