#!/bin/sh

DOMAIN="${SITE1_DOMAIN}"

# Генерируем sitemap.xml
cat > /usr/share/nginx/html/sitemap.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://${DOMAIN}/</loc>
    <lastmod>$(date +%Y-%m-%d)</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
  <!-- Добавьте другие URL по необходимости -->
</urlset>
EOF

# Генерируем robots.txt
cat > /usr/share/nginx/html/robots.txt << EOF
User-agent: *
Allow: /
Disallow: /generate-sitemap.sh
Sitemap: https://${DOMAIN}/sitemap.xml
EOF

exec "$@"