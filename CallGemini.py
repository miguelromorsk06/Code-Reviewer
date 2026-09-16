#!usr/bin/env python3
import json
import time
import random
from google import genai
from google.genai import errors
client=genai.Client()
max_tries=5
base_rate=2

def Review_Code(code,Use_promt):

            chat= client.chats.create(
                model="gemini-3.1-flash-lite",
                config={
                    "response_mime_type": "application/json"
                }  
            )
            response = chat.send_message(Use_promt.format(diff=code))
            return response.text  
    



       
