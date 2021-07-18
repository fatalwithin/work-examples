# Как пользоваться приватным PyPi-сервером  

## Общая информация  

Здесь и далее - примеры для Python3, то есть в явном виде в командах используются python3 и pip3. Для python2.7 используйте python2 и pip2.
Анонимного доступа нет.
Доступ только по HTTPS (SSL).

## Как получить учетную запись на внутреннем PyPi-сервере  

- придумать username и отправить Марселю/Данилу
- получить invite-ссылку, перейти по ней, ввести свой username, придумать пароль и зарегистрироваться на сервере

## Создание пакетов  

- установить следующие pip-пакеты: setuptools, wheel, twine, tqdm (далее примеры для Ubuntu Linux):

```bash
$ sudo python3 -m pip install --upgrade pip setuptools wheel
$ sudo python3 -m pip install tqdm
$ sudo python3 -m pip install --user --upgrade twine
```

- создать файл setup.py со всеми необходимыми вам метаданными
- скомпилировать пакет:

```bash
$ python3 setup.py bdist_wheel
```

## Загрузка пакета на внутренний PyPi-сервер  

- создать файл в домашней директории под названием .pypirc (на самом деле не обязательно в домашней - далее будет описано почему)

```bash
$ vim ~/.pypirc

[distutils]
index-servers=pypicloud

[pypicloud]
repository: https://pypi.sbear.ru/simple
username: 'ваш username (без кавычек)'
password: 'ваш пароль (без кавычек)'
```

- можно дополнительно защитить файл, если на компьютере работают другие пользователи:

```bash
$ chmod 600 ~/.pypirc
```

- загрузить пакет на сервер PyPi:

```bash
$ python3 -m twine upload dist/* --config-file ~/.pypirc --repository pypicloud
```

или, если хотите загрузить конкретную версию пакета,

```bash
$ python3 -m twine upload dist/<имя файла.whl> --config-file ~/.pypirc --repository pypicloud
```

- проверить, появился ли ваш пакет в веб-интерфейсе (поиск из консоли с доступом по HTTPS работает некорректно):
https://pypi.sbear.ru/#/


## Прописать в pip.conf (на любом уровне) PyPi-сервер в доверенные хосты  

Настройка может быть на уровне системы, пользователя или на уровне venv. 
Где находятся ваши настройки - смотрите здесь в зависимости от системы:
https://pip.pypa.io/en/stable/user_guide/#config-file

```bash
$ vim pip.conf

[global]
trusted-host = pypi.sbear.ru
```

## Установка пакета  

```bash
$ pip3 install -i https://pypi.sbear.ru/simple/ <имя_пакета>
```

или для установки конкретной версии 

```bash
$ pip3 install -i https://pypi.sbear.ru/simple/ <имя_пакета>=<номер версии>
```
Введите ваши username и пароль в приглашении командной строки.

## Установка хоста pypi перманентно

```bash
$ vim pip.conf

[global]
trusted-host = pypi.sbear.ru
index-url = https://login:password@pypi.sbear.ru/simple/
```
