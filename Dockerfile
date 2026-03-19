FROM php:8.2-apache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libxml2-dev \
    libzip-dev \
    libicu-dev \
    libonig-dev \
    default-mysql-client \
    git \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Configure and install PHP extensions (without imap)
RUN docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
        gd \
        mysqli \
        pdo \
        pdo_mysql \
        xml \
        zip \
        gettext \
        intl \
        mbstring

# Install APCu
RUN pecl install apcu \
    && docker-php-ext-enable apcu

# Enable Apache mod_rewrite
RUN a2enmod rewrite

# Build the deployed osTicket web root from the source repository
WORKDIR /usr/src/osticket
COPY . /usr/src/osticket/

RUN find /usr/src/osticket/setup/inc/streams -type f -name '*.sql' -exec sed -i 's/\r$//' {} + \
    && find /usr/src/osticket/include/upgrader/streams -type f -name '*.sql' -exec sed -i 's/\r$//' {} +

RUN rm -rf /var/www/html/* \
    && php manage.php deploy --setup /var/www/html \
    && mkdir -p /var/www/html/uploads \
    && cp /var/www/html/include/ost-sampleconfig.php /var/www/html/include/ost-config.php \
    && chmod -R 755 /var/www/html \
    && chmod 666 /var/www/html/include/ost-config.php \
    && chmod -R 777 /var/www/html/uploads \
    && chown -R www-data:www-data /var/www/html

RUN chmod +x /usr/src/osticket/docker-entrypoint.sh

WORKDIR /var/www/html

# Expose port 80
EXPOSE 80

CMD ["/usr/src/osticket/docker-entrypoint.sh"]
