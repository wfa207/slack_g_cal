# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import re

from dateutil.parser import parse
from .exceptions import NoInputDateError


class Datetime(object):
    def __init__(self, date_input=None, now=False):
        if not now and date_input is None:
            raise NoInputDateError

        if isinstance(date_input, dict):
            self._date_str = date_input.get('dateTime') or date_input['date']
        else:
            self._date_str = date_input
        self._datetime = datetime.datetime.utcnow() if now else parse(self._date_str)

    def __call__(self):
        return self.date_str

    @property
    def date_str(self):
        raw_datetime_str = self._datetime.strftime('%A, %B %d at %I:%M%p')
        return re.sub(r'(?<!:)\b0([0-9]+)', r'\1', raw_datetime_str)


class JSON(object):
    def __init__(self_, **kwargs):
        """ Converts a JSON dict into a class that will recursively chain nested fields"""
        while kwargs:
            key, val = kwargs.popitem()
            fmted_key = re.sub(r'([a-z])([A-Z])', r'\1_\2', key).lower()
            self_.set_prop(fmted_key, val)

    def set_prop(self_, fmted_key, val):
        if isinstance(val, dict):
            setattr(self_, fmted_key, JSON(**val))
        else:
            setattr(self_, fmted_key, val)
