# Usa un'immagine PHP con Apache
FROM php:8.1-apache

# Installa le librerie necessarie per PDO e MySQL
RUN apt-get update && apt-get install -y libmariadb-dev libmariadb-dev-compat && docker-php-ext-install pdo pdo_mysql


# Abilita il modulo Apache rewrite
RUN a2enmod rewrite

# Copia i tuoi file nella cartella di destinazione
COPY . /var/www/html/

