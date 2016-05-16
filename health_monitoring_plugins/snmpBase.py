#!/usr/bin/python
if __name__ == "__main__":
    
    # verify that a hostname is set
    if host == "" or host is None:
        helper.exit(summary="Hostname must be specified", exit_code=unknown, perfdata='')
