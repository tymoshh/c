#!/usr/bin/env python3

print("Content-Type: text/plain\n")  # Set the content type to plain text

import os
import cgi
import json
import sys

sys.path.insert(0, "/home/k24_c/cebularz7/local/usr/lib/python3/dist-packages")

try:
    contentLength = int(os.environ.get('CONTENT_LENGTH', 0))
except (TypeError, ValueError):
    contentLength = 0
rawData = sys.stdin.read(contentLength) if contentLength > 0 else ''
try:
    jsonData = json.loads(rawData)
except json.JSONDecodeError:
    print(json.dumps({"error": "Invalid JSON"}))
    sys.exit(1)

json.dumps(jsonData)