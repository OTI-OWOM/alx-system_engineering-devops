# Puppet manifest to increase NGINX ULIMIT to handle more connections
exec { 'increase-limit':
  command => 'sed -i "s/ULIMIT=\"-n 15\"/ULIMIT=\"-n 4096\"/" /etc/default/nginx',
  path    => '/usr/local/bin/:/bin/',
  onlyif  => 'grep -q "ULIMIT=\"-n 15\"" /etc/default/nginx',
}

# restart nginx to apply new settings
exec { 'restart-nginx':
  command => '/etc/init.d/nginx restart',
  path    => '/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin',
  require => Exec['increase-limit'],
}
