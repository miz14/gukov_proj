#!/bin/sh

echo "Проверка SSL сертификатов..."

DOMAINS="${SITE1_DOMAIN} ${SITE2_DOMAIN}"

get_certificate() {
    local domain=$1

    if [ -d "/etc/letsencrypt/live/$domain" ]; then
        echo "SSL сертификат для $domain существует"
        # Активируем редирект с HTTP на HTTPS
        enable_https_redirect "$domain"
        return 0
    fi

    echo "Создание SSL сертификата для $domain"
    # Останавливаем nginx временно для получения сертификата
    nginx -s stop
    
    certbot certonly --standalone \
        --domain $domain \
        --domain www.$domain \
        --email "${LETSENCRYPT_EMAIL}" \
        --agree-tos \
        --no-eff-email \
        --non-interactive \
        --config-dir /etc/letsencrypt \
        --work-dir /etc/letsencrypt/work \
        --logs-dir /etc/letsencrypt/log

    local result=$?
    
    # Перезапускаем nginx
    nginx -g "daemon off;" &
    
    if [ $result -eq 0 ]; then
        echo "SSL сертификат для $domain успешно создан"
    else
        echo "Ошибка при создании SSL сертификата для $domain"
    fi
}

enable_https_redirect() {
    local domain=$1

    echo "Активация редиректа с HTTP на HTTPS для $domain"
    # local config_file="/etc/nginx/sites-available/$domain.conf"
}

for domain in $DOMAINS; do
    get_certificate "$domain"
done

echo "SSL сертификаты успешно проверены"