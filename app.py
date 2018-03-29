
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
    print('event type: ',event_type)
    print('slack event',slack_event)
    welcome_msg = jsonify(concierge_bot.get_message('welcome_message'))
    return welcome_msg
    # ============== Message Events ============= #

    # if event_type == "message":
    #     concierge_bot.user_id = slack_event["event"].get("user")
    #     concierge_bot.getting_started_message()
    #     return make_response("Getting Started Message Sent", 200,)

########################################################################
@app.route("/welcome", methods=["GET", "POST"])
def send_welcome():
    welcome_msg = jsonify(concierge_bot.get_message('welcome_message'))
    return welcome_msg

@app.route("/coach", methods=["GET", "POST"])
def questions_to_coach():
    with open('messages/coach/message_hello.json') as json_file:
        return jsonify(json.load(json_file))


@app.route("/button_pressed", methods=["POST"])
def button_pressed():
    action = json.loads(request.form["payload"])
    return concierge_bot.button_handler(action)


@app.route("/listening", methods=["GET", "POST"])
def hears():
    """
    This route listens for incoming events from Slack and uses the event
    handler helper function to route events to our Bot.
    """
    if request.data == b'':
        return make_response('Not a valid Slack message', 403, {"X-Slack-No-Retry": 1})
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
