#!/bin/bash
HOSTNAME_IP=$(hostname -I | awk '{print $1}')
exec python /app/app/__main__.py --host="$HOSTNAME_IP"
