#!/bin/sh

# Генерируем временную HTTP-конфигурацию для получения сертификатов
echo "=== Генрация HTTP конфигурации nginx ==="

echo "Домены: $SITE1_DOMAIN, $SITE2_DOMAIN"

cat > /etc/nginx/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream site1 {
        server site1:80;
    }
    upstream site2 {
        server site2:80;
    }

    upstream forms-data-handler {
        server forms-data-handler:3000;
    }

    # Default server для запросов по IP
    server {
        listen 80 default_server;
        server_name _;
        return 444;
    }
    
    # SITE1 - HTTP конфигурация (для certbot)
    server {
        listen 80;
        server_name ${SITE1_DOMAIN} www.${SITE1_DOMAIN};

        # Certbot challenges
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        # Редирект всего остального на HTTPS (после получения сертификатов)
        location / {
            return 301 https://$host$request_uri;
        }

        location /api/ {
            proxy_pass http://forms-data-handler/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

    # SITE2 - HTTP конфигурация (для certbot)
    server {
        listen 80;
        server_name ${SITE2_DOMAIN} www.${SITE2_DOMAIN};

        # Certbot challenges
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        # Редирект всего остального на HTTPS (после получения сертификатов)
        location / {
            return 301 https://$host$request_uri;
        }

        location /api/ {
            proxy_pass http://forms-data-handler/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF

# Применяем переменные окружения
envsubst '${SITE1_DOMAIN} ${SITE2_DOMAIN}' < /etc/nginx/nginx.conf > /etc/nginx/nginx.conf.tmp
mv /etc/nginx/nginx.conf.tmp /etc/nginx/nginx.conf

echo "=== Nginx HTTP конфигурация сгенерирована ==="
echo ""