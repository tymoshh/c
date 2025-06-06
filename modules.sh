#!/bin/bash

export PYTHONPATH=$HOME/local/usr/lib/python3/dist-packages:$PYTHONPATH

cp ./dbcon/dbcon.py /home/k24_c/cebularz7/local/usr/lib/python3/dist-packages
chmod 700 /home/k24_c/cebularz7/local/usr/lib/python3/dist-packages/dbcon.py

find ./ -type d -exec chmod 711 {} \;
find ./ ! -name "*.php" ! -type d -exec chmod 644 {} \;
find ./ -name '*.php' -exec chmod 700 {} \;
find ./ -name '*.php' -exec dirname {} \; | xargs -I {} find {} -type f -exec chmod 600 {} \;