# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import re

from slack_g_cal.parse import JSON


class Event(JSON):
    def __init__(self, slack_client, event_json):
        # Build JSON fields
        super(Event, self).__init__(**event_json)

        self.slack_client = slack_client

        # Get sender information along with other fields
        self.sender = self.slack_client.get_user_data(self.user)
        self.bot_id = self.slack_client.bot_id
        self.is_direct_msg = self.type == 'message'
        self.clean_text = self._get_clean_text()

        self.at_mentions = self._get_mentioned_users()

    def _get_clean_text(self):
        return self.text.replace(self.bot_id, '').replace("\u2019", "'").strip().lower()

    def _get_mentioned_users(self):
        res = []
        user_ids = re.findall(r'<@(U[0-9A-Z]+)>', self.text)

        for user_id in user_ids:
            parsed_user = self.slack_client.get_user_data(user_id)
            # TODO: UNCOMMENT THIS
            #  if not parsed_user.is_bot:
            res.append(parsed_user)

        return res
