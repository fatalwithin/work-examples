#!/bin/sh
echo "Open Web Analytics start"

# Setup timezone
TZ=${TZ:=UTC}
echo "timezone=${TZ}"
rm -rf /etc/localtime
ln -s /usr/share/zoneinfo/${TZ} /etc/localtime
echo "${TZ}" > /etc/timezone
sed -i "s|;*date.timezone\s*=.*|date.timezone = \"${TZ}\"|i" /etc/php5/conf.d/owa.ini

exec $@