# app.py
# where the first point of contact for all user messages goes through and where the bot replies back

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


# any user action comes to this method first
@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    # call wit.ai method in utils.py
                    ai_response = ai.wit_response(message_text)
                    masjid, date = ai.extract_info(ai_response)

                    if date != None:
                        message = sheets.construct_schedule(date)
                        send_message(sender_id, message)
                    else:
                        message = sheets.construct_schedule(None)
                        send_message(sender_id, message)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID

                    payload_text = messaging_event["postback"]["payload"]
                    payload_text = payload_text.lower()
                     
                    # when the user first uses the bot and presses the "get started" button (TO BE IMPLEMENTED)
                    if (payload_text == "get started"):
                        
                        message = getStarted()
                        send_message(sender_id, message)

                    # when the menu option "Todays Prayer Times" is selected
                    if (payload_text == "todays prayer times"):
                        
                        message = sheets.construct_schedule(date=None)
                        send_message(sender_id, message)

    return "ok", 200

# method specifically for when 'get started' button is pressed
# ...because the message might chnage over time and having a method makes this easier to change
def getStarted():

    capability = "At the moment the bot can get today's prayer times or get the prayer times for any date this calendar year\n\n"

    # feature 1 - get today's prayer times
    todayTimes = "TODAY'S PRAYER TIMES:\n Swipe up on the menu below and press \"Today's Prayer Times\" \n\n"

    # feature 2 - get prayer times for any date in this calenday year
    anyTime = "PRAYER TIMES FOR ANY DATE:\n Swipe up in the menu below and press \"Send Message\" then type in a date, say '10 May' and the prayer times for 10 May will be shown"

    message = capability + todayTimes + anyTime

    return message

# sends a TEXT message to the user
def send_message(recipient_id, message_text):

    # print in heroku to check everything is okay
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    # three variables below construct the message to be sent
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

    # sends the message to the user
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


# method for debuggung
def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
