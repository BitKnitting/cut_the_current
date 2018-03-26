
import json
import requests

BOT_AUTH='xoxb-336573790342-HdTuxLuE012aXDsPxpsKexzB'

class Message(object):
    def __init__(self):
        super(Message, self).__init__()
        self.channel = ""
        self.timestamp = ""


    def sendMessage(self,filepath):
        with open(filepath) as json_file:
            message_content = json.load(json_file)
            post_message = self.client.api_call("chat.postMessage",
                                channel=self.channel,
                                text=message_content['text'],
                                attachments=message_content['attachments']
                                )
            timestamp = post_message["ts"]
            # message_content["channel"] = "C9VCRKADR"
            # import pdb;pdb.set_trace()
            # payload = "{\n\t\"channel\":\"C9VCRKADR\",\n    \"text\": \":wave: Welcome.  I am so glad you will be playing cut-the-current. \",\n    \"attachments\": [\n        {\n            \"title\": \"Benefits\",\n            \"image_url\": \"https://i.imgur.com/zZFb7i4.png\"\n        },\n        {\n            \"fallback\": \"Would you like to know more about the game?\",\n            \"title\": \"Would you like to know more about the game?\",\n            \"callback_id\": \"benefits_callback\",\n            \"color\": \"#3AA3E3\",\n            \"attachment_type\": \"default\",\n            \"actions\": [\n              {\n                \"name\": \"impact\",\n                \"text\": \"Yes\",\n                \"type\": \"button\",\n                \"value\": \"Yes\"\n              },\n              {\n                \"name\": \"impact\",\n                \"text\": \"No, Sign me up!\",\n                \"type\": \"button\",\n                \"value\": \"No, Sign me up!\"\n              }\n            ]\n        }\n    ]\n}\n"
            # # payload["channel"]= self.channel
            # url = "https://slack.com/api/chat.postMessage"
            # auth_string = "Bearer "+ BOT_AUTH
            # headers = {
            #     'Content-Type': "application/json",
            #     'Authorization': auth_string,
            # }
            # response = requests.request("POST", url, data=payload, headers=headers)
            # print(response.text)
