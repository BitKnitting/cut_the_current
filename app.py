
# -*- coding: utf-8 -*-
"""
A routing layer for the onboarding bot tutorial built using
[Slack's Events API](https://api.slack.com/events-api) in Python
"""
import concierge_bot
import json
from flask import Flask, jsonify, request, make_response, render_template

concierge_bot = concierge_bot.Bot()


app = Flask(__name__)


def _event_handler(event_type, slack_event):
    """
    A helper function that routes events from Slack to our Bot
    by event type and subtype.
    Parameters
    ----------
    event_type : str
        type of event recieved from Slack
    slack_event : dict
        JSON response from a Slack reaction event
    Returns
    ----------
    obj
        Response object with 200 - ok or 500 - No Event Handler error
    """
    # ============== Message Events ============= #

    # if event_type == "message":
    #     concierge_bot.user_id = slack_event["event"].get("user")
    #     concierge_bot.getting_started_message()
    #     return make_response("Getting Started Message Sent", 200,)

########################################################################
@app.route("/welcome", methods=["GET", "POST"])
def send_welcome():
    # token = request.form.get('token',None)
    # if NOT token:
    #     message = "no token for the /welcome command"
    #    return make_response(message, 403, {"X-Slack-No-Retry": 1})
    welcome_msg = jsonify(concierge_bot.welcome_message)
    return welcome_msg


@app.route("/button_pressed", methods=["POST"])
def button_pressed():
    message_action = json.loads(request.form["payload"])
    which_button = message_action['actions'][0]['name']
    message = jsonify(concierge_bot.get_message(which_button))
    return message
    # return make_response("button pressed", 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    """
    This route listens for incoming events from Slack and uses the event
    handler helper function to route events to our Bot.
    """
    slack_event = json.loads(request.data)
      # ============= Slack URL Verification ============ #
    # In order to verify the url of our endpoint, Slack will send a challenge
    # token in a request and check for this token in the response our endpoint
    # sends back.
    #       For more info: https://api.slack.com/events/url_verification
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"
                                                             })
    # ============ Slack Token Verification =========== #
    # We can verify the request is coming from Slack by checking the
    # verification token in the request matches our app's settings
    if concierge_bot.verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s \nconcierge_bot has: \
                   %s\n\n" % (slack_event["token"], concierge_bot.verification)
        # By adding "X-Slack-No-Retry" : 1 to our response headers, we turn off
        # Slack's automatic retries during development.
        make_response(message, 403, {"X-Slack-No-Retry": 1})
    # ====== Process Incoming Events from Slack ======= #
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
            you're looking for.", 200, {"X-Slack-No-Retry": 1})

########################################################################
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=9001)
