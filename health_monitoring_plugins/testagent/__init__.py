"""
This package provides a standalone SNMP Master Agent.
It can be used as stub/mock during unit and integration tests.
It is based on the open source work from https://github.com/pief/python-netsnmpagent.
"""

import os
import threading
import time

# from testagent
import eventloop
import masteragent
import snmp_fd
import re

def _log_handler(priority, message):
    """Discard netsnmp log messages."""
    pass

def _wrap_locked(func):
    def inner(*arg, **kwarg):
        with ModuleVars.lock:
            ret_obj = func(*arg, **kwarg)
        return ret_obj
    return inner

def configure(**kwargs):
    """Set some configuration paramters for the agent.
    
    Changed parameters will only take effect after you (re-)start the agent.
    
    Args:
        agent_address (str): "localhost:1234"
        rocommunity (str): "public"
        rwcommunity (str): "private"
    """
    ModuleVars.agentName = "testagent"
    ModuleVars.agent = masteragent.MasterAgent(
        AgentName      = ModuleVars.agentName,
        MIBFiles       = kwargs.get("MIBFiles"),
        LogHandler     = _log_handler,
    )
    cfg_kwarg = dict()
    if 'agent_address' in kwargs:
        cfg_kwarg['agent_address'] = kwargs['agent_address']
    if 'rocommunity' in kwargs:
        cfg_kwarg['rocommunity'] = kwargs['rocommunity']
    if 'rwcommunity' in kwargs:
        cfg_kwarg['rwcommunity'] = kwargs['rwcommunity']
    ModuleVars.agent.make_config(**cfg_kwarg)

def start_server():
    """Start request processing in the agent event loop.

    Previously registered OIDs will be restored after stop_server - start_server cycles.
    """
    ModuleVars.thread.start()
    while not ModuleVars.evt_loop.is_running():
        time.sleep(0.1)

def stop_server():
    """Stop request processing and wait blocking until agent thread has stopped."""
    if ModuleVars.evt_loop.is_running():
        ModuleVars.pipe_w.write("stop")
        ModuleVars.pipe_w.flush()
        ModuleVars.thread.join()
        ModuleVars.agent.shutdown()
        ModuleVars.pipe_w.close()

def Integer32(initval = None, oidstr = None, writable = True, context = ""):
    """Create scalar of ASN type INTEGER.
    This appends a .0 to your OID.
    Registered using netsnmp_register_watched_scalar internally."""
    varobj = ModuleVars.agent.Integer32(initval, oidstr, writable, context)
    varobj.update = _wrap_locked(varobj.update)
    varobj.value = _wrap_locked(varobj.value)
    return varobj

def Integer32Instance(initval = None, oidstr = None, writable = True, context = ""):
    """Create instance of ASN type INTEGER.
    Registered using netsnmp_register_watched_instance internally."""
    varobj = ModuleVars.agent.Integer32Instance(initval, oidstr, writable, context)
    varobj.update = _wrap_locked(varobj.update)
    varobj.value = _wrap_locked(varobj.value)
    return varobj

def Unsigned32(initval = None, oidstr = None, writable = True, context = ""):
    """Create scalar of ASN type UNSIGNED.
    This appends a .0 to your OID.
    Registered using netsnmp_register_watched_scalar internally."""
    varobj = ModuleVars.agent.Unsigned32(initval, oidstr, writable, context)
    varobj.update = _wrap_locked(varobj.update)
    varobj.value = _wrap_locked(varobj.value)
    return varobj

def Unsigned32Instance(initval = None, oidstr = None, writable = True, context = ""):
    """Create scalar of ASN type UNSIGNED.
    This appends a .0 to your OID.
    Registered using netsnmp_register_watched_scalar internally."""
    varobj = ModuleVars.agent.Unsigned32Instance(initval, oidstr, writable, context)
    varobj.update = _wrap_locked(varobj.update)
    varobj.value = _wrap_locked(varobj.value)
    return varobj

def Counter32(initval = None, oidstr = None, writable = True, context = ""):
    """Create scalar of ASN type COUNTER.
    This appends a .0 to your OID.
    Registered using netsnmp_register_watched_scalar internally."""
    varobj = ModuleVars.agent.Counter32(initval, oidstr, writable, context)
    varobj.update = _wrap_locked(varobj.update)
    varobj.value = _wrap_locked(varobj.value)
    return varobj

def Counter32(initval = None, oidstr = None, writable = True, context = ""):
    """Create scalar of ASN type COUNTER.
    This appends a .0 to your OID.
    Registered using netsnmp_register_watched_scalar internally."""
    varobj = ModuleVars.agent.Counter32Instance(initval, oidstr, writable, context)
    varobj.update = _wrap_locked(varobj.update)
    varobj.value = _wrap_locked(varobj.value)
    return varobj

def Counter64(initval = None, oidstr = None, writable = True, context = ""):
    """Create scalar of ASN type COUNTER64.
    This appends a .0 to your OID.
    Registered using netsnmp_register_watched_scalar internally."""
    varobj = ModuleVars.agent.Counter64(initval, oidstr, writable, context)
    varobj.update = _wrap_locked(varobj.update)
    varobj.value = _wrap_locked(varobj.value)
    return varobj

def Counter64Instance(initval = None, oidstr = None, writable = True, context = ""):
    """Create scalar of ASN type COUNTER64.
    This appends a .0 to your OID.
    Registered using netsnmp_register_watched_scalar internally."""
    varobj = ModuleVars.agent.Counter64Instance(initval, oidstr, writable, context)
    varobj.update = _wrap_locked(varobj.update)
    varobj.value = _wrap_locked(varobj.value)
    return varobj

def TimeTicks(initval = None, oidstr = None, writable = True, context = ""):
    """Create scalar of ASN type TIMETICKS.
    This appends a .0 to your OID.
    Registered using netsnmp_register_watched_scalar internally."""
    varobj = ModuleVars.agent.TimeTicks(initval, oidstr, writable, context)
    varobj.update = _wrap_locked(varobj.update)
    varobj.value = _wrap_locked(varobj.value)
    return varobj

def OctetString(initval = None, oidstr = None, writable = True, context = ""):
    """Create scalar of ASN type OCTET_STR.
    This appends a .0 to your OID.
    Registered using netsnmp_register_watched_scalar internally."""
    varobj = ModuleVars.agent.OctetString(initval, oidstr, writable, context)
    varobj.update = _wrap_locked(varobj.update)
    varobj.value = _wrap_locked(varobj.value)
    return varobj

def OctetStringInstance(initval = None, oidstr = None, writable = True, context = ""):
    """Create scalar of ASN type OCTET_STR.
    This appends a .0 to your OID.
    Registered using netsnmp_register_watched_scalar internally."""
    varobj = ModuleVars.agent.OctetStringInstance(initval, oidstr, writable, context)
    varobj.update = _wrap_locked(varobj.update)
    varobj.value = _wrap_locked(varobj.value)
    return varobj

def DisplayString(initval = None, oidstr = None, writable = True, context = ""):
    """Create scalar of ASN type OCTET_STR.
    This appends a .0 to your OID.
    Registered using netsnmp_register_watched_scalar internally."""
    varobj = ModuleVars.agent.DisplayString(initval, oidstr, writable, context)
    varobj.update = _wrap_locked(varobj.update)
    varobj.value = _wrap_locked(varobj.value)
    return varobj

def IpAddress(initval = "0.0.0.0", oidstr = None, writable = True, context = ""):
    """Create scalar of ASN type IPADDRES.
    This appends a .0 to your OID.
    Registered using netsnmp_register_watched_scalar internally."""
    varobj = ModuleVars.agent.IpAddress(initval, oidstr, writable, context)
    varobj.update = _wrap_locked(varobj.update)
    varobj.value = _wrap_locked(varobj.value)
    return varobj

def Table(oidstr, indexes, columns, counterobj = None, extendable = False, context = ""):
    table = ModuleVars.agent.Table(oidstr, indexes, columns, counterobj, extendable, context)
    table.addRow = _wrap_locked(table.addRow)
    table.value = _wrap_locked(table.value)
    table.clear = _wrap_locked(table.clear)
    return table

def register_snmpwalk_ouput(walk_str):
    """"Parse the output from snmpget and setup OIDs accordinly
    This is hardly tested. Use snmpget -On -Oe."""
    p = re.compile('^[\s]*([\w\d.\-:]+)[\s]*=[\s]*([\w\d]+):[\s]*(.+)$')
    for line in walk_str.splitlines():
        m = p.search(line)
        if m:
            oid_str = m.group(1)
            type = m.group(2)
            value = m.group(3).strip('"').rstrip('"')
            if type == 'INTEGER':
                Integer32Instance(initval=int(value), oidstr=oid_str)
            elif type == 'Unsigned32':
                Unsigned32Instance(initval=int(value), oidstr=oid_str)
            elif type == 'Counter32':
                Counter32Instance(initval=int(value), oidstr=oid_str)
            elif type == 'Counter64':
                Counter64Instance(initval=int(value), oidstr=oid_str)
            elif type == 'Timeticks':
                pass
            elif type == 'IpAddress':
                pass
            elif type == 'OID':
                pass
            elif type == 'STRING':
                OctetStringInstance(initval=value, oidstr=oid_str)
            elif type == 'BITS':
                pass

def unregister_all():
    ModuleVars.agent.unregister_all()

def _thread_io_hnd(stopfunc):
    stopfunc()

def _netsnmp_hnd(stopfunc):
    with ModuleVars.lock:
        ModuleVars.agent.check_and_process(False)
    _setup_fd()

def _setup_fd():
    del ModuleVars.evt_loop.readfds[:]
    ModuleVars.evt_loop.set_default_handler(_netsnmp_hnd)
    ModuleVars.evt_loop.add_handler(ModuleVars.pipe_r.fileno(), _thread_io_hnd)
    for fd in snmp_fd.netsnmp_event_fd():
        ModuleVars.evt_loop.add_default_fd(fd)

def _exec():
    """Start event loop in agent thread."""
    try:
        r, w = os.pipe()
        ModuleVars.pipe_r = os.fdopen(r, 'r')
        ModuleVars.pipe_w = os.fdopen(w, 'w')
        ModuleVars.agent.start()
    except netsnmpagent.netsnmpAgentException as e:
        # End thread
        return
    _setup_fd()
    # runs until someone calls stop_server()
    ModuleVars.evt_loop.run()
    # event loop stopped now
    ModuleVars.pipe_r.close()

class ModuleVars:
    agent = None
    agentName = "MasterAgentSimulator"
    thread = threading.Thread(target = _exec)
    lock = threading.Lock()
    evt_loop = eventloop.EventLoop()
    pipe_w = None
    pipe_r = None
