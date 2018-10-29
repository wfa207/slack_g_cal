# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from . import raven_client


def sentry_enabled(raise_error=True):
    def wrapper(fn):
        def wrapped_func(*args, **kwargs):
            while True:
                try:
                    return fn(*args, **kwargs)
                except Exception:
                    raven_client.captureException()
                    if raise_error:
                        raise
        return wrapped_func

    return wrapper
