## 这是一个资产管理项目，Client是运行在各个资产端，将自身的数据发送到assets app，该项目将数据收集并进行管理，前端使用adminlet进行展示，后端是django admin对资产数据进行管理，实现资产数据的增删改查

先创建虚拟环境
使用pip安装第三方依赖
修改settings.example.py文件为settings.py,并填写自己的key
运行migrate命令，创建数据库和数据表
在client端修改要发送的服务器的ip，端口等，正确配置
运行python manage.py runserver启动服务器