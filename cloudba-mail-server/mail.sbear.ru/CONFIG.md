# Настройки почтового сервиса для домена sbear.ru

## Записи DNS 

1) A (HOST)

| NAME              | TTL    | TYPE   | DATA         |
|-------------------|--------|--------|--------------|
| mail.sbear.ru     | 14400  | A      | 212.47.250.89 |
| autodiscover      | 14400  | CNAME  | mail         |
| autoconfig        | 14400  | CNAME  | mail         |
| @                 | 14400  | MX     | mail         |

2) PTR

| NAME              | TTL    | TYPE   | DATA         |
|-------------------|--------|--------|--------------|
| 212.47.250.89      |  60    |  PTR   |  mail.sbear.ru |

3) SPF

| NAME              | TTL    | TYPE   | DATA         |
|-------------------|--------|--------|--------------|
| @         | 3600  |  IN TXT|  "v=spf1 mx ~all" |

4) DKIM

| NAME              | TTL    | TYPE   | DATA         |
|-------------------|--------|--------|--------------|
| dkim._domainkey   | 3600   |  IN TXT | "" |

5) DMARK

| NAME              | TTL    | TYPE   | DATA         |
|-------------------|--------|--------|--------------|

## Конфигурация сервера
* Internal IP: 10.64.38.121
* External IP: 212.47.250.89
* OS: Ubuntu Bionic Beaver (18.04 LTS)
* vCPU: 2
* vRAM: 2GB
* vDisk: 25GB


## Ошибки и нюансы

* Если при запуске docker-compose up -d вываливаются ошибки и несколько последних контейнеров не запускаются, то в качестве временного решения можно сделать так:
* COMPOSE_HTTP_TIMEOUT=200 docker-compose up -d