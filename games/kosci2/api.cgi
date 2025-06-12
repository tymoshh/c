#!/usr/bin/env python3

import cgi
import cgitb
import os

# Enable error reporting in browser (for debugging)
cgitb.enable()

# Print HTTP headers
print("Content-Type: text/html")
print()

# Print HTML response
print(f"""
<!DOCTYPE html>
<html>
<head>
    <title>CGI Test</title>
</head>
<body>
    <h1>CGI GET Request Test</h1>
</body>
</html>
""")
