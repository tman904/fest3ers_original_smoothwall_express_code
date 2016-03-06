#! /bin/sh

# If dontlog is found, the patch has already been applied
if grep "conf/magic" /etc/httpd/conf/httpd.conf >/dev/null 2>&1; then
  echo "httpd.conf already patched"
  exit

else

  # Patch apache's conf
  sed -i -e 's=/usr/share/magic=/etc/httpd/conf/magic=' \
      /etc/httpd/conf/httpd.conf
  echo "httpd.conf patched"

  # Restart apache
  killall /usr/sbin/httpd
  /usr/sbin/httpd -DSSL
  echo "httpd restarted"
fi
