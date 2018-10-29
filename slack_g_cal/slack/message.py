# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import json


class Message(object):
    def __init__(self, event=None, **kwargs):
        """ Class that builds a message JSON object that is compatible with the Slack API """
        self._json = kwargs
        if event:
            self.at_mention = '' if event.is_direct_msg else '<@{}> '.format(event.user_id)
            self._json.update({
                'text': '{}{}'.format(self.at_mention, kwargs.pop('text', '')),
                'channel': event.channel
            })

        # Attachments must be serialized json strings
        if 'attachments' in self._json:
            self._json['attachments'] = json.dumps(self._json['attachments'])

    @property
    def kwargs(self):
        """ Attribute to pass to api call """
        if ('text' not in self._json and 'attachments' not in self._json) or 'channel' not in self._json:
            return None
        return self._json

    def _get_rand_item(self, input_iter):
        from random import randint
        return input_iter[randint(0, len(input_iter) - 1)]


class _BaseStockMessage(Message):
    def __init__(self, **kwargs):
        text = kwargs.pop('text', self._get_rand_item(self.text_options))
        attachments = kwargs.pop('attachments', [{}])
        base_attachments = {attr_: getattr(self, attr_) for attr_ in ('image_url', 'fallback') if hasattr(self, attr_)}
        for attachment in attachments:
            attachment.update(base_attachments)

        super(_BaseStockMessage, self).__init__(text=text, **kwargs)


class SuccessMessage(_BaseStockMessage):
    text_options = ('We\'re good to go!', 'No problem!', 'OK!', 'Yup!')


class GreetMessage(_BaseStockMessage):
    text_options = ('Hello!', 'Hi!', 'What\'s up?')


class YWMessage(_BaseStockMessage):
    text_options = ('Of course!', 'You\'re welcome!', 'No prob!', 'Anytime!')


class ErrorMessage(_BaseStockMessage):
    text_options = (
        "Sorry I'm not sure I know how to help with that.",
        "`ERROR! ERR` — just kidding, but seriously, I'm not sure what to do.",
        "Hmm... I'm not sure I understand what it is you want.",
    )
