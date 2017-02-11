## SMap (Share Map)

Create .env
```
SECRET_KEY=5(15ds+i2+%ik6z&!yer+ga9m=e%jcqiz_5wszg)r-z!2--b2d
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
DB_SERVICE=postgres
DB_PORT=5432
DEBUG=true
```

docker-compose up
```
docker-compose up
```

...And migration
```
docker-compose exec web bash
(into web container)
python manage.py makemigrations todo
python manage.py migrate
```

Access http://localhost:8080
