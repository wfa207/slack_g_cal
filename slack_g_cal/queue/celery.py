# -*- encoding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from os import environ
from celery import Celery

BROKER_URL = environ['BROKER_URL']


app = Celery('slack_g_cal.queue', broker=BROKER_URL, include=['slack_g_cal.queue.tasks'])


if __name__ == '__main__':
    app.start()
