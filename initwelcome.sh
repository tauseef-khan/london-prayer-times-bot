#!/bin/bash

# initwelcome.sh: sets welcome screen
# Execute once only

# Greeting Text
curl -X POST -H "Content-Type: application/json" -d '{
  "greeting":[
    {
      "locale":"default",
      "text":"Salaam {{user_first_name}}, Welcome to London Prayer Times Bot!"
    }
  ] 
}' "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=$PAGE_ACCESS_TOKEN"    

# Get Started button
curl -X POST -H "Content-Type: application/json" -d '{
  "setting_type":"call_to_actions",
  "thread_state":"new_thread",
  "call_to_actions":[
    {
      "payload":"Get Started"
    }
  ]
}' "https://graph.facebook.com/v2.6/me/thread_settings?access_token=$PAGE_ACCESS_TOKEN"