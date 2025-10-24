#!/bin/sh

# Настраиваем nginx конфиг
/nginx-config-setup.sh

# Настраиваем SSL сертификаты
/ssl-setup.sh

# Запускаем nginx
exec nginx -g "daemon off;"