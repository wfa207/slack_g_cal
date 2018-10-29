# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import re

from slack_g_cal.parse import Datetime


class GoogleDatetime(Datetime):
    def __init__(self, *args, **kwargs):
        super(GoogleDatetime, self).__init__(*args, **kwargs)

    def __call__(self, tz=False):
        if not tz:
            return self._datetime.strftime('%Y-%m-%dT%H:%M:%S')

        raw_str = self._datetime.strftime('%Y-%m-%dT%H:%M:%S%z')
        if self._datetime.tzinfo is None:
            return raw_str + '-00:00'
        else:
            return re.sub(r'([+-])([0-9]{2})([0-9]{2})$', r'\1\2:\3', raw_str)


class GoogleDate(Datetime):
    def __init__(self, *args, **kwargs):
        super(GoogleDate, self).__init__(*args, **kwargs)

    def __call__(self):
        return self._datetime.strftime('%Y-%m-%d')
