#!/bin/sh
SSL_DIR="/etc/letsencrypt"
LIVE_DIR="$SSL_DIR/live"
DOMAINS=("${SITE1_DOMAIN}" "${SITE2_DOMAIN}" "www.${SITE1_DOMAIN}" "www.${SITE2_DOMAIN}")

check_nginx_config() {
    echo "Проверка конфигурации nginx..."
    if nginx -t; then
        echo "Конфигурация nginx корректна"
        return 1
    else 
        echo "Ошибка конфигурации nginx"
        return 0
    fi
}

check_certificates_exist() {
    local domain="$1"
    local cart_path="$LIVE_DIR/$domain/cert.pem"

    if [ -f "$cart_path" ]; then
        echo "SSL сертификат для $domain существует"
        return 1
    else
        echo "SSL сертификат для $domain не существует"
        return 0
    fi
}

check_certificate_expiration_date() {
    local domain="$1"
    local cart_path="$LIVE_DIR/$domain/cert.pem"

    if [ -f "$cart_path" ]; then
        echo "SSL сертификат для $domain не найден"
        return 2
    fi

    local expiration_date=$(openssl x509 -in "$cart_path" -noout -enddate | cut -d= -f2)
    local expiration_epoch=$(date -d "$expiration_date" +%s)
    local current_epoch=$(date +%s)
    local days_left=$(( ($expiration_epoch - $current_epoch) / 86400 ))

    if [ $days_left -le 30 ]; then
        echo "SSL сертификат для $domain требует обновление, истекает через $days_left дней"
        return 0
    else
        echo "SSL сертификат для $domain истекает через $days_left дней"
        return 1
    fi
}

generate_certificates() {
    local args=""
    for domain in "${DOMAINS[@]}"; do
        args="$args -d $domain"
    done

    if certbot certonly --nginx \
        $args \
        --non-interactive \
        --agree-tos \
        --email "${LETSENCRYPT_EMAIL}" \
        --keep-until-expiring; then

        echo "SSL сертификаты успешно созданы"
    else
        echo "Ошибка при создании SSL сертификатов"
    fi
}

renew_certificates() {
    if certbot renew --quiet; then
        echo "Сертификаты успешно обновлены"
        
        # Перезагружаем nginx для применения новых сертификатов
        echo "Перезагрузка nginx..."
        systemctl reload nginx
        
        if [ $? -eq 0 ]; then
            echo "Nginx успешно перезагружен"
            return 1
        else
            echo "Ошибка при перезагрузке nginx"
            return 0
        fi
    else
        echo "Ошибка при обновлении сертификатов"
        return 0
    fi
}

main() {
    echo "=== Начало проверки SSL сертификатов ==="
    echo "Домены: ${DOMAINS[*]}"
    
    if ! check_nginx_config; then
        echo "Прерывание проверки SSL сертификатов"
        exit 1
    fi

    local need_renewal=false
    local need_generation=false

    for domain in "${DOMAINS[@]}"; do
        # если существет
        if check_certificates_exist "$domain"; then
            # если истекает
            if ! check_certificate_expiration_date "$domain"; then
                need_renewal=true
            fi
        else 
            need_generation=true
        fi
        echo ""
    done

    if [ "$need_generation" = true ]; then
        echo "=== Начало создания SSL сертификатов ==="
        generate_certificates
        
    elif [ "$need_renewal" = true ]; then
        echo "=== Начало обновления SSL сертификатов ==="
        renew_certificates
    else
        echo "SSL сертификаты актуальны"
    fi
}

main