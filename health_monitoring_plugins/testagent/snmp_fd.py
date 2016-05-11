import ctypes
import netsnmpapi

class fd_set(ctypes.Structure):
    _fields_ = [('fds_bits', ctypes.c_long * 32)]

class Timeval(ctypes.Structure):
    _fields_ = [("tv_sec", ctypes.c_long), ("tv_usec", ctypes.c_long)]

def FD_SET(fd, fd_set):
    """Set fd in fd_set, where fd can may be in range of 0..FD_SETSIZE-1 (FD_SETSIZE is 1024 on Linux)."""
    l64_offset = fd / 64
    bit_in_l64_idx = fd % 64;
    fd_set.fds_bits[l64_offset] = fd_set.fds_bits[l64_offset] | (2**bit_in_l64_idx)

def FD_ISSET(fd, fd_set):
    """Check if fd is in fd_set."""
    l64_offset = fd / 64
    bit_in_l64_idx = fd % 64;
    if fd_set.fds_bits[l64_offset] & (2**bit_in_l64_idx) > 0:
        return True
    return False

def netsnmp_event_fd():
    """Return each netsnmp file descriptor by number."""
    maxfd = ctypes.c_int(0)
    fdset = fd_set()
    timeval = Timeval(0, 0)
    fakeblock = ctypes.c_int(1)
    netsnmpapi.libnsa.snmp_select_info(
        ctypes.byref(maxfd),
        ctypes.byref(fdset),
        ctypes.byref(timeval),
        ctypes.byref(fakeblock)
    )
    for fd in range(0, maxfd.value):
        if FD_ISSET(fd, fdset):
            yield fd
