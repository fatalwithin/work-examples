FROM alpine:3.8

# Add application user and group
RUN set -ex \
	&& addgroup -g $OWA_UID -S $OWA_GROUP \
	&& adduser -u $OWA_GID -D -S -G $OWA_USER $OWA_GROUP \
# Install packages
    && apk update \
    && apk upgrade \
    && apk add --update tzdata \
    && apk --no-cache add \
    php5-fpm \    
    php5-mysql \
    php5-mysqli \
    php5-pcntl \
    php5-json \
    php5-openssl \
    php5-curl \
    php5-zlib \
    php5-xml \
    php5-phar \
    php5-intl \
    php5-dom \
    php5-xmlreader \
    php5-ctype \
    php5-gd \
    supervisor curl jq \
# Setup OWA configuration
    && cp /tmp/owa-config/owa-www.conf /etc/php5/fpm.d/ \
    && cp /tmp/owa-config/owa.ini /etc/php5/conf.d/ \
    && mkdir -p /etc/supervisor/conf.d \
    && cp /tmp/owa-config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf \
    && cp /tmp/owa-config/entrypoint.sh /usr/bin/owa-entrypoint.sh \
    && chmod 0775 /usr/bin/owa-entrypoint.sh \
# Setup php-fpm unix user/group
    && sed -i "s|user\s*=.*|user = ${OWA_USER}|g" /etc/php5/php-fpm.conf \
    && sed -i "s|group\s*=.*|group = ${OWA_GROUP}|g" /etc/php5/php-fpm.conf \
# Add Open Web Analytics (OWA)
    chown -R $OWA_USER:$OWA_GROUP $WEBROOT_DIR/ \
    && chmod -R 0775 $WEBROOT_DIR/ \
    && apk del jq

WORKDIR $WEBROOT_DIR
EXPOSE 80 443
ENTRYPOINT ["/usr/bin/owa-entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]