FROM nginx:alpine

COPY . /usr/share/nginx/html

RUN chmod +x /usr/share/nginx/html/generate-sitemap-robots.sh

ENTRYPOINT ["/usr/share/nginx/html/generate-sitemap-robots.sh"]
CMD ["nginx", "-g", "daemon off;"]