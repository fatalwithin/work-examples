# cloudba-webanalytics

Прототипирование и анализ работы различных решения для веб-аналитики и анализа поведения пользователей на веб-сайтах (в контексте данного пространства - на сайтах, относящихся к проекту Cloud-Based Education).

## Продукт №1 - count.ly

Основные компоненты: MongoDB + Node.JS.

Ресурс с документацией: https://resources.count.ly/docs/installing-countly-server

Адрес официального контейнера на Docker Hub: https://hub.docker.com/r/countly/countly-server/

### Подготовка

Вытащить последний образ Docker:

```bash
docker pull countly/countly-server
```

Сделать директорию под persistent-данные MongoDB:

```bash
mkdir /var/data/mongodb
```

Запустить контейнер, указав порт для перенаправления и том под хранение данных Монги:

```bash
docker run -d -P -p 80:80 -p 443:443 -v /var/data/mongodb:/var/lib/mongodb countly/countly-server
```

### Опыт использования

1) При старте контейнера с внешним томом для mongodb - почему-то не поднимается основное веб-приложение, nginx показывает 502 ошибку
2) Приложение не аналог Webvisor-а, а аналог скорее Google.Analytics. Не умеет делать replay сессий пользователей, не умеет показывать Click Heatmaps.

## Продукт №2 - Open Web Analytics (OWA)

Основные компоненты: PHP, MySQL.

Ресурс с документацией: https://github.com/padams/Open-Web-Analytics/wiki

Готовых контейнеров нет, дистрибутив требует PHP версии не меньше, чем 5.2 и внешнюю MySQL-базу. Имеет смысл сделать docker-compose-сборку.

### Подготовка

1) Вытащить последнюю версию дистрибутива, либо сделать git checkout: https://github.com/padams/Open-Web-Analytics/releases

2) Настроить nginx или apache таким образом, чтобы папка 'owa' была в доступности корневой директории веб-сервера.

3) Настроить MySQL/Maria DB таким образом, чтобы можно было задать следующие данные в мастере установки:

* db host - имя сервера
* db name - имя базы
* db user - имя пользователя с правами чтения и записи на базу
* db password - пароль пользователя

4) Запустить мастер установки по адресу: http://hostname/dir/subdir/.../owa/install.php

5) ...Profit!

### Архитектура:

* 3 контейнера:
** nginx - для обработки внешних запросов
** mariadb - для базы данных
** owa - для приложения

* Сборка - через docker-compose
