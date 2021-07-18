# Sentry #

Глобальный регистратор ошибок

## Общая информация

Сервис состоит из компонентов:  
    - main - основной сервис (контейнер)
    - redis - вспомогательная бд. (контейнер)
    - memcached - вспомогательный сервис (контейнер)
    - cron - сервис для выполнения задач по расписанию (контейнер, совмещен с main)
	- worker - выполение асинхронных задач. (контейнер, совмещен с main)
	
Зависимость от внешних сервисов.   
    - Сервис опирается на внешнюю бд(Postgres) и требует явного указания адреса БД. Используется локально установленная на ВМ БД PostgreSQL 10. 
    - Для рассылки используется внешний smtp сервер (в данном случае это внешний сервис рассылок mailgun.com).
    - для публикации сервиса для внешнего веб-доступа используется локальный веб-сервер Nginx, так как сам по себе сервис Sentry основан на фреймворке Django, который не умеет работать в качестве прокси и перенаправлять запросы со стороны клиентов. Запрос на порт 80 перенаправляется на порт 443 (SSL), который в свою очередь силами того же Nginx перенаправляется на адрес 127.0.0.1:9000 (порт по умолчанию для веб-сервиса Sentry)

## Prerequisites

## Установка PostgreSQL

```bash
# add distro
sudo yum install epel-release

# install db server
sudo yum install postgresql10-server postgresql10 postgresql10-contrib

# init pgdata
sudo /usr/pgsql-10/bin/postgresql10-setup initdb

# start and autostart
sudo systemctl start postgresql-10
sudo systemctl enable postgresql-10

# open psql console
sudo su - postgres
```

```sql

CREATE USER sentry;
ALTER USER sentry with encrypted password 'pjTKmNiAQydlMD6qZqPktJTrEy7HRktnjbvB5NondkE=';
ALTER USER sentry CREATEDB;
ALTER USER sentry SUPERUSER;
CREATE DATABASE sentry OWNER sentry;
```

Далее происходит настройка аутентификации и сетевого доступа PostgreSQL:

```bash
# configure md5 auth 

sudo vim /var/lib/pgsql/10/data/pg_hba.conf

# [...]
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     peer
# IPv4 local connections:
host    all             all             127.0.0.1/32            ident
# IPv6 local connections:
host    all             all             ::1/128                 ident

# "local" is for Unix domain socket connections only
local   all             sentry                                  md5
# # IPv4 local connections:
host    all             sentry             127.0.0.1/32         md5
host    all             sentry             172.17.0.0/16        md5
host    all             sentry             172.20.0.0/16        md5
# # IPv6 local connections:
host    all             sentry             ::1/128              md5
         md5
# [...]

#configure network access
sudo vim /var/lib/pgsql/10/data/postgresql.conf

# [...]
listen_addresses = 'localhost, 172.17.0.1,172.20.0.1'
# [...]
port = 5432
# [...]

#restart db
sudo systemctl restart postgresql-10

```


## Установка и настройка nginx и SSL-сертификатов Let's Encrypt
В целом установка и настройка nginx почти полностью повторяет инструкцию с данного ресурса:
http://howto.05bit.com/services/sentry/


```bash
# install nginx and letsencrypt binaries
sudo yum install nginx letsencrypt

# выпуск сертификата, ответы на последовательные вопросы:
sudo certbot certonly
#webroot = /usr/share/nginx/html

# Автоматический перевыпуск сертификатов (по умолчанию сертификаты letsencrypt действуют 90 дней)
sudo crontab -e

>>> 43 6 * * * certbot renew --cert-name -q "sentry.sbear.ru" --post-hook "systemctl reload nginx"

```


## Управление развертыванием происходит через файл.
### sentry_deploy.sh
Ознакомиться со списком команд можно с помощью команды ниже:

```bash
./deploy_manager.sh help
```

## Перед началом развертывания требуется провести настройку окружения.

```bash
./deploy_manager.sh init
```
Будут выполнены миграции и потребуется интерактивное добаление пользователя.

## Запуск

```bash
./deploy_manager.sh run
```
