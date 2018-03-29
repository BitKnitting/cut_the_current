import os
import json
from time import sleep
import threading



from slackclient import SlackClient
from flask import jsonify, make_response

# The Concierge channel ID
CHANNEL_ID = "C9VCRKADR"


class Bot(object):
    """ Instanciates a Bot object to handle concierge interactions."""

    def __init__(self):
        super(Bot, self).__init__()
        # When we instantiate a new bot object, we can access the app
        # credentials we set earlier in our local development environment.
        self.oauth = {"client_id": os.environ.get("CLIENT_ID"),
                      "client_secret": os.environ.get("CLIENT_SECRET"),
                      # Scopes provide and limit permissions to what our app
                      # can access. It's important to use the most restricted
                      # scope that your app will need.
                      "scope": "bot"}
        self.verification = os.environ.get("VERIFICATION_TOKEN")

        # NOTE: Python-slack requires a client connection to generate
        # an oauth token. We can connect to the client without authenticating
        # by passing an empty string as a token and then reinstantiating the
        # client with a valid OAuth token once we have one.
        self.client = SlackClient("")
        # We'll use this dictionary to store the state of each message object.
        # In a production envrionment you'll likely want to store this more
        # persistantly in  a database.
        self.messages = {}

        self.user_id = 0

    def auth(self, code):
        """
        Authenticate with OAuth and assign correct scopes.
        Save a dictionary of authed team information in memory on the bot
        object.
        Parameters
        ----------
        code : str
            temporary authorization code sent by Slack to be exchanged for an
            OAuth token
        """
        # After the user has authorized this app for use in their Slack team,
        # Slack returns a temporary authorization code that we'll exchange for
        # an OAuth token using the oauth.access endpoint
        auth_response = self.client.api_call(
            "oauth.access",
            client_id=self.oauth["client_id"],
            client_secret=self.oauth["client_secret"],
            code=code
        )
        # To keep track of authorized teams and their associated OAuth tokens,
        # we will save the team ID and bot tokens to the global
        # authed_teams object
        team_id = auth_response["team_id"]
        authed_teams[team_id] = {"bot_token":
                                 auth_response["bot"]["bot_access_token"]}
        # Then we'll reconnect to the Slack Client with the correct team's
        # bot token
        self.client = SlackClient(authed_teams[team_id]["bot_token"])

    def get_message(self, which_message):
        file = None
        # import pdb;pdb.set_trace()
        if which_message == 'benefits_message_YES':
            file = "messages/concierge/message_about.json"
        elif which_message == 'welcome_message':
            file = "messages/concierge/message_welcome.json"
        elif which_message == 'install_form_success':
            file = "messages/concierge/message_install_form_success.json"
        if file:
            with open(file) as json_file:
                return json.load(json_file)

    def show_dialog(self, which_button, trigger_id):
        if which_button == 'install_dialog_YES':
            with open("messages/concierge/dialog_install.json") as json_file:
                json_loaded = json.load(json_file)
                open_dialog = self.client.api_call(
                    "dialog.open",
                    trigger_id=trigger_id,
                    token=os.environ.get("BOT_AUTH"),
                    dialog=json_loaded
                )

    def button_handler(self, action):
        # Check if incoming was the result of a form Submit.
        callback_id = action['callback_id']
        if callback_id == 'install_form':
            # import pdb;pdb.set_trace()
            # return make_response("",200)
            channel = channel=action['channel']['id']
            fname = 'list_of_messages_after_appt_setup'
            # send messages after responding to the dialog submit button....
            t = threading.Timer(1,self.send_messages,kwargs={'filename':fname,'channel':channel})
            t.start()
            return make_response("",200)
        which_message = action['actions'][0]['name']
        print(which_message)
        if 'dialog' in which_message:
            trigger_id = action["trigger_id"]
            self.show_dialog(which_message,trigger_id)
            return make_response("",200)
        else:
            message = jsonify(self.get_message(which_message))
            return message
            # return make_response("button pressed", 200, {"X-Slack-No-Retry": 1})

    # A little conversationsal chatter....
    def send_messages(self,**kwargs):
        fname = kwargs['filename']
        channel = kwargs['channel']
        filename = 'messages/concierge/'+fname+'.list'
        print(filename)
        with open(filename) as f:
            messages = f.read().splitlines()
            for message in messages:
                sleep(5.0)
                self.client.api_call(
                    "chat.postMessage",
                    token=os.environ.get("BOT_AUTH"),
                    channel=channel,
                    text=message,
                    as_user=False,
                    icon_url="https://i.imgur.com/quvFoGF.png"
                )
