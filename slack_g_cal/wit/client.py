# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from os import environ
from wit import Wit
from .response import MessageResponse


class _Wit(Wit):
    def __init__(self, *args, **kwargs):
        super(_Wit, self).__init__(*args, **kwargs)

    def message(self, *args, **kwargs):
        return MessageResponse(**super(_Wit, self).message(*args, **kwargs))


wit_client = _Wit(environ['WIT_ACCESS_TOKEN'])
