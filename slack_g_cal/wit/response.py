# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from slack_g_cal.parse import JSON
from .datetime_ import WitDatetimeContainer


class MessageResponse(JSON):
    """ Container wrapping responses from the Message API """
    def __init__(self, **res_json):
        self.datetime_keys = ['datetime']

        entities = res_json.pop('entities')
        super(MessageResponse, self).__init__(**dict(res_json, **entities))
        self._parse_dt_props()

    def _parse_dt_props(self):
        for key in self.datetime_keys:
            if hasattr(self, key):
                dt_json = getattr(self, key).__dict__
                setattr(self, key, WitDatetimeContainer(**dt_json))

    def set_prop(self, fmted_key, val):
        if isinstance(val, list):
            val_to_set = self.get_highest_confidence_field(val)
            super(MessageResponse, self).set_prop(fmted_key, val_to_set)
        else:
            super(MessageResponse, self).set_prop(fmted_key, val)

    def get_highest_confidence_field(self, field_):
        """ Returns the value with the highest confidence if there is more tha one """
        if field_ is not None and isinstance(field_, list):
            res = field_[0]
            for dict_ in field_:
                res = dict_ if dict_['confidence'] > res['confidence'] else res
            return res
        elif isinstance(field_, str):
            return field_
