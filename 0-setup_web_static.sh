#!/usr/bin/env bash
# Sets up a web server for deployment of web_static.

# Check if Nginx is installed, if not, install it
if ! command -v nginx &> /dev/null; then
    apt-get update
    apt-get install -y nginx
fi

# Create necessary directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create fake HTML file for testing Nginx configuration
echo "Holberton School" > /data/web_static/releases/test/index.html

# Check if symbolic link exists, recreate if necessary
if [ -L /data/web_static/current ]; then
    rm /data/web_static/current
fi
ln -s /data/web_static/releases/test/ /data/web_static/current

# Set ownership and permissions recursively
chown -R ubuntu:ubuntu /data/
chmod -R 755 /data/

# Update Nginx configuration
printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}" > /etc/nginx/sites-available/default

# Restart Nginx
service nginx restart

# Test Nginx configuration
response_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/hbnb_static/index.html)
if [ "$response_code" != "200" ]; then
    echo "Error: Nginx configuration not updated successfully"
    exit 1
fi

# Exit successfully
exit 0
