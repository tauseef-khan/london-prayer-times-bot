# sheets.py
# when the use of querying the prayer times worksheet is required via the use of Google Sheets and gspread

import datetime
import pytz
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import subprocess
import os
import json

# create the message contents of the prayer times message
def construct_schedule(date):

    # get date details
    #day = datetime.datetime.day()
    #month = datetime.datetime.month()

    now = None
    day = None
    month = None
    year = None
    date_today = None

    # depends if date specified in users message or 'Todays Prayer Times' is pressed
    if date != None:
        prayerDate = datetime.datetime.strptime(date[:10], '%Y-%m-%d')

        day = prayerDate.day
        month = prayerDate.month
        year = 2017
        date_today = str(day) + "/" + str(month) + "/" + str(year)

    else:
        now = datetime.datetime.now(pytz.timezone('Europe/London'))
        day = now.day
        month = now.month
        year = 2017
        date_today = str(day) + "/" + str(month) + "/" + str(year)

    monthCode = ""

    if month == 1:
        monthCode = "Jan-17"
    elif month == 2:
        monthCode = "Feb-17"
    elif month == 3:
        monthCode = "Mar-17"
    elif month == 4:
        monthCode = "Apr-17"
    elif month == 5:
        monthCode = "May-17"
    elif month == 6:
        monthCode = "Jun-17"
    elif month == 7:
        monthCode = "Jul-17"
    elif month == 8:
        monthCode = "Aug-17"
    elif month == 9:
        monthCode = "Sep-17"
    elif month == 10:
        monthCode = "Oct-17"
    elif month == 11:
        monthCode = "Nov-17"
    else:
        monthCode = "Dec-17"


    # sort out cell range
    dayCell = str(day + 2)
    cellRange = 'B' + dayCell + ":" + "M" + dayCell

    # read from excel sheet which has times in it
    # authentication
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(os.environ['GOOGLEAUTH']), scope)
    gc = gspread.authorize(credentials)

    # Open a worksheet from spreadsheet with one shot
    #wks = gc.open_by_url('https://drive.google.com/open?id=1atbX-oMa6qeS0VjScLUAzEaghCVyh8MkcJ9pk5r3sAk')
    wks = gc.open('elm-prayer-times')
    worksheet = wks.worksheet(monthCode)


    # Fetch a cell range
    values_list = worksheet.row_values(day + 2)
    times = values_list[1:13]

    # construct message
    intro = "Prayer Times for (" + date_today + ") are:" + "\n\n"

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