FROM nginx:alpine

RUN apk add --no-cache gettext certbot

COPY nginx.conf.template /etc/nginx/nginx.conf.template

COPY nginx-config-setup.sh /
COPY ssl-setup.sh /
COPY start.sh /
RUN chmod +x /nginx-config-setup.sh /ssl-setup.sh /start.sh

ENTRYPOINT ["/start.sh"]

# RUN echo "0 */12 * * * /ssl-magager.sh" >> /etc/crontabs/root