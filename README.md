## SMap (Share Map)

Create .env
```
SECRET_KEY=5(15ds+i2+%ik6z&!yer+ga9m=e%jcqiz_5wszg)r-z!2--b2d
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
DB_HOST=postgres
```

docker-compose up
```
docker-compose up
```

...And migration
```
(into web container)
docker-compose exec app ./manage.py makemigrations
docker-compose exec app ./manage.py migrate
```

Access http://localhost:8080
