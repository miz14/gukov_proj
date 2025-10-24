FROM nginx:alpine

RUN apk add --no-cache gettext

COPY nginx.conf.template /etc/nginx/nginx.conf.template

COPY docker-entrypoint.sh /
COPY ssl-magager.sh /
RUN chmod +x /docker-entrypoint.sh /ssl-magager.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]

ENTRYPOINT ["/ssl-magager.sh"]
RUN echo "0 */12 * * * /ssl-magager.sh" >> /etc/crontabs/root