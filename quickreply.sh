#!/bin/bash

# quickreply.sh: sets quick reply buttons
# Execute once only

curl -X POST -H "Content-Type: application/json" -d '{
  "recipient":{
    "id":"USER_ID"
  },
  "message":{
    "text":"Select an option:",
    "quick_replies":[
      {
        "content_type":"text",
        "title":"Todays Times",
        "payload":"Todays Prayer Times"
      }
    ]
  }
}' "https://graph.facebook.com/v2.6/me/messages?access_token=$PAGE_ACCESS_TOKEN"    