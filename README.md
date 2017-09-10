# london-prayer-times-bot

A Facebook Messenger bot which tells you the Muslim prayer time in London

So far only prayer time data from East London Mosque (ELM) is used.

## Bot structure:
* app.py -> where the first point of contact for all user messages goes through and where the bot replies back
* ai.py -> when user messages need to be processed using the wit.ai NLP platform, convert user input to narrowly defined outputs for easy processing
* sheets.py -> when the use of querying the prayer times worksheet is required via the use of Google Sheets and gspread

## Current features:
* get prayer times for today
* get prayer times for any date via user input (for ELM only)

## Features currently being developed:
* find nearest mosque (location feature)

## Roadmap:
* Getting started instructions
* Incorporate data from other mosques
