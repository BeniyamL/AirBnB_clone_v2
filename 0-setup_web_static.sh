#!/usr/bin/env bash
# Bash script that install ngnix and configure it
# It configures to port 80

# It configures to rediret to 301 moved permanently
# It configures to have a cutom 404 page

# install nginx
apt update
apt install -y nginx

# create the foler if doesn't exits
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# create a fake HTML file
printf "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n</html>\n" > /data/web_static/releases/test/index.html

# create a symbolic link , recreate every time when the script run
ln -sf /data/web_static/releases/test/ /data/web_static/current

# give owner ship and group to ubuntu user for data 
chown -R ubuntu /data/
chgrp -R ubuntu /data/

# configure the ngnix server

printf %s "server {
	listen 80;
	listen [::]:80 default_server;
	add_header X-Served-By &HOSTNAME;
	root /var/www/html;
	index index.html index.htm;

	location /hbnb_static {
		alias /data/web_static/current/;
		index index.html index.htm;	
	}

	location /redirect_me {
		return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
	}

	error_page 404 /404.html;
	location /404 {
		root /var/www/html;
		internal;
	}
}" > /etc/nginx/sites-available/default

service nginx restart
