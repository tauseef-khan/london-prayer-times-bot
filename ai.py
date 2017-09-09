import os
from wit import Wit
import json

access_token = os.environ['WIT_AI_TOKEN']

client = Wit(access_token = access_token)

#message_text = "ELM 15 July"

#resp = client.message(message_text)

#print(resp)

def wit_response(message_text):
	resp = client.message(message_text)
	entity = None
	value = None

	entity2 = None
	value2 = None


	try:
		entity = list(resp['entities'])[0]
		value = resp['entities'][entity][0]['value']

		entity2 = list(resp['entities'])[1]
		value2 = list(resp['entities']['datetime'][0]['values'])[0]['value']
	except:
		pass
	return (entity, value, entity2, value2)


def extract_info(info):

	masjid = None
	date = None

	if str(info[0]) == "masjid" and str(info[2]) == "datetime":
		masjid = str(info[1])
		date = str(info[3])

	elif str(info[0]) == "masjid":
		masjid = str(info[1])
		date = None

	elif str(info[0]) == "datetime":
		masjid = None
		date = str(info[1])

	else:
		masjid = None
		date = None

	return (masjid, date)


info = wit_response("I want the prayer times for ELM on July 29")
masjid, date = extract_info(info)

print("MASJID:", masjid)
print("DATE:", date)

info = wit_response("I want the prayer times for ELM")
masjid, date = extract_info(info)

print("MASJID:", masjid)
print("DATE:", date)

info = wit_response("I want the prayer times for 27 March")
masjid, date = extract_info(info)

print("MASJID:", masjid)
print("DATE:", date)