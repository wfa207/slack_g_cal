# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from google.oauth2 import service_account
from googleapiclient import discovery
from .event import Event
from .datetime_ import GoogleDatetime, GoogleDate


class GoogleCalClient(object):
    def __init__(self, auth_file_path, scopes, **kwargs):
        super(GoogleCalClient, self).__init__()
        self.credentials = service_account.Credentials.from_service_account_file(auth_file_path,
                                                                                 scopes=scopes)
        # TODO: Think about inheriting from the Resource class; Google doesn't provide an easy way to do this atm
        self.service = discovery.build('calendar', 'v3', credentials=self.credentials)

    def create_event(self, wit_res, slack_event):
        google_event = {
            'summary': self._get_event_summary(wit_res, slack_event),
            'attendees': self._get_attendees(wit_res, slack_event),
            'reminders': {'useDefault': False},
        }

        wit_dt = wit_res.datetime
        if wit_dt.is_interval:
            dt_key = 'dateTime'
            start_dt = GoogleDatetime(wit_dt.dt_from())
            wit_dt.dt_to.adjust_grain_by(-1)
            end_dt = GoogleDatetime(wit_dt.dt_to())
        else:
            dt_key = 'date'
            api_date = wit_dt.date()
            start_dt = GoogleDate(api_date)
            end_dt = GoogleDate(api_date)

        google_event.update({
            'start': {
                dt_key: start_dt(),
                'timeZone': slack_event.sender.tz,
            },
            'end': {
                dt_key: end_dt(),
                'timeZone': slack_event.sender.tz,
            },
        })

        res = self.service.events().insert(calendarId=slack_event.sender.email, body=google_event).execute()
        return Event(**res)

    def get_next_event(self, wit_res, slack_event):
        time_now = GoogleDatetime(now=True)
        events = self.service.events().list(calendarId=slack_event.sender.email,
                                            orderBy='startTime',
                                            singleEvents=True,
                                            timeMin=time_now(tz=True)).execute()

        try:
            return Event(**events['items'][0])
        except (IndexError, KeyError):
            return None

    def _get_event_summary(self, wit_res, slack_event):
        if hasattr(wit_res, 'message_subject'):
            return wit_res.message_subject.value
        else:
            return 'Event created via Slack'

    def _get_attendees(self, wit_res, slack_event):
        res = [{'email': slack_event.sender.email}]
        if hasattr(wit_res, 'contact'):
            res += [{'email': user.email} for user in slack_event.at_mentions]

        return res
