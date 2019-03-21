# WholeProgram
Django操作数据库
1.mysql指令：首先通过命令行登陆mysql数据库，创建数据库与相关用户
2.在Django的settings.py文件中配置DATABASES
3.通过django-admin startapp TestModel创建app
4.修改TestModel下的model.py文件
5.在Django的settings.py文件中的INSTALLED_APPS 加入model.py文件所在应用的名称
6.命令行执行python manage.py makemigrations TestModel
7.命令行执行python manage.py migrate即创建好对应的表

ajax发送的请求，url延时问题，将ajax的参数cache设置为false

因为在app应用中的路径被包含在整个项目内，url(r'^wenshu', include(wenshu_urls)),
首先需要先匹配文书，在匹配addIdAndFilename，所以在浏览器应该访问如下url:
http://127.0.0.1:8000/wenshu/addIdAndFilename

前端中，在一个界面如result_fact界面，点击按钮“1th”会跳转到content界面（在对应的index_result.js文件中），
跳转后的界面将以result_fact作为父路径，即/result_fact/content，url应该匹配路径/result_fact/content，并且在
content.html中应该对引入的srcipt文件加两层父路径


