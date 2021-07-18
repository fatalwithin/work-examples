# Olivia Persistent Services


## Веб-доступ (публичный)

Домен для размещения общесистемных сервисов для Olivia:
http://sinago.ga

Доступ извне - по SSL, терминирующемся на Nginx.
После Nginx - доступ к самим сервисам по HTTP.

| **Домен** | **Назначение** |
| ------ | ------ |
| [sinago.ga](https://sinago.ga) | корневой домен |
| [postgres.sinago.ga](https://postgres.sinago.ga) | веб-панель администрирования PostgreSQL | 
| [pg.sinago.ga](https://pg.sinago.ga) | веб-панель администрирования PostgreSQL(алиас) |
| [rabbit.sinago.ga](https://rabbit.sinago.ga) | веб-панель администрирования RabbitMQ |
| [mq.sinago.ga](https://mq.sinago.ga) | веб-панель администрирования RabbitMQ(алиас) |
| [redis.sinago.ga](https://redis.sinago.ga) | веб-панель администрирования Redis |
| [rd.sinago.ga](https://rd.sinago.ga) | веб-панель администрирования Redis (алиас) |
| [s3.sinago.ga](https://s3.sinago.ga) | доступ к объектному хранилищу S3 на базе Minio |


## PostgreSQL


### Веб-морда:  

Настройка pgadmin:
Если pgadmin отдает ошибку 500, необходимо проверить права на папки и все вложенные файлы
По каким-то причинам при старте apache файлы создаются с владельцем root:root

Первым шагом проверить наличие папок:
```
/var/lib/pgadmin4/
/var/log/pgadmin4/
```
Вторым шагом проверить владельца папок и вложенных файлов. В случае, если владелец не apache:apache, то изменить владельца
```
chown -R apache:apache /var/lib/pgadmin4/*
chown -R apache:apache /var/log/pgadmin4/*
```
Перезапустить apache
```
systemctl restart httpd
```

## RabbitMQ


### Веб-морда:  

Управление менеджером очередей по HTTP(S) осуществляется через собственный менеджмент-плагин: https://www.rabbitmq.com/management.html

Установка через rabbitmq-plugins
```
rabbitmq-plugins enable rabbitmq_management
```

Перезагружать сам Rabbit после установки плагина не надо.
Доступ к самой морде - по адресу http://{node-hostname}:15672/. 

Важно что UI и порт HTTP API - обычно 15672 — не поддерживают AMQP 0-9-1, AMQP 1.0, STOMP или MQTT соединения. 
Для этих клиентов надо настраивать отдельные порты.

### Настройка доступа к веб-морде через SSL/TLS


Ниже - типовые параметры в основном конфиге Rabbit-а для доступа к веб-морде по SSL.

```
management.ssl.port       = 15671
management.ssl.cacertfile = /path/to/ca_certificate.pem
management.ssl.certfile   = /path/to/server_certificate.pem
management.ssl.keyfile    = /path/to/server_key.pem
```

Более подробно описано тут: https://www.rabbitmq.com/ssl.html


## Redis


### Веб-морда:  

Первый и основной вариант - Redis Commander, решение на базе Node.JS  
Аргументы - большое количество недавних коммитов, количество обнаруженных и решенных issues на GitHub, заявленный функционал.  
Страница продукта:  
http://joeferner.github.io/redis-commander/  
Страница на GitHub:  
https://github.com/joeferner/redis-commander  

Процесс установки:

```
$ npm install -g redis-commander
$ redis-commander
```
Для автозагрузки redis-commander необходимо содать Systemd Unit File
```
# cat /etc/systemd/system/redis-commander.service
[Unit]
Description=Redis Commander
Documentation=https://github.com/joeferner/redis-commander
After=network.target

[Service]
Environment='HASH=$2a$10$vGdgUtoiS8snOysaNMWh5eh/ykZRC7lKu.bXHkQdPB7.rTfPBn7rO'
Type=simple
User=centos
ExecStart=/usr/bin/redis-commander --redis-password <redis-pass> --http-auth-username admin --http-auth-password-hash $HASH
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
В переменную HASH добавить хеш пароля админа.
Хеш можно вычислить на странице: [bcrypt](https://www.browserling.com/tools/bcrypt)

Связь с экземпляром Redis либо прямым подключением, либо через инстанс sentinel.


Второй вариант - проект Rebrow, веб-морда на базе Python и Flask: https://github.com/marians/rebrow

Процесс установки: 

```
git clone https://github.com/marians/rebrow.git
cd rebrow
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python runserver.py

Then open 127.0.0.1:5001.
```

