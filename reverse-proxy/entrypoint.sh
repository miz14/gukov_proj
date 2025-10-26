#!/bin/sh

# Генерируем временную HTTP конфигурацию для получения сертификатов
/nginx-config-setup.sh

# Запускаем nginx с HTTP конфигурацией
nginx -g 'daemon off;' &
NGINX_PID=$!

# Проверяем что nginx процесс запущен и слушает порт
for i in $(seq 1 30); do
    # Проверяем что процесс nginx существует
    if kill -0 $NGINX_PID 2>/dev/null; then
        # Проверяем что nginx слушает порт 80
        if netstat -tuln 2>/dev/null | grep -q ':80 '; then
            echo 'Nginx запущен и слушает порт 80'
            break
        fi
    fi
    
    if [ $i -eq 30 ]; then
        echo 'Таймаут ожидания nginx'
        exit 1
    fi
    
    sleep 1
    echo 'Ожидание запуска nginx...'
done

# Получаем SSL сертификаты
/ssl-setup.sh

# Генерируем полную SSL конфигурацию
/ssl-nginx-config-setup.sh

# Перезагружаем nginx с SSL конфигурацией
nginx -s reload
echo 'Nginx запущен с SSL конфигурацией'

wait $NGINX_PID
