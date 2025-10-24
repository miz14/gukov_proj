FROM nginx:alpine

RUN apk add --no-cache gettext certbot

COPY nginx.conf.template /etc/nginx/nginx.conf.template

COPY nginx-config-setup.sh /
COPY ssl-setup.sh /
RUN chmod +x /nginx-config-setup.sh /ssl-setup.sh

ENTRYPOINT ["/nginx-config-setup.sh"]
CMD ["nginx", "-g", "daemon off;"]

# ENTRYPOINT ["/ssl-setup.sh"]

# RUN echo "0 */12 * * * /ssl-magager.sh" >> /etc/crontabs/root