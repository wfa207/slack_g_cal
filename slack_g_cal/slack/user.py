# -*- encoding: utf-8 -*-
from __future__ import unicode_literals


from slack_g_cal.parse import JSON


class User(JSON):
    def __init__(self, **user_data):
        """ Converts Slack User data to portable class to be used throughout bot """
        # Pop off profile to over-write any identically-named fields we might get in the first layer
        profile = user_data.pop('profile')
        super(User, self).__init__(**user_data)

        # Brings profile attributes to first-level
        super(User, self).__init__(**profile)
