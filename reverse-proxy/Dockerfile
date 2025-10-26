FROM nginx:alpine

RUN apk add --no-cache gettext

COPY nginx.conf.template /etc/nginx/nginx.conf.template

COPY nginx-config-setup.sh /
COPY ssl-nginx-config-setup.sh /
COPY ssl-setup.sh /
COPY entrypoint.sh /
RUN chmod +x /nginx-config-setup.sh /ssl-nginx-config-setup.sh /ssl-setup.sh /entrypoint.sh

RUN mkdir -p /var/www/certbot

ENTRYPOINT ["/entrypoint.sh"]
CMD []