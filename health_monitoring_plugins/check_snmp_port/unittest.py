#!/usr/bin/python
from check_snmp_port import *
import pytest
import unittest


def test_get():
    assert get_data("1.2.3.4", 2, "public", ".1") == None    
    assert get_data("localhost", 2, "public", ".1.3.6.1.2.1.25.1.5.0") == "1"

def test_walk_data():
    assert walk_data("1.2.3.4", 2, "public", ".1") == ()
    assert walk_data("localhost", 2, "public", ".1.3.6.1.2.1.25.1.5")[0] == "1"

def test_check_typ(capsys):
    with pytest.raises(SystemExit):
        check_typ(helper, "test")
    out, err = capsys.readouterr()    
    assert out == "Unknown - Type (-t) must be udp or tcp.\n"
        
    assert check_typ(helper, "tcp") == None
    assert check_typ(helper, "udp") == None
    
def test_check_port(capsys):
    with pytest.raises(SystemExit):
        check_port(helper, "test")
    out, err = capsys.readouterr()    
    assert out == "Unknown - Port (-p) must be a integer value or 'scan'.\n"
        
    assert check_port(helper, "22") == None
    assert check_port(helper, "scan") == None

def test_check_udp(capsys):
    # check "scan"
    with pytest.raises(SystemExit):
        check_udp(helper, "127.0.0.1", 2, "public", "scan")
    out, err = capsys.readouterr()    
    assert "UDP" in out
    
    # check "161" (open)
    assert check_udp(helper, "127.0.0.1", 2, "public", "161") == "Current status for UDP port 161 is: OPEN"
    
    # check "164" (closed)
    assert check_udp(helper, "127.0.0.1", 2, "public", "164") == "Current status for UDP port 164 is: CLOSED"

    # check "test"
    assert check_udp(helper, "127.0.0.1", 2, "public", "test") == "Current status for UDP port test is: CLOSED"
    


# we need to test the main function