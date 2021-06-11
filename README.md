# Мини Апи

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