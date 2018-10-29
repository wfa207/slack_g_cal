# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from os import environ

from client import SlackClient

slack_client = SlackClient(environ['SLACK_BOT_TOKEN'])
