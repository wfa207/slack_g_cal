# Slack Google Calendar Bot

## Installation

First, you'll need to setup a virtual environment, if you haven't already. To do so, run the following:

```bash
$ mkvirtualenv slack_g_cal
```

Once you've setup and installed your virtual environment, you can setup all your dependencies by running:

```bash
$ make setup
```

Make sure you export the appropriate environment variables:
  * SLACK_BOT_TOKEN: This is your 'Bot User OAuth Access Token' found in the 'OAuth & Permissions' section of the [Slack API](https://api.slack.com/apps) console
  * GOOGLE_AUTH_FILENAME: Your google auth filename (i.e. "g_auth.json")
  * WIT_ACCESS_TOKEN: Your 'Server Access Token' in the [Wit.ai](https://wit.ai) console
  * SENTRY_DSN: This is your DSN found in your [Sentry](https://sentry.io/welcome/) project's settings
  * BROKER_URL: A broker url supplied to [Celery](http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#application) to allow your bot to process tasks independently from your server

## Running Locally

You'll need to run three commands locally (you'll only need the `server-dev` and `queue` commands for production) for your bot to function properly:
```bash
$ make server-dev
$ make queue
$ ssh -R slack_g_cal.serveo.net:80:localhost:5000 serveo.net
```

The third command sets up SSL tunnelling to allow the Slack Events API to reach your local server. I recommend using [Serveo](https://serveo.net/) for convenience. You should **only need to setup SSL tunnelling for local development**. Make sure to **enable the [Events API](https://api.slack.com/events-api) within your Slack API console**. Once enabled, you will need to **[verify your request URL](https://api.slack.com/events-api#subscriptions)**.
