#!/bin/sh
set -eu

if [ -f /var/www/html/include/ost-config.php ]; then
    php /usr/src/osticket/configure_local_install.php >/tmp/osticket-configure.log 2>&1 || true
fi

exec apache2-foreground