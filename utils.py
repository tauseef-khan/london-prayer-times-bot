from wit import Wit
import os

access_token = os.environ.get('WIT_AI_TOKEN', none)

client = Wit(access_token = access_token)

message_text = "ELM 15 July"

resp = client.message(message_text)

print(resp)



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

#print(wit_response("I want the prayer times for ELM on July 29"))

info = wit_response("I want the prayer times for ELM on July 29")
info = (wit_response("July 4"))

print(info[0])

# print(info[3][:10])

# print(info[3][:4])
# print(info[3][5:7])
# print(info[3][8:10])