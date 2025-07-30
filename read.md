```
 ..\env\Scripts\activate

 python manage.py runserver

 python manage.py makemigrations
 python manage.py migrate

 python manage.py createsuperuser

 django-admin startapp core
 django-admin startproject back

 python manage.py makemigrations core users
 python manage.py migrate
 python manage.py collectstatic --noinput
 python manage.py loaddata initial_data.json
 python manage.py createsuperuser --username admin --email admin@example.com --password admin123
 python manage.py shell -c "from users.models import Team; Team.objects.create(name='Team 1', description='Description 1')"


```

访问 Swagger UI 文档
默认情况下，Django-Ninja 在以下路径提供 Swagger UI：
http://localhost:8000/api/v1/docs