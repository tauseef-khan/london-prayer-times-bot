import os
import sys
import json

import subprocess

import requests
from flask import Flask, request

# custom made modules
import sheets
import ai

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID

                    payload_text = messaging_event["postback"]["payload"]
                    payload_text = payload_text.lower()
                     
                    if (payload_text == "get started"):
                        send_message(sender_id, "Further instructions coming...")

                    if (payload_text == "todays prayer times"):
                        message = sheets.construct_schedule(date=None)
                        send_message(sender_id, message)

                    if (payload_text == "coordinates"):
                        send_message(sender_id, "Found location")

                if messaging_event.get("message"):  # someone sent us a message

                    lat = None
                    lon = None
                    location = list(messaging_event['message'])
                    message_text = None

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID

                    try: 
                        message_text = messaging_event["message"]["text"]  # the message's text
                    except:
                        pass

                    try:
                        lat = list(location['attachments'])[0]
                        lat = list(lat['payload']['coordinates']['lat'])
                        log("LAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaT")
                        log(lat)

                        lon = location['attachments'][0]['payload']['coordinates']['lon']
                    except:
                        pass


                    send_message(sender_id, "here")
                    send_message(sender_id, location)
                    send_message(sender_id, lat)
                    send_message(sender_id, lon)

                    #
                    # call wit.ai method in utils.py
                    #ai_response = ai.wit_response(message_text)
                    #masjid, date = ai.extract_info(ai_response)

                    #if date != None:
                    #    message = sheets.construct_schedule(date)
                    #    send_message(sender_id, message)
                    #

                    #message = sheets.construct_schedule()
                    #send_message(sender_id, message)
                    #send_message(sender_id, "This is where I am when user puts in their onw message...maybe.")


    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
