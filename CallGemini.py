#!usr/bin/env python3
from google import genai
client=genai.Client()


def Review_Code(code,Use_promt):
    answer= client.models.generate_content(
        model="gemini-3.6-flash",
        contents=Use_promt.format(diff=code),
        config={
            "response_mime_type": "application/json"
        }  
    )
    return answer.text
