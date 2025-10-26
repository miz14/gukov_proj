#!/bin/sh


# Запускаем nginx с HTTP конфигурацией
nginx -g 'daemon off;' &
NGINX_PID=$!

echo 'Ожидание запуска nginx...'
echo 'Ожидание запуска nginx...'
while ! ps -p $NGINX_PID > /dev/null; do
    sleep 0.1
done
echo 'Nginx запущен'

# Получаем SSL сертификаты
/ssl-setup.sh

# Генерируем полную SSL конфигурацию
/ssl-nginx-config-setup.sh

# Перезагружаем nginx с SSL конфигурацией
nginx -s reload
echo 'Nginx запущен с SSL конфигурацией'

wait $NGINX_PID
