# Настройки почтового сервиса для домена cloudba.ru

## Записи DNS

1) A (HOST)

 NAME              | TTL    | TYPE   | DATA         
------------ | ------------ | ------------ | ------------
mail.cloudba.ru   |  14400 |  A     |  51.15.111.50 
autodiscover      |  14400 |  CNAME |  mail   
autoconfig        |  14400 |  CNAME |  mail   
@                 |  14400 |  MX    |  mail   

2) PTR

NAME              | TTL    | TYPE   | DATA         
-------------------|--------|--------|--------------
51.15.111.50      |  60    |  PTR   |  mail.cloudba.ru 

3) SPF

NAME              | TTL    | TYPE   | DATA         
-------------------|--------|--------|--------------
@         |   3600 |  IN TXT |  "v=spf1 mx ~all" 

4) DKIM

NAME              | TTL    | TYPE   | DATA         
-------------------|--------|--------|--------------
 dkim._domainkey   |  3600  |    IN TXT |  "v=DKIM1;k=rsa;t=s;s=email;p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu4Dbcyt00/ly338glpRxXgYfeTpjV5WjR+ltjqpMJ1K+hWuFuir6r13OJETcbM+uIqYKPPMIJpaj2BA+U69yQVl3jDfuadPRkGBmjptjnFb8d8R+aSds/NXq7pSpQLRhI+mqWw+eKEcOSKCf5q9RFh+vfHhlYiwLCW9IoLh2JjdBsUzJVjQNMdVuFKDva6PQx4H3x6yGIoIXqwrot22OwSj2ykzYeMTVbRKAgqU50+kY6xOpD552nr5jwOkPazACNS0PDDH3Zf0NiDcYc0qW4PXpt2oxb9fqNhZF8Cg7Upba869Z7PK1AUsnqNqC1L6Sb+BwJaeNA0MIBnIevN7V/wIDAQAB" 

5) DMARK
* ...TBD...

## Конфигурация сервера
* Internal IP: 10.21.33.17
* External IP: 51.15.111.50
* OS: Ubuntu Xenial (16.04 LTS)
* vCPU: 1
* vRAM: 1GB
* vDisk: 25GB
* 

## Ошибки и нюансы

* Если при запуске docker-compose up -d вываливаются ошибки и несколько последних контейнеров не запускаются, то в качестве временного решения можно сделать так:
* COMPOSE_HTTP_TIMEOUT=200 docker-compose up -d