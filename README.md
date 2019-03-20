# WholeProgram
Django操作数据库
1.mysql指令：首先通过命令行登陆mysql数据库，创建数据库与相关用户
2.在Django的settings.py文件中配置DATABASES
3.通过django-admin startapp TestModel创建app
4.修改TestModel下的model.py文件
5.在Django的settings.py文件中的INSTALLED_APPS 加入model.py文件所在应用的名称
6.命令行执行python manage.py makemigrations TestModel
7.命令行执行python manage.py migrate即创建好对应的表

因为在app应用中的路径被包含在整个项目内，url(r'^wenshu', include(wenshu_urls)),
首先需要先匹配文书，在匹配addIdAndFilename，所以在浏览器应该访问如下url:
http://127.0.0.1:8000/wenshu/addIdAndFilename