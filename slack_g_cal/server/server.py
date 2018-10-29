# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from slack_g_cal.queue.tasks import process_msg  # NOQA

from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return 'Hello World!', 200

    if request.method == 'POST':
        req_json = request.json
        cb_type = req_json.get('type')

        if cb_type == 'url_verification':
            return jsonify({'challenge': request.json['challenge']})

        elif cb_type == 'event_callback':
            if req_json:
                process_msg.delay(req_json)
                return 'Success', 200
            else:
                return 'Failure', 500

        else:
            print 'Unrecognized callback type encountered: "{}"'.format(cb_type)
            return 'Unrecognized callback type', 404
