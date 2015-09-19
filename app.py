#!/usr/bin/python

import os
import requests

from requests.auth import HTTPBasicAuth

from gunicorn.app.base import BaseApplication
from gunicorn.six import iteritems

def wsgi_handler(environ, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World!"]

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
    # # print( apiUrl )
    # auth = HTTPBasicAuth('admin', 'redhat')
    # r = requests.get( url=apiUrl, auth=auth )
    #
    # print( r.text )
    #
    StandaloneApplication(wsgi_handler, {'bind': ':8080'}).run()
