#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()
import sys
from Read_Rutes import read_rute
from ParserJson import parser_answer
from Promts import Fast_promt , AuditoryPromt
from DiffGit import obtain_diff
from CallGemini import Review_Code
from TerminalOutput import Show_Comments

def Fast_Mode():
    diff = obtain_diff()
    if not diff.strip():
        print("No hay cambios en staging (usá 'git add').")
        return
    
    crude_answer = Review_Code(diff,Fast_promt)
    data = parser_answer(crude_answer)
    Show_Comments(data)

def Auditory_Mode(rute):
    code=read_rute(rute)
    Final_Report=Review_Code(code,AuditoryPromt)
    print(Final_Report)

def main():
    if len(sys.argv) >=3 and sys.argv[1] == "--audit":
        Auditory_Mode(sys.argv[2])
    elif len(sys.argv) ==1:
        Fast_Mode()
    else:
        print("Bad use of the commands")
        print("Use:")
        print("  python main.py                    → fast diff review ")
        print("  python main.py --audit archivo.py → auditory review of an archive")


if __name__ == "__main__":
    main()
