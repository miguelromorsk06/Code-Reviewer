#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()
from ParserJson import parser_answer
from Promts import Fast_promt
from DiffGit import obtain_diff
from CallGemini import Review_Code
from TerminalOutput import Show_Comments

def main():
    diff = obtain_diff()
    if not diff.strip():
        print("No hay cambios en staging (usá 'git add').")
        return
    
    crude_answer = Review_Code(diff)
    data = parser_answer(crude_answer)
    Show_Comments(data)

if __name__ == "__main__":
    main()