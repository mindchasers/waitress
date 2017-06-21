#!/usr/bin/python3

import os, sys
import syslog
import argparse
import signal

import waitress

""" 
    This script won't work on Windows
    
    Waitress is able to listen on multiple sockets, 
    including IPv4 and IPv6. Instead of passing in a host/port combination 
    provide waitress with a space delineated list, and it will create as many sockets as required. 
"""

nodename = os.uname()[1]
if 'macmini' in nodename:
    sys.path.append('/Users/bcochran/Development/web-eraser')
    Linux = False
else:
    sys.path.append('/build/web-eraser')
    Linux = True

from wsgi import wsgi_middleware
from daemonize import Daemonize
    
VERSION = '0.2'     # uses daemonize instead of daemon


def waitress_daemon(address=['192.168.3.24:8000']):
    waitress.serve(wsgi_middleware.application, listen=address)
    
if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    parser = argparse.ArgumentParser(description='waitress web server', 
                                 epilog='Version: ' + VERSION)
    parser.add_argument('-d','--daemonize',help='daemonize the program',action='store_true')
    parser.add_argument('-v','--verbose',help='verbose output to standard out',action='store_true')    
    parser.add_argument('-a','--address',help='the last byte of the ip address',action='store')    
    args = parser.parse_args()


    if 'macmini' in nodename:
        address = ['192.168.3.24:8000']
    else:
        if args.address:
            address = '192.168.3.'+args.address+':80'
        else:
            address = '192.168.3.1:80'
        address = address + ' 127.0.0.1:80 '
    
    if args.daemonize:
        #pid = "/var/run/waitress.pid"
        pid = "/tmp/waitress.pid"
        daemon = Daemonize(app="waitress", pid=pid, action=waitress_daemon, auto_close_fds=False)
        daemon.start()
   
    else:
        syslog.openlog('waitress',logoption=syslog.LOG_PID)
        waitress.serve(wsgi_middleware.application, listen=address)
