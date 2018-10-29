# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from .event import Event
from .dispatch import Dispatch
from .user import User
from slackclient import SlackClient as _SlackClient
from slack_g_cal.wit import wit_client
from slack_g_cal.raven import raven_client


class SlackClient(_SlackClient):
    def __init__(self, *args, **kwargs):
        super(SlackClient, self).__init__(*args, **kwargs)
        bot_info = self.api_call('auth.test')
        self.bot_id = bot_info['user_id']
        self.bot_name = bot_info['user']
        self.dispatch = Dispatch()

    def get_user_data(self, tgt_user_id):
        api_res = self.api_call('users.info', user=tgt_user_id)
        return User(**api_res['user'])

    def handle_cb(self, cb_json):
        # We pass "self" here so event can make Slack API calls
        event = Event(self, cb_json['event'])
        if self.should_process(event):
            self.process(event)

    def should_process(self, event):
        return not event.sender.is_bot

    def process(self, event):
        """
        Uses the Wit.ai library to determine what command to execute based on user-inputted text our bot receives
        """
        try:
            wit_res = wit_client.message(event.clean_text)
            msg = self.dispatch(wit_res, event)
        except Exception:
            raven_client.captureException()
            msg = self.dispatch.error(event=event)
        self.send_response(msg)

    def send_response(self, msg):
        self.api_call('chat.postMessage', **msg.kwargs)
