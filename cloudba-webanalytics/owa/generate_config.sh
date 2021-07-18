#!/usr/bin/env bash

set -o pipefail

if grep --help 2>&1 | grep -q -i "busybox"; then
  echo "BusybBox grep detected, please install gnu grep, \"apk add --no-cache --upgrade grep\""
  exit 1
fi
if cp --help 2>&1 | grep -q -i "busybox"; then
  echo "BusybBox cp detected, please install coreutils, \"apk add --no-cache --upgrade coreutils\""
  exit 1
fi

if [ -f owa.conf ]; then
  read -r -p "A config file exists and will be overwritten, are you sure you want to contine? [y/N] " response
  case $response in
    [yY][eE][sS]|[yY])
      mv owa.conf owa.conf_backup
      chmod 600 owa.conf_backup
      ;;
    *)
      exit 1
    ;;
  esac
fi

echo "Press enter to confirm the detected value '[value]' where applicable or enter a custom value."
while [ -z "${OWA_HOSTNAME}" ]; do
  read -p "Hostname (FQDN): " -e OWA_HOSTNAME
  DOTS=${OWA_HOSTNAME//[^.]};
  if [ ${#DOTS} -lt 2 ] && [ ! -z ${OWA_HOSTNAME} ]; then
    echo "${OWA_HOSTNAME} is not a FQDN"
    OWA_HOSTNAME=
  fi
done

if [ -a /etc/timezone ]; then
  DETECTED_TZ=$(cat /etc/timezone)
elif [ -a /etc/localtime ]; then
  DETECTED_TZ=$(readlink /etc/localtime|sed -n 's|^.*zoneinfo/||p')
fi

while [ -z "${OWA_TZ}" ]; do
  if [ -z "${DETECTED_TZ}" ]; then
    read -p "Timezone: " -e OWA_TZ
  else
    read -p "Timezone [${DETECTED_TZ}]: " -e OWA_TZ
    [ -z "${OWA_TZ}" ] && OWA_TZ=${DETECTED_TZ}
  fi
done

cat << EOF > owa.conf
# ------------------------------
# Open Web Analytics initial configuration
# ------------------------------

OWA_HOSTNAME=${OWA_HOSTNAME}

# ------------------------------
# SQL database configuration
# ------------------------------

DBNAME=owadb
DBUSER=owauser

# Please use long, random alphanumeric strings (A-Za-z0-9)

DBPASS=$(LC_ALL=C </dev/urandom tr -dc A-Za-z0-9 | head -c 28)
DBROOT=$(LC_ALL=C </dev/urandom tr -dc A-Za-z0-9 | head -c 28)

# ------------------------------
# HTTP/S Bindings
# ------------------------------

HTTP_PORT=80
HTTP_BIND=0.0.0.0

HTTPS_PORT=443
HTTPS_BIND=0.0.0.0

# ------------------------------
# Other bindings
# ------------------------------
# You should leave that alone
# Format: 11.22.33.44:25 or 0.0.0.0:465 etc.
# Do _not_ use IP:PORT in HTTP(S)_BIND or HTTP(S)_PORT

SQL_PORT=127.0.0.1:13306

# Your timezone

TZ=${OWA_TZ}

# Fixed project name

COMPOSE_PROJECT_NAME=owadockerized

# Internal IPv4 /24 subnet, format n.n.n (expands to n.n.n.0/24)

IPV4_NETWORK=172.20.1

# Internal IPv6 subnet in fc00::/7

IPV6_NETWORK=fd4d:6169:6c63:6f88::/64

OWA_UID="82" \
OWA_USER="www-data" \
OWA_GID="82" \
OWA_GROUP="www-data" \
WEBROOT_DIR="/owa"

EOF

# make .env file to import into docker-compose

ln -s owa.conf .env

chmod 600 owa.conf



