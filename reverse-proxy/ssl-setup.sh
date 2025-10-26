#!/bin/sh

echo "=== Настройка SSL сертификатов ==="

DOMAINS="${SITE1_DOMAIN} ${SITE2_DOMAIN}"

setup_cron_renewal() {
    echo "Настройка автоматического обновления SSL сертификатов..."
    echo "0 */12 * * * /ssl-renew.sh >> /var/log/cron.log 2>&1" > /etc/crontabs/root
    echo "✅ Cron задача для обновления SSL настроена (каждые 12 часов)"
}

get_certificate() {
    local domain=$1

    if [ -d "/etc/letsencrypt/live/$domain" ]; then
        echo "SSL сертификат для $domain существует"
        return 0
    fi

    echo "Создание SSL сертификата для $domain"
    
    # Создаем директорию для challenge-запросов
    mkdir -p /var/www/certbot
    
    # Получаем сертификат используя webroot метод (не требует остановки nginx)
    certbot certonly --webroot \
        --webroot-path /var/www/certbot \
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
    
    if [ $result -eq 0 ]; then
        echo "SSL сертификат для $domain успешно создан"
    else
        echo "Ошибка при создании SSL сертификата для $domain"
    fi
}

for domain in $DOMAINS; do
    get_certificate "$domain"
done


echo "=== Настройка SSL сертификатов окончена ==="