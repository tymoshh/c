#!/usr/bin/env python3

import sys

sys.path.insert(0, "/home/k24_c/cebularz7/local/usr/lib/python3/dist-packages")

import cgi

print("Content-Type: text/plain\n")  # Set the content type to plain text

for i in range(1, 11):
    print(i)

try:
    import testowyimport
    print("zadzialalo")
except:
    print("import sie wysypal")