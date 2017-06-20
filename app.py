import os
import sys
import json

import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import requests
from flask import Flask, request

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

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    message = construct_schedule()
                    send_message(sender_id, "roger that!")
                    send_message(sender_id, message)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

def construct_schedule():

    # get date details
    #day = datetime.datetime.day()
    #month = datetime.datetime.month()

    now = datetime.datetime.now()
    day = now.day
    month = now.month
    monthCode = ""

    if month == 6:
        monthCode = "Sheet2"

    # sort out cell range
    dayCell = str(day + 2)
    cellRange = 'B' + dayCell + ":" + "M" + dayCell

    # read from excel sheet which has times in it
    # authentication
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('CF Data Extraction-ed446c061ae6.json', scope)
    gc = gspread.authorize(credentials)

    # Open a worksheet from spreadsheet with one shot
    #wks = gc.open_by_url('https://drive.google.com/open?id=1atbX-oMa6qeS0VjScLUAzEaghCVyh8MkcJ9pk5r3sAk')
    wks = gc.open('test')
    worksheet = wks.worksheet("Sheet2")


    # Fetch a cell range
    values_list = worksheet.row_values(day + 2)
    times = values_list[1:13]

    # construct message
    intro = "Prayer Times for today are:" + "\n"

    fajr_begins = "Fajr Begins - " + times[0] + "\n"
    fajr_jamaah = "Fajr Jama'ah - " + times[1] + "\n"

    sunrise = "Sunrise - " + times[2] + "\n"

    zuhr_begins = "Zuhr Begins - " + times[3] + "\n"
    zuhr_jamaah = "Zuhr Jama'ah - " + times[4] + "\n"

    asr_mithl1 = "Asr Mithl 1 - " + times[5] + "\n"
    asr_mithl2 = "Asr Mithl 2 - " + times[6] + "\n"
    asr_jamaah = "Asr Jama'ah - " + times[7] + "\n"

    maghrib_begins = "Maghrib Begins - " + times[8] + "\n"
    maghrib_jamaah = "Maghrib Jama'ah - "  + times[9] + "\n"

    isha_begins = "Isha Begins - " + times[10] + "\n"
    isha_jamaah = "Isha Jama'ah - " + times[11]

    msg = intro + fajr_begins + fajr_jamaah + sunrise + zuhr_begins + zuhr_jamaah + asr_mithl1 + asr_mithl2 + asr_jamaah + maghrib_begins + maghrib_jamaah + isha_begins + isha_jamaah
    
    return(msg)


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
