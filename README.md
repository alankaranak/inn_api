# Мини Апи

## Сервер

### Установите curl
```
sudo apt update
sudo apt install curl
```
### Установка Docker
Поэтапно введите следующие команды
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```
sudo chmod +x /usr/local/bin/docker-compose
```
Проверьте установку следующей командой
```
docker-compose --version
```
Пример ответа, если установка прошла успешно

`docker-compose version 1.29.2, build 1110ad01`

## Docker 
1. Создайте файл .env;
2. Скопируйте туда содержимое .env.template;
3. Внесите ваши настройки в .env
4. Запустите `docker-compose up --build`

## Django
Создать супер-пользователя:
```
docker-compose exec app python manage createsuperuser
```
Создать файлы миграции:
```
docker-compose exec app python manage.py makemigrations 
```
Провести миграции:
```
docker-compose exec app python manage.py migrate
```
Заполнить БД данными из .csv файлов
```
docker-compose exec app python manage.py --filename="наименование-вашего-файла.csv"
```

## Документация

https://example.com/swagger - Автодокументация апи

## Авторизация 
Отправьте POST запрос по адресу `http://lic.meapp.ru/auth/token/` с параметрами `username`, `password` в теле запроса, где

`username` - Имя зарегистрированного пользователя

`password` - Пароль зарегистрированного пользователя

Если такой пользователь существует, а также переданные вам данные верны, то сервер ответит токеном авторизации

После этого добавьте в ваш запрос новый заголовок `Authorization` и дайте ему значение `token полученный-вами-токен`

## Ход работы

### Проверка лицензии
Отправьте GET запрос по адресу `http://lic.meapp.ru/api/v1/license/scan/` с параметрами `uid`, `inn`, `address`, `include_date` в теле запроса

`uid` - Уникальный идентификатор пользователя

`inn` - ИНН организации

`address` - Адрес организации

`include_date` - Опциональный параметр, булево, проверять ли срок лицензии на истечение

Если в базе существует совпадение по всем трем полям, то в сервер ответит `1`, иначе `0`

### Загрузка CSV файла лицензий
Отправьте POST запрос по адресу `http://lic.meapp.ru/api/v1/exchange/upload/` с параметром `file` в теле запроса.

`file` - Ваш .csv файл

После успешной обработки файла будет получен ответ со статусом 200

### Количество лицензий у компании
Отправьте GET запрос по адресу `http://lic.meapp.ru​/api​/v1​/company​/{inn}​/nol​/`, где `{inn}` - искомый ИНН

Если по искомому ИНН найдена организация, то сервер ответит количеством лицензий, иначе будет получен ответ со статусом 404
