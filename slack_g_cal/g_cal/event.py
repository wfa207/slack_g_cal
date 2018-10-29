# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from slack_g_cal.parse import JSON, Datetime


class Event(JSON):
    def __init__(self, **event_json):
        self.datetime_keys = (
            'created',
            'end',
            'original_start_time',
            'start',
            'updated',
        )

        self.attendees = []
        self.resources = []

        self._parse_datetime_props(event_json)  # Removes datetime keys from event_json
        self._attendees = event_json.pop('attendees', [])
        self._parse_attendees()

        super(Event, self).__init__(**event_json)

    def _parse_attendees(self):
        for attendee in self._attendees:
            attendee_json = JSON(**attendee)
            if attendee.get('resource'):
                self.resources.append(attendee_json)
            else:
                self.attendees.append(attendee_json)

    def _parse_datetime_props(self, event_json):
        for key in self.datetime_keys:
            if key in event_json:
                val = event_json.pop(key)
                setattr(self, key, Datetime(val))

    @property
    def room(self):
        return self.resources[0].display_name if self.resources else None
