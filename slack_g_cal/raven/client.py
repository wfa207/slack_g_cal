# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from os import environ
from raven import Client


class RavenClient(Client):
    def __init__(self, dsn_key, *args, **kwargs):
        self.has_dsn_key = bool(dsn_key)
        super(RavenClient, self).__init__(dsn_key, *args, **kwargs)

    def captureException(self, *args, **kwargs):
        if self.has_dsn_key:
            super(RavenClient, self).captureException(*args, **kwargs)
        else:
            print 'Exception encountered! Enable Sentry by including a `SENTRY_DSN` environment variable'


raven_client = RavenClient(environ.get('SENTRY_DSN'))
