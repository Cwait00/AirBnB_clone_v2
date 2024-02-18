# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
file { '/data':
  ensure  => 'directory',
  owner   => 'ubuntu',  # Correct ownership to ubuntu
  group   => 'ubuntu',  # Correct group to ubuntu
  mode    => '0755',
}

file { '/data/web_static':
  ensure  => 'directory',
  owner   => 'ubuntu',  # Correct ownership to ubuntu
  group   => 'ubuntu',  # Correct group to ubuntu
  mode    => '0755',
}

file { '/data/web_static/releases':
  ensure  => 'directory',
  owner   => 'ubuntu',  # Correct ownership to ubuntu
  group   => 'ubuntu',  # Correct group to ubuntu
  mode    => '0755',
}

file { '/data/web_static/shared':
  ensure  => 'directory',
  owner   => 'ubuntu',  # Correct ownership to ubuntu
  group   => 'ubuntu',  # Correct group to ubuntu
  mode    => '0755',
}

file { '/data/web_static/releases/test':
  ensure  => 'directory',
  owner   => 'ubuntu',  # Correct ownership to ubuntu
  group   => 'ubuntu',  # Correct group to ubuntu
  mode    => '0755',
}

# Create fake HTML file for testing
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  owner   => 'ubuntu',  # Correct ownership to ubuntu
  group   => 'ubuntu',  # Correct group to ubuntu
  mode    => '0644',
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test',
  owner   => 'ubuntu',  # Correct ownership to ubuntu
  group   => 'ubuntu',  # Correct group to ubuntu
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  content => "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
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
}",
}

# Restart Nginx
service { 'nginx':
  ensure    => 'running',
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
