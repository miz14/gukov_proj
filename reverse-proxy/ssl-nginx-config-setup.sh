#!/bin/sh

# Генерируем полную конфигурацию с SSL
echo "=== Генерация полной конфигурации nginx ==="
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
    
    # HTTP редирект на HTTPS
    server {
        listen 80;
        server_name ${SITE1_DOMAIN} www.${SITE1_DOMAIN};
        return 301 https://$host$request_uri;
    }

    server {
        listen 80;
        server_name ${SITE2_DOMAIN} www.${SITE2_DOMAIN};
        return 301 https://$host$request_uri;
    }

    # HTTPS конфигурация для SITE1
    server {
        listen 443 ssl;
        server_name ${SITE1_DOMAIN} www.${SITE1_DOMAIN};

        ssl_certificate /etc/letsencrypt/live/${SITE1_DOMAIN}/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/${SITE1_DOMAIN}/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        
        location / {
            proxy_pass http://site1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /api/ {
            proxy_pass http://forms-data-handler/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

    # HTTPS конфигурация для SITE2
    server {
        listen 443 ssl;
        server_name ${SITE2_DOMAIN} www.${SITE2_DOMAIN};

        ssl_certificate /etc/letsencrypt/live/${SITE2_DOMAIN}/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/${SITE2_DOMAIN}/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        
        location / {
            proxy_pass http://site2;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
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

echo "Nginx SSL конфигурация сгенерирована"