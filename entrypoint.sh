#!/bin/sh
set -a
echo "Starting"
. /home/k24_c/mio/.c/.env
set +a
exec lighttpd -D -f /etc/lighttpd/lighttpd.conf