#!/usr/bin/env python3

# Import required module
import os

# Send HTTP header
print("Content-Type: text/html\n")

# Start HTML output
print("<html><head><title>CGI Test</title></head><body>")
print("<h1>CGI is working!</h1>")
print("<p>Environment Variables:</p>")
print("<pre>")

# Print environment variables for debugging
for key, value in os.environ.items():
    print(f"{key}: {value}")

print("</pre>")
print("</body></html>")
