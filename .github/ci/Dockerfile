FROM php:8.2-apache-bookworm
RUN apt-get update -qq && apt-get install -y -qq unzip curl libzip-dev libpng-dev libjpeg-dev libfreetype6-dev >/dev/null \
 && docker-php-ext-configure gd --with-freetype --with-jpeg >/dev/null \
 && docker-php-ext-install -j4 mysqli gd zip >/dev/null \
 && a2enmod rewrite >/dev/null \
 && curl -sL -o /tmp/oc.zip https://github.com/opencart/opencart/releases/download/4.1.0.4/opencart-4.1.0.4.zip \
 && unzip -q /tmp/oc.zip -d /tmp/oc && cp -r /tmp/oc/opencart-4.1.0.4/upload/. /var/www/html/ 2>/dev/null || cp -r /tmp/oc/upload/. /var/www/html/ \
 && mv /var/www/html/config-dist.php /var/www/html/config.php && mv /var/www/html/admin/config-dist.php /var/www/html/admin/config.php \
 && chown -R www-data:www-data /var/www/html && rm -rf /tmp/oc /tmp/oc.zip
