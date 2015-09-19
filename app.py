#!/usr/bin/python

import os
import requests
import csv
import pprint
import json

from requests.auth import HTTPBasicAuth

from gunicorn.app.base import BaseApplication
from gunicorn.six import iteritems

def wsgi_handler(environ, start_response):

    apiUrl = 'http://192.168.0.101:1936/haproxy?stats;csv'

    auth = HTTPBasicAuth('admin', 'redhat')
    r = requests.get( url=apiUrl, auth=auth )

    fieldnames = ('pxname', 'svname', 'qcur', 'qmax', 'scur', 'smax', 'slim', 'stot', 'bin', 'bout', 'dreq', 'dresp', 'ereq', 'econ', 'eresp', 'wretr', 'wredis', 'status', 'weight', 'act', 'bck', 'chkfail', 'chkdown', 'lastchg', 'downtime', 'qlimit', 'pid', 'iid', 'sid', 'throttle', 'lbtot', 'tracked', 'type', 'rate', 'rate_lim', 'rate_max', 'check_status', 'check_code', 'check_duration', 'hrsp_1xx', 'hrsp_2xx', 'hrsp_3xx', 'hrsp_4xx', 'hrsp_5xx', 'hrsp_other', 'hanafail', 'req_rate', 'req_rate_max', 'req_tot', 'cli_abrt', 'srv_abrt', 'comp_in', 'comp_out', 'comp_byp', 'comp_rsp', 'lastsess', 'last_chk', 'last_agt', 'qtime', 'ctime', 'rtime', 'ttime', '')
    reader = csv.DictReader(r.text.splitlines(), fieldnames)

    out = '<html>Routes found:<br>'
    for row in reader:
        if row['pxname'].startswith('be_http_'):
            out += row['pxname'].split('_', 2)[-1].replace('-','/',1) + '<br>'

    out += '</html>'

    start_response('200 OK', [('Content-Type','text/html')])
    return out

class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == '__main__':

    # apiUrl = 'http://85.190.178.15:1936/haproxy?stats;csv'
    #
    # auth = HTTPBasicAuth('admin', 'redhat')
    # r = requests.get( url=apiUrl, auth=auth )
    #
    # fieldnames = ('pxname', 'svname', 'qcur', 'qmax', 'scur', 'smax', 'slim', 'stot', 'bin', 'bout', 'dreq', 'dresp', 'ereq', 'econ', 'eresp', 'wretr', 'wredis', 'status', 'weight', 'act', 'bck', 'chkfail', 'chkdown', 'lastchg', 'downtime', 'qlimit', 'pid', 'iid', 'sid', 'throttle', 'lbtot', 'tracked', 'type', 'rate', 'rate_lim', 'rate_max', 'check_status', 'check_code', 'check_duration', 'hrsp_1xx', 'hrsp_2xx', 'hrsp_3xx', 'hrsp_4xx', 'hrsp_5xx', 'hrsp_other', 'hanafail', 'req_rate', 'req_rate_max', 'req_tot', 'cli_abrt', 'srv_abrt', 'comp_in', 'comp_out', 'comp_byp', 'comp_rsp', 'lastsess', 'last_chk', 'last_agt', 'qtime', 'ctime', 'rtime', 'ttime', '')
    # reader = csv.DictReader(r.text.splitlines(), fieldnames)


    # out = ''
    # for row in reader:
    #     if row['pxname'].startswith('be_http_'):
    #         out += row['pxname'].split('_', 2)[-1].replace('-','/',1) + '<br>'
    # #
    # # for row in reader:
    # #     if row['pxname'].startswith('be_http_'):
    # #         print( row['pxname'].split('_', 2)[-1].replace('-','/',1) )
    #
    # print(out)

    StandaloneApplication(wsgi_handler, {'bind': ':8080'}).run()
