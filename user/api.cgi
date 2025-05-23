#!/usr/bin/env python3

import cgi
import json
import sys

# json
# action
# username
# password

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

    if jsonData["action"] == 'login':
        




    

