# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os import environ, path
from .client import GoogleCalClient


SCOPES = ['https://www.googleapis.com/auth/calendar']
GOOGLE_AUTH_FILENAME = environ['GOOGLE_AUTH_FILENAME']
GOOGLE_AUTH_FILEPATH = path.abspath(path.join(path.dirname(__file__), './{}'.format(GOOGLE_AUTH_FILENAME)))

g_cal_client = GoogleCalClient(GOOGLE_AUTH_FILEPATH, SCOPES)
