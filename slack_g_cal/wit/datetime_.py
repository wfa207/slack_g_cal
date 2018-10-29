# -*- encoding: utf-8 -*-
from __future__ import unicode_literals


from slack_g_cal.parse import JSON, Datetime


class WitDatetimeContainer(JSON):
    """ Container wrapping datetime values from the Wit API """
    def __init__(self, **dt_json):
        self.is_interval = dt_json['type'] == 'interval'
        # Get rid of values; we don't need this parameter
        dt_json.pop('values', None)
        if self.is_interval:
            from_, to_ = dt_json.pop('from'), dt_json.pop('to')
            self.dt_from = WitDatetime(date_input=from_.value, grain=from_.grain)
            self.dt_to = WitDatetime(date_input=to_.value, grain=to_.grain)
        else:
            self.date = WitDatetime(date_input=dt_json.pop('value'), grain=dt_json.pop('grain'))
        super(WitDatetimeContainer, self).__init__(**dt_json)


class WitDatetime(Datetime):
    def __init__(self, date_input, **dt_json):
        self.grain = dt_json.pop('grain')
        super(WitDatetime, self).__init__(date_input=date_input, **dt_json)

    def adjust_grain_by(self, adj_val):
        kwargs = {self.grain: getattr(self._datetime, self.grain) + adj_val}
        self._datetime = self._datetime.replace(**kwargs)
