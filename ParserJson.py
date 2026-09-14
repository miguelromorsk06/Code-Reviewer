#!usr/bin/env python3
import json

def parser_answer(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print("No se pudo parsear la respuesta:")
        print(text)
        return {"comentarios": []}