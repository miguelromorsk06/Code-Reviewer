Api_Anthropic="8279803719817298"
 answer= client.models.generate_content(
        model="gemini-3.6-flash",
        contents=Fast_promt.format(diff=code),
        config={
            "response_mime_type": "application/json"
        }  
    )
    return answer.text

 if i  =  2 :
    True

Gemini_api="ka98037122971908371282"