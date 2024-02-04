# Puppet script to set up web_static

# Set up /data directory with the right permissions
file { '/data':
  ensure => 'directory',
  mode   => '755',
}

# Set up /data/web_static directory with the right permissions
file { '/data/web_static':
  ensure => 'directory',
  mode   => '755',
}

# Set up /data/web_static/releases directory with the right permissions
file { '/data/web_static/releases':
  ensure => 'directory',
  mode   => '755',
}

# Set up /data/web_static/releases/test directory with the right permissions
file { '/data/web_static/releases/test':
  ensure => 'directory',
  mode   => '755',
}

# Create /data/web_static/releases/test/index.html with the right permissions
file { '/data/web_static/releases/test/index.html':
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
  mode    => '644',
}

# Create a symbolic link to /data/web_static/releases/test
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

# Notify that everything is set up
notify { 'Web_Static_Setup_Complete':
  message => 'Web_Static setup completed successfully.',
}
