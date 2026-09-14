#!/usr/bin/env python3
import subprocess
#h
def obtain_diff():
    results = subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True,
        text=True
    )
    return results.stdout

if __name__ == "__main__":
    diff = obtain_diff()
    print(diff)