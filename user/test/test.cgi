#!/usr/bin/env python3

print("Content-Type: text/plain\n")  # Set the content type to plain text

import cgi
import json
import sys

sys.path.insert(0, "/home/k24_c/cebularz7/local/usr/lib/python3/dist-packages")

def main():
    
    try:
        contentLength = int(sys.os.environ.get('CONTENT_LENGTH', 0))
    except (TypeError, ValueError):
        contentLength = 0

    rawData = sys.stdin.read(contentLength) if contentLength > 0 else ''

    try:
        jsonData = json.loads(rawData)
    except json.JSONDecodeError:
        data = None

    import dbcon
    if jsonData["action"] == 'login':
        userObject = dbcon.userClass(jsonData["username"], jsonData["password"])
        userObject.createPasswdHash()
        userObject.fetchToken()
        tokenVar = userObject.viewToken()
        print(tokenVar)

main()