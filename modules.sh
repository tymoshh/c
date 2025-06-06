#!/bin/bash

export PYTHONPATH=$HOME/local/usr/lib/python3/dist-packages:$PYTHONPATH

cp ./dbcon/dbcon.py /home/k24_c/cebularz7/local/usr/lib/python3/dist-packages
chmod 700 /home/k24_c/cebularz7/local/usr/lib/python3/dist-packages/dbcon.py

find ./ -type d -print0 | xargs -0 chmod 711
find ./ -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" \) -print0 | xargs -0 chmod 644
find ./ -type f -name "*.php" -print0 | xargs -0 chmod 700
find ./ -type f \( -name "*.cgi" -o -name "*.pl" -o -name "*.py" \) -print0 | xargs -0 chmod 700
find ./ -type f \( -name "*.php" -o -name "*.cgi" -o -name "*.pl" -o -name "*.py" \) -print0 | xargs -0 -I {} dirname {} | xargs -0 -I {} find {} -type f \( -name "*.txt" -o -name "*.dat" \) -print0 | xargs -0 chmod 600