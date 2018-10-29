# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from slack_g_cal.slack import slack_client
from slack_g_cal.raven import raven_client

from .celery import app


@app.task()
def process_msg(req_json):
    try:
        slack_client.handle_cb(req_json)
    except Exception:
        raven_client.captureException()
