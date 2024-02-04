# Puppet script to set up web_static deployment on web servers

# Ensure /data directory exists with the correct permissions
file { '/data':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Ensure /data/web_static directory exists with the correct permissions
file { '/data/web_static':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
  mode   => '0755',
}

# Ensure /data/web_static/releases directory exists with the correct permissions
file { '/data/web_static/releases':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
  mode   => '0755',
}

# Ensure /data/web_static/releases/test/index.html exists with the correct permissions
file { '/data/web_static/releases/test/index.html':
  ensure => 'file',
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
  owner  => 'root',
  group  => 'root',
  mode   => '0644',
}

# Ensure /data/web_static/current exists
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  owner  => 'root',
  group  => 'root',
}

# Ensure Nginx configuration is updated
file { '/etc/nginx/sites-available/default':
  ensure => 'file',
  content => "server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location / {
        add_header X-Served-By $hostname;
        proxy_pass http://127.0.0.1:5000;
    }

    error_page 404 /404.html;
    location /404 {
        root /usr/share/nginx/html;
        internal;
    }

    location /redirect_me {
        rewrite ^/redirect_me /;
        rewrite ^/redirect_me /;
    }
}
",
  notify => Service['nginx'],
}

# Notify Nginx to restart if the configuration is updated
service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => File['/etc/nginx/sites-available/default'],
}
