FROM nginx:alpine

COPY . /usr/share/nginx/html

COPY generate-sitemap-robots.sh /

RUN chmod +x /generate-sitemap-robots.sh

ENTRYPOINT ["/generate-sitemap-robots.sh"]
CMD ["nginx", "-g", "daemon off;"]