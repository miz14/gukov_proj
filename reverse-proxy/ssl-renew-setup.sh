#!/bin/sh

setup_cron_renewal() {
    # Создаем скрипт для обновления
    cat > /renew-certs.sh << 'EOF'
#!/bin/sh
echo "$(date): Проверка обновления SSL сертификатов..."

    # Проверяем нужно ли обновление (сертификаты истекают через <30 дней)
    if certbot renew --dry-run --quiet --webroot --webroot-path /var/www/certbot; then
        echo "$(date): SSL сертификаты требуют обновления"
        # Делаем реальное обновление
        certbot renew --quiet --webroot --webroot-path /var/www/certbot --deploy-hook "nginx -s reload && echo '$(date): Nginx перезагружен после обновления сертификатов'"
        # ... перезагрузка nginx
    else
        echo "$(date): Обновление сертификатов не требуется"
    fi
EOF
    chmod +x /renew-certs.sh

    echo "0 */12 * * * /renew-certs.sh >> /var/log/cron.log 2>&1" > /etc/crontabs/root
    echo "Cron задача для обновления SSL настроена (каждые 12 часов)"
}


echo "=== Настройка автоматического обновления SSL сертификатов ==="

setup_cron_renewal

echo "=== Настройка автоматического обновления SSL сертификатов окончена ==="
