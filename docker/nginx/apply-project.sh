#!/bin/sh

if [ ! -L /etc/nginx/sites-enabled/ttm4115-e-scooter-application.conf ]; then
    ln -s /etc/nginx/sites-available/ttm4115-e-scooter-application.conf /etc/nginx/sites-enabled/
fi

exec nginx -g 'daemon off;'