#!/usr/bin/env python3

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
        print(json.dumps({"token": tokenVar}))

main()
        
        




    

