FROM nginx:alpine

RUN apk add --no-cache gettext

COPY nginx.conf.template /etc/nginx/nginx.conf.template

COPY docker-entrypoint.sh /
COPY ssl-magager.sh /
COPY test.sh /
RUN chmod +x /docker-entrypoint.sh /ssl-magager.sh /test.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]

ENTRYPOINT ["/test.sh"]
# RUN echo "0 */12 * * * /ssl-magager.sh" >> /etc/crontabs/root