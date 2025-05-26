#!/usr/bin/env python3

import cgi

print("Content-Type: text/plain\n")  # Set the content type to plain text

for i in range(1, 11):
    print(i)

import dbcon
