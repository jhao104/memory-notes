> Nginx部署Django

## 安装Nginx

```
apt-get install nginx
```
```
sudo /etc/init.d/nginx start    # 启动
sudo /etc/init.d/nginx stop     # 停止
sudo /etc/init.d/nginx restart  # 重启
```


## 安装uwsgi

```
apt-get install python-dev
pip install uwsgi
```

## 测试uwsgi

新建test.py文件，
```
# test.py
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return ["Hello World"] # python2
    #return [b"Hello World"] # python3
```
然后执行shell命令：
```
uwsgi --http-socket :8001 --plugin python --wsgi-file test.py
```
加上--plugin python是告诉uWSGI在使用python插件，不然很有可能会出现类似这样的错误：
```
uwsgi: unrecognized option '--wsgi-file'
getopt_long() error
```
执行成功在浏览器中打开：http://localhost:8001显示Hello World说明uwsgi正常运行。

## 测试Django

首先得保证Django项目没有问题
```
python manage.py runserver 0.0.0.0:8001
```
访问http://localhost:8001,项目运行正常。
然后链接Django和uwsgi，实现简单的web服务器，到Django项目目录下执行shell:
```
uwsgi --http-socket :8001 --plugin python --module blog.wsgi
```
blog为你的项目名。访问http://localhost:8001，项目正常。注意这时项目的静态文件是不会被加载的，需要用nginx做静态文件代理。

## 配置uwsgi
uwsgi支持通过配置文件的方式启动，可以接受更多的参数，我们在Django项目目录下新建uwsgi.ini
```
# uwsgi.ini file
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir           = /home/ubuntu/blog
daemonize       = uwsgi.log
socket          = 0.0.0.0:8001
# Django's wsgi file
module          = blog.wsgi
# the virtualenv (full path)
home            = /home/ubuntu
# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 4
# the socket (use the full path to be safe
socket          = /home/ubuntu/mysite.sock
# ... with appropriate permissions - may be needed
# chmod-socket    = 664
# clear environment on exit
vacuum          = true
```

## 配置nginx



http://www.mamicode.com/info-detail-1442333.html