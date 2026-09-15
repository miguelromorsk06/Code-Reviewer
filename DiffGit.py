#!/usr/bin/env python3
import subprocess
import os
import sys
# def obtain_diff():

#     results = subprocess.run(
#         ["git", "diff", "--staged"],
#         capture_output=True,
#         text=True
#     )
#     return results.stdout

# if __name__ == "__main__":
#     diff = obtain_diff()
#     print(diff)



def obtain_diff():
    Base_ref=os.getenv("BASE_REF") #For github Actions
    github_event = os.getenv("GITHUB_EVENT_NAME")
    if Base_ref:
        #PullRequest
        command= ["git","diff",f"origin/{Base_ref}...HEAD"]
    elif github_event == "push":
        #Push
        command = ["git", "diff", "HEAD~1", "HEAD"]
    else:
        command = ["git", "diff", "--staged"]
    try:
        resultado = subprocess.run(command, capture_output=True, text=True, check=True)
        return resultado.stdout
    except subprocess.CalledProcessError as e :
        print(f"Error in git diff")
        sys.exit(1)
