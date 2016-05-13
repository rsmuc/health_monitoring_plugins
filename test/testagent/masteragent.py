import atexit
import netsnmpagent
import os
import shutil
import sys
import tempfile
from collections import defaultdict
from netsnmpapi import *

class MasterAgent(netsnmpagent.netsnmpAgent):
    """"Extends the upstream version of netsnmpAgent to make it suite for our use case.

    Instead of modifying the netsnmpAgent sources,
    modifications are kept separate to make them obvious.
    """

    def __init__(self, **kwargs):

        # This is a workaround, to avoid initialization as agentx client.
        # The other way around would be to patch the original sources. 
        import netsnmpapi
        def skip_init_agent(*args, **kwargs):
            return 0
        def skip_init_mib(*args, **kwargs):
            pass
        def skip_read_mib(*args, **kwargs):
            return 1
        tmp_init_agent = netsnmpapi.libnsa.init_agent
        tmp_netsnmp_init_mib = netsnmpapi.libnsa.netsnmp_init_mib
        tmp_read_mib = netsnmpapi.libnsa.read_mib
        netsnmpapi.libnsa.init_agent = skip_init_agent
        netsnmpapi.libnsa.netsnmp_init_mib = skip_init_mib
        netsnmpapi.libnsa.read_mib = skip_read_mib

        self.config_file = tempfile.NamedTemporaryFile()
        self.state_dir = tempfile.mkdtemp()

        kwargs["MasterSocket"] = None
        kwargs["PersistenceDir"] = self.state_dir

        super(MasterAgent,self).__init__(**kwargs)

        # Make us an AgentX master agent, in order to run standalone.
        if libnsa.netsnmp_ds_set_boolean(
            NETSNMP_DS_APPLICATION_ID,
            NETSNMP_DS_AGENT_ROLE,
            0
        ) != SNMPERR_SUCCESS:
            raise netsnmpAgentException(
                "netsnmp_ds_set_boolean() failed for NETSNMP_DS_AGENT_ROLE!"
            )

        NETSNMP_DS_LIB_OPTIONALCONFIG           = 5
        NETSNMP_DS_LIB_DONT_READ_CONFIGS        = 6

        if libnsa.netsnmp_ds_set_string(
            NETSNMP_DS_LIBRARY_ID,
            NETSNMP_DS_LIB_OPTIONALCONFIG,
            ctypes.c_char_p(self.config_file.name)
        ) != SNMPERR_SUCCESS:
            raise netsnmpAgentException(
                "netsnmp_ds_set_string() failed for NETSNMP_DS_LIB_OPTIONALCONFIG!"
            )
        if libnsa.netsnmp_ds_set_boolean(
            NETSNMP_DS_LIBRARY_ID,
            NETSNMP_DS_LIB_DONT_READ_CONFIGS,
            ctypes.c_int(1)
        ) != SNMPERR_SUCCESS:
            raise netsnmpAgentException(
                "netsnmp_ds_set_boolean() failed for NETSNMP_DS_LIB_DONT_READ_CONFIGS!"
            )

        # Initialize net-snmp library (see netsnmp_agent_api(3))
        if tmp_init_agent(self.AgentName) != 0:
            raise netsnmpAgentException("init_agent() failed!")

        # Initialize MIB parser
        if self.UseMIBFiles:
            tmp_netsnmp_init_mib()

        # If MIBFiles were specified (ie. MIBs that can not be found in
        # net-snmp's default MIB directory /usr/share/snmp/mibs), read
        # them in so we can translate OID strings to net-snmp's internal OID
        # format.
        if self.UseMIBFiles and self.MIBFiles:
            for mib in self.MIBFiles:
                if tmp_read_mib(mib) == 0:
                    raise netsnmpAgentException("netsnmp_read_module({0}) " +
                                                "failed!".format(mib))

        atexit.register(self.__del__)

    def InstanceVarTypeClass(property_func):
        def create_vartype_class(self, initval = None, oidstr = None, writable = True, context = ""):
            agent = self
            # Call the decorated function
            props = property_func(self, initval)

            if initval == None:
                initval = props["initval"]

            class cls(object):
                def __init__(self):
                    for prop in ["flags", "asntype"]:
                        setattr(self, "_{0}".format(prop), props[prop])

                    # Create the ctypes class instance representing the variable
                    # to be handled by the net-snmp C API. If this variable type
                    # has no fixed size, pass the maximum size as second
                    # argument to the constructor.
                    if props["flags"] == WATCHER_FIXED_SIZE:
                        self._cvar      = props["ctype"](initval)
                        self._data_size = ctypes.sizeof(self._cvar)
                        self._max_size  = self._data_size
                    else:
                        self._cvar      = props["ctype"](initval, props["max_size"])
                        self._data_size = len(self._cvar.value)
                        self._max_size  = max(self._data_size, props["max_size"])

                    if oidstr:
                        # Prepare the netsnmp_handler_registration structure.
                        agent._status = netsnmpagent.netsnmpAgentStatus.REGISTRATION
                        self._handler_reginfo = agent._prepareRegistration(oidstr, writable)
                        agent._status = netsnmpagent.netsnmpAgentStatus.CONNECTED
                        self._handler_reginfo.contents.contextName = context

                        # Create the netsnmp_watcher_info structure.
                        self._watcher = libnsX.netsnmp_create_watcher_info(
                            self.cref(),
                            self._data_size,
                            self._asntype,
                            self._flags
                        )

                        # Explicitly set netsnmp_watcher_info structure's
                        # max_size parameter. netsnmp_create_watcher_info6 would
                        # have done that for us but that function was not yet
                        # available in net-snmp 5.4.x.
                        self._watcher.contents.max_size = self._max_size

                        # Register handler and watcher with net-snmp.
                        result = libnsX.netsnmp_register_watched_instance(
                            self._handler_reginfo,
                            self._watcher
                        )
                        if result != 0:
                            raise netsnmpAgentException("Error registering variable with net-snmp!")

                        # Finally, we keep track of all registered SNMP objects for the
                        # getRegistered() method.
                        agent._objs[context][oidstr] = self

                def value(self):
                    val = self._cvar.value
                    if val <= sys.maxint:
                        val = int(val)
                    return val

                def cref(self):
                    return ctypes.byref(self._cvar) if self._flags == WATCHER_FIXED_SIZE \
                                                    else self._cvar

                def update(self, val):
                    if self._asntype == ASN_COUNTER and val >> 32:
                        val = val & 0xFFFFFFFF
                    if self._asntype == ASN_COUNTER64 and val >> 64:
                        val = val & 0xFFFFFFFFFFFFFFFF
                    self._cvar.value = val
                    if props["flags"] == WATCHER_MAX_SIZE:
                        if len(val) > self._max_size:
                            raise netsnmpAgentException(
                                "Value passed to update() truncated: {0} > {1} "
                                "bytes!".format(len(val), self._max_size)
                            )
                        self._cvar.value = val
                        self._data_size  = self._watcher.contents.data_size = len(val)

                if props["asntype"] in [ASN_COUNTER, ASN_COUNTER64]:
                    def increment(self, count=1):
                        self.update(self.value() + count)

            cls.__name__ = property_func.__name__

            # Return an instance of the just-defined class to the agent
            return cls()

        return create_vartype_class

    def start(self):
        libnsa.init_snmp(self.AgentName)
        libnsa.init_master_agent()
        self._status = netsnmpagent.netsnmpAgentStatus.CONNECTED

    def make_config(self, rocommunity = 'public', rwcommunity = 'private', agent_address = 'localhost:1234', informport = 1235):
        self.rocommunity = rocommunity
        self.rwcommunity = rwcommunity
        self.agent_address = agent_address
        self.informport = informport
        self.smuxport = 1236
        self.mastersocket = ""
        self.config_file.seek(0)
        self.config_file.truncate()
        self.config_file.write("rocommunity {0}\n".format(self.rocommunity))
        self.config_file.write("rwcommunity {0}\n".format(self.rwcommunity))
        self.config_file.write("agentaddress {0}\n".format(self.agent_address))
        self.config_file.write("informsink localhost:{0}\n".format(self.informport))
        self.config_file.write("smuxsocket localhost:{0}\n".format(self.smuxport))
        self.config_file.write("iquerySecName {0}\n".format(self.AgentName))
        self.config_file.flush()

    def unregister_all(self):
        for ctxkey, ctxdict in self._objs.iteritems():
            for objkey, objval in ctxdict.iteritems():
                # contextName points to a reference counted object in pythons memory pool, do not bother netsnmp with free()ing it
                objval._handler_reginfo.contents.contextName = None
                libnsa.netsnmp_unregister_handler(objval._handler_reginfo)
                objval._handler_reginfo = None
                objval._watcher = None
        self._objs = defaultdict(dict)

    def shutdown(self):
        super(MasterAgent,self).shutdown()

    def __del__(self):
        if self.config_file:
            self.config_file.close()
        try:
            shutil.rmtree(self.state_dir)  # delete directory
        except OSError as exc:
            if exc.errno != errno.ENOENT:  # ENOENT - no such file or directory
                raise  # re-raise exception

    @InstanceVarTypeClass
    def Integer32Instance(self, initval = None, oidstr = None, writable = True, context = ""):
        return {
            "ctype"         : ctypes.c_long,
            "flags"         : WATCHER_FIXED_SIZE,
            "initval"       : 0,
            "asntype"       : ASN_INTEGER
        }
    @InstanceVarTypeClass
    def Unsigned32Instance(self, initval = None, oidstr = None, writable = True, context = ""):
        return {
            "ctype"         : ctypes.c_ulong,
            "flags"         : WATCHER_FIXED_SIZE,
            "initval"       : 0,
            "asntype"       : ASN_UNSIGNED
        }

    @InstanceVarTypeClass
    def Counter32Instance(self, initval = None, oidstr = None, writable = True, context = ""):
        return {
            "ctype"         : ctypes.c_ulong,
            "flags"         : WATCHER_FIXED_SIZE,
            "initval"       : 0,
            "asntype"       : ASN_COUNTER
        }

    @InstanceVarTypeClass
    def Counter64Instance(self, initval = None, oidstr = None, writable = True, context = ""):
        return {
            "ctype"         : counter64,
            "flags"         : WATCHER_FIXED_SIZE,
            "initval"       : 0,
            "asntype"       : ASN_COUNTER64
        }

    @InstanceVarTypeClass
    def TimeTicksInstance(self, initval = None, oidstr = None, writable = True, context = ""):
        return {
            "ctype"         : ctypes.c_ulong,
            "flags"         : WATCHER_FIXED_SIZE,
            "initval"       : 0,
            "asntype"       : ASN_TIMETICKS
        }

    @InstanceVarTypeClass
    def OctetStringInstance(self, initval = None, oidstr = None, writable = True, context = ""):
        return {
            "ctype"         : ctypes.create_string_buffer,
            "flags"         : WATCHER_MAX_SIZE,
            "max_size"      : netsnmpagent.MAX_STRING_SIZE,
            "initval"       : "",
            "asntype"       : ASN_OCTET_STR
        }

    @InstanceVarTypeClass
    def DisplayStringInstance(self, initval = None, oidstr = None, writable = True, context = ""):
        return {
            "ctype"         : ctypes.create_string_buffer,
            "flags"         : WATCHER_MAX_SIZE,
            "max_size"      : netsnmpagent.MAX_STRING_SIZE,
            "initval"       : "",
            "asntype"       : ASN_OCTET_STR
        }
