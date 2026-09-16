#!usr/bin/env python3
import time
import random
from google import genai
from google.genai import errors
client=genai.Client()
max_tries=5
base_rate=2

def Review_Code(code,Use_promt):

            answer= client.models.generate_content(
                model="gemini-3.6-flash",
                contents=Use_promt.format(diff=code),
                config={
                    "response_mime_type": "application/json"
                }  
            )
            return answer.text
    



       
