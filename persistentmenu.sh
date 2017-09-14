#!/bin/bash

# persistentmenyu.sh: sets persistent menu
# Execute once only

a = "Today's" 
b = " Prayer Times"
c = $a$b


curl -X POST -H "Content-Type: application/json" -d '{
  "persistent_menu":[
    {
      "locale":"default",
      "composer_input_disabled":false,
      "call_to_actions":[
        {
          "type":"postback",
          "title":'$c',
          "payload":"Todays Prayer Times"
        },
        {
          "type":"web_url",
          "title":"Like London Prayer Times Bot",
          "url":"https://www.facebook.com/London-Prayer-Times-Bot-139230819969675/",
          "webview_height_ratio": "full",
        },
      ]
    }
  ]
}' "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=$PAGE_ACCESS_TOKEN"
    