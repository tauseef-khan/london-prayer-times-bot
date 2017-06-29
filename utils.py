from wit import Wit

access_token = "6HCB47N5VKIPZDXSER6HH5CSYI5KIFGF"

client = Wit(access_token = access_token)

message_text = "ELM 15 July"

resp = client.message(message_text)

print(resp)