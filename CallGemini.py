#!usr/bin/env python3
from google import genai
from Promts import Fast_promt

client=genai.Client()
def Review_Code(code):
    answer= client.models.generate_content(
        model="gemini-3.6-flash",
        contents=Fast_promt.format(diff=code),
        config={
            "response_mime_type": "application/json"
        }  
    )
    return answer.text