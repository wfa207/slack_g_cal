# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import re

from slack_g_cal.g_cal import g_cal_client
from slack_g_cal.slack.message import Message, GreetMessage, YWMessage, ErrorMessage


class Dispatch(object):
    def __init__(self, *args, **kwargs):
        super(Dispatch, self).__init__(*args, **kwargs)

    def __call__(self, wit_res, event):
        if re.search(r'\bth+a+n+k+s*\b', event.clean_text):
            cmd_name = 'thanks'
        elif self.is_hello_cmd(event.clean_text):
            cmd_name = 'hi'
        else:
            cmd_name = wit_res.intent.value

        return getattr(self, cmd_name)(wit_res, event)

    def is_hello_cmd(self, clean_text):
        re_match = re.search(r'h+i+\b|h+e+y+\b|h+e+l+o+\b', clean_text)
        return bool(re_match) and re_match.endpos == len(clean_text)

    def schedule(self, wit_res, event):
        scheduled_event = g_cal_client.create_event(wit_res, event)
        kwargs = self._get_base_cal_kwargs(event)
        kwargs.update(self._format_attm(scheduled_event,
                                        pretext='Your event has been scheduled!',
                                        fallback='Summary of your new event'))
        return Message(**kwargs)

    def next(self, wit_res, event):
        next_event = g_cal_client.get_next_event(wit_res, event)
        kwargs = self._get_base_cal_kwargs(event)

        if next_event:
            kwargs.update(self._format_attm(next_event,
                                            pretext='Your next event is as follows:',
                                            fallback='Summary of upcoming event'))
        else:
            kwargs.update({'text': 'Looks like your schedule\'s all clear!'})

        return Message(**kwargs)

    def hi(self, wit_res, event):
        return GreetMessage(event=event)

    def thanks(self, wit_res, event):
        return YWMessage(event=event)

    def error(self, **kwargs):
        return ErrorMessage(**kwargs)

    # ======== PRIVATE METHODS ========
    def _get_base_cal_kwargs(self, event):
        return {
            'event': event,
            'as_user': True,
        }

    def _format_attm(self, event_obj, **addl_fields):
        return {
            'attachments': [dict({
                'title': event_obj.summary,
                'author_name': 'Google Calendar',
                'author_link': 'https://calendar.google.com/calendar/r',
                'author_icon': 'https://www.gstatic.com/images/branding/product/2x/calendar_48dp.png',
                'fields': [{
                    'title': label,
                    'value': value,
                    'short': True,
                } for label, value in (
                    ('Begins', event_obj.start()),
                    ('Ends', event_obj.end()),
                    ('Room', event_obj.room)
                ) if value is not None]
            }, **addl_fields)]
        }
