```


 ..\env\Scripts\activate
 cd backend

 python manage.py runserver

 python manage.py makemigrations
 python manage.py migrate

 python manage.py createsuperuser

 django-admin startapp core
 django-admin startapp projects
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

npm install pnpm

pnpm install

pnpm  dev

npm install chart.js

https://pure-admin.cn/


## 4. 数据备份与恢复
除了在管理后台进行数据导入导出外，还可以使用 Django 的命令行工具进行数据备份和恢复：

### 4.1 备份数据
```
cd e:\projects\Django\keyan-sys\backend
python manage.py dumpdata --exclude auth.permission 
--exclude contenttypes > db_backup.json
```
### 4.2 恢复数据
```
cd e:\projects\Django\keyan-sys\backend
python manage.py loaddata db_backup.json
```
## 5. 运行开发服务器
完成以上配置后，运行开发服务器并访问 Django Admin 后台：

```
python manage.py runserver
```
在浏览器中访问 http://localhost:8000/admin/ ，使用超级用户凭据登录，您应该可以看到所有注册的模型，并能够进行数据的导入导出操作。

 --username admin --email admin@example.com --password admin123
docker-compose exec backend python manage.py createsuperuser


# 停止并移除现有的容器
docker-compose down

# 删除现有的PostgreSQL数据卷（注意：这会删除所有数据库数据！）
docker volume rm keyan-sys_postgres_data

# 重新构建并启动容器
docker-compose up --build -d