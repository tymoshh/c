#!/usr/bin/env python3

import sys

sys.path.append('/usr/local/lib/python3.x/dist-packages')

import cgi

print("Content-Type: text/plain\n")  # Set the content type to plain text

for i in range(1, 11):
    print(i)

print("przed zaimportowaniem dbcon")

import dbcon
