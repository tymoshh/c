#!/usr/bin/env python3

import json

# Set the HTTP header to return JSON content
print("Content-Type: application/json")
print()  # blank line to end headers

# Create a sample dictionary to return as JSON
response = {
    "message": "This is an example JSON response",
    "status": "success",
    "data": {
        "example_key": "example_value"
    }
}

# Output the JSON response
print(json.dumps(response))
