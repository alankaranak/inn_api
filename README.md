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

## Ход работы

Отправьте POST запрос по адресу `https://example.com/api/v1/` с параметрами `uid`, `inn`, `address` в теле запроса

`uid` - Уникальный идентификатор пользователя

`inn` - ИНН организации

`address` - Адрес организации

Если в базе существует совпадение по всем трем полям, то в сервер ответит `1`, иначе `0`
