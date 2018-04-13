> Django的部署可以有很多方式，采用nginx+uwsgi的方式是其中比较常见的一种方式。今天在Ubuntu上使用Nginx部署Django服务，虽然不是第一次搞这个了，但是发现还是跳进了好多坑，google了好久才搞定。想想还是把这个过程记录下来，免得下次再来踩同样的坑。

## 安装Nginx

```shell
apt-get install nginx
```

ubantu安装完Nginx后，文件结构大致为：
　　所有的配置文件都在 /etc/nginx下；
　　启动程序文件在 /usr/sbin/nginx下；
　　日志文件在 /var/log/nginx/下，分别是access.log和error.log；
　　并且在  /etc/init.d下创建了启动脚本nginx。
```shell
sudo /etc/init.d/nginx start    # 启动
sudo /etc/init.d/nginx stop     # 停止
sudo /etc/init.d/nginx restart  # 重启
```


## 安装uwsgi

```shell
apt-get install python-dev
pip install uwsgi
```
至于为什么要使用uwsgi,可以参见这边博客：[快速部署Python应用：Nginx+uWSGI配置详解(1)](http://developer.51cto.com/art/201010/229615.htm)。
这样大体的流程是：nginx作为服务器最前端，负责接收client的所有请求，统一管理。静态请求由Nginx自己处理。非静态请求通过uwsgi传递给Django，由Django来进行处理，从而完成一次WEB请求。
通信原理是：
`the web client <-> the web server(nginx) <-> the socket <-> uwsgi <-> Django`

## 测试uwsgi

在Django项目下新建test.py文件，
```python
# test.py
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return ["Hello World"] # python2
    #return [b"Hello World"] # python3
```
然后执行shell命令：
```shell
uwsgi --http :8001 --plugin python --wsgi-file test.py
```
加上--plugin python是告诉uWSGI在使用python插件，不然很有可能会出现类似这样的错误：
```shell
uwsgi: unrecognized option '--wsgi-file'
getopt_long() error
```
执行成功在浏览器中打开：http://localhost:8001显示Hello World说明uwsgi正常运行。

## 测试Django

首先得保证Django项目没有问题
```shell
python manage.py runserver 0.0.0.0:8001
```
访问http://localhost:8001,项目运行正常。
然后链接Django和uwsgi，实现简单的web服务器，到Django项目目录下执行shell:
```shell
uwsgi --http :8001 --plugin python --module blog.wsgi
```
blog为你的项目名。访问http://localhost:8001，项目正常。注意这时项目的静态文件是不会被加载的，需要用nginx做静态文件代理。

## 配置uwsgi
uwsgi支持通过配置文件的方式启动，可以接受更多的参数，高度可定制。我们在Django项目目录下新建uwsgi.ini
```
[uwsgi]
# Django-related settings

socket = :8001

# the base directory (full path)
chdir           = /home/ubuntu/blog

# Django s wsgi file
module          = blog.wsgi

# process-related settings
# master
master          = true

# maximum number of worker processes
processes       = 4

# ... with appropriate permissions - may be needed
# chmod-socket    = 664
# clear environment on exit
vacuum          = true
```
在shell中执行：
```shell
sudo uwsgi --ini uwsgi.ini 
```
ps:如果实在不想配置nginx的话，单uwsgi就已经能完成部署了（把socket换成http），你可以把Django中的静态文件放到云平台中如七牛等等，这样你的Web也能被正常访问。

## 配置nginx

nginx默认会读取`/etc/nginx/sites-enabled/default`文件中的配置，修改其配置如下:

```python
server {
    # the port your site will be served on
    listen      80;
    # the domain name it will serve for
    server_name 127.0.0.1; # substitute your machine's IP address or FQDN
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media  {
        alias /home/ubuntu/blog/media;  # your Django project's media files - amend as required
    }

    location /static {
        alias /home/ubuntu/blog/static; # your Django project's static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        include     uwsgi_params; # the uwsgi_params file you installed
        uwsgi_pass 127.0.0.1:8001;
    }
}
```
## 收集Django静态文件

把Django自带的静态文件收集到同一个static中，不然访问Django的admin页面会找不到静态文件。在django的setting文件中，添加下面一行内容：
```python
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
```
然后到项目目录下执行:

```shell
python manage.py collectstatic
```

修改配置文件
```python
DEBUG = False
ALLOWED_HOSTS = ['*']
```
## 运行

一切配置好后直接重启nginx即可。更加详细的说明请参见[官方文档](http://uwsgi-docs.readthedocs.io/en/latest/BuildSystem.html)

## 可能遇到的问题

[如果监听80端口，部署后访问localhost自动跳转到nginx默认的欢迎界面](https://segmentfault.com/q/1010000007047896?_ea=1227923)

[uwsgi: option ‘--http‘ is ambiguous](http://www.mamicode.com/info-detail-1442333.html)

[把settings.py中的DEBUG设置为False前端页面显示不正常了](https://www.v2ex.com/t/184979)