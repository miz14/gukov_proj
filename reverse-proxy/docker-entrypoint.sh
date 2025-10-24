#!/bin/sh
# Подставляем переменные при запуске контейнера
envsubst '${SITE1_DOMAIN} ${SITE2_DOMAIN}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf
exec "$@"