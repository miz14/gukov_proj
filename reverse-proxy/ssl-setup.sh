#!/bin/bash

echo "Проверка SSL сертификатов..."

get_certificate() {
    local domain=$1

    if [ -d "/etc/letsencrypt/live/$domain" ]; then
        echo "SSL сертификат для $domain существует"
        # Активируем редирект с HTTP на HTTPS
        enable_https_redirect "$domain"
        return 0
    fi

    echo "Создание SSL сертификата для $domain"
    certbot certonly --standalone \
        --domain $domain \
        --domain www.$domain \
        --email "${LETSENCRYPT_EMAIL}" \
        --agree-tos \
        --no-eff-email \
        --non-interactive \
        --config-dir /etc/ssl \
        --work-dir /etc/ssl/work \
        --logs-dir /etc/ssl/log

    if [ $? -eq 0 ]; then
        echo "SSL сертификат для $domain успешно создан"
        # Активируем редирект с HTTP на HTTPS
        enable_https_redirect "$domain"
    else
        echo "Ошибка при создании SSL сертификата для $domain"
    fi
}

enable_https_redirect() {
    local domain=$1

    echo "Активация редиректа с HTTP на HTTPS для $domain"
    # local config_file="/etc/nginx/sites-available/$domain.conf"
}