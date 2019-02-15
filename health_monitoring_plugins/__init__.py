import pynag
import netsnmp
from pynag.Plugins import unknown

netsnmp.verbose = 0


class SnmpException(Exception):
    """SNMP Errors being detected:
    -DNS resolution for host name during Session.__init__ fails
    -SNMP set failed with SNMP standard error code
    -SNMP getbulk error during netsnmptable.get_entries
    -Received data can't be parsed into expected type
    """
    pass


class HelperExtension(pynag.Plugins.PluginHelper):
    """some extensions for the Pynag Helper"""
    def __init__(self):
        pass

    def update_status(self, helper, status):
        """ update the helper """
        if status:
            self.status(status[0])

            # if the status is ok, add it to the long output
            if status[0] == 0:
                self.add_long_output(status[1])
            # if the status is not ok, add it to the summary
            else:
                self.add_summary(status[1])


class SnmpHelper(pynag.Plugins.PluginHelper, HelperExtension):
    def __init__(self, *args, **kwargs):
        pynag.Plugins.PluginHelper.__init__(self, *args, **kwargs)
        self.parser.add_option('-H', '--hostname', help="Hostname or ip address")
        self.parser.add_option('-C', '--community', help='SNMP community of the SNMP service on target host.',
                               default='public')
        self.parser.add_option('-V', '--snmpversion', help='SNMP version. (1 or 2)', default=2, type='int')
        self.parser.add_option('--retries', help='Number of SNMP retries.', default=0, type='int')
        self.parser.add_option('-U', '--securityname', help="SNMPv3: security name (e.g. bert)", dest="secname")
        self.parser.add_option('-L', '--securitylevel',
                               help="SNMPv3: security level (noAuthNoPriv, authNoPriv, authPriv)", dest="seclevel")
        self.parser.add_option('-a', '--authprotocol', help="SNMPv3: authentication protocol (MD5|SHA)",
                               dest="authproto")
        self.parser.add_option('-A', '--authpass', help="SNMPv3: authentication protocol pass phrase",
                               dest="authpass")
        self.parser.add_option('-x', '--privproto', help="SNMPv3: privacy protocol (DES|AES)", dest="privproto")
        self.parser.add_option('-X', '--privpass', help="SNMPv3: privacy protocol pass phrase", dest="privpass")

    def parse_arguments(self):
        pynag.Plugins.PluginHelper.parse_arguments(self)
        if not self.options.hostname:
            self.parser.error(
                "Hostname must be specified")

    def get_snmp_args(self):
        args = {'DestHost': self.options.hostname,
                'Version': self.options.snmpversion,
                'SecName': self.options.secname,
                'SecLevel': self.options.seclevel,
                'AuthProto': self.options.authproto,
                'AuthPass': self.options.authpass,
                'PrivProto': self.options.privproto,
                'PrivPass': self.options.privpass,
                'Community': self.options.community,
                'Retries': self.options.retries}
        if self.options.timeout:
            args['Timeout'] = self.options.timeout * 1000

        return args

    @staticmethod
    def get_snmp_value(sess, helper, oid):
        """ return a snmp value or exits the plugin with unknown"""
        snmp_result = sess.get_oids(oid)[0]
        if snmp_result is None:
            helper.exit(summary="No response from device for oid " + oid, exit_code=unknown, perfdata='')

        else:
            return snmp_result

    @staticmethod
    def walk_snmp_values(sess, helper, oid, check):
        """ return a snmp value or exits the plugin with unknown"""
        try:
            snmp_walk = sess.walk_oid(oid)

            result_list = []
            for x in range(len(snmp_walk)):
                result_list.append(snmp_walk[x].val)

            if result_list != []:
                return result_list

            else:
                raise SnmpException("No content")
        except SnmpException:
            helper.exit(summary="No response from device for {} ({})".format(check, oid),
                        exit_code=unknown, perfdata='')


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
