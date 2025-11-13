FROM nginx:alpine

COPY generate-sitemap-robots.sh /generate-sitemap-robots.sh
RUN chmod +x /generate-sitemap-robots.sh

COPY . /usr/share/nginx/html

ENTRYPOINT ["/generate-sitemap-robots.sh"]
CMD ["nginx", "-g", "daemon off;"]