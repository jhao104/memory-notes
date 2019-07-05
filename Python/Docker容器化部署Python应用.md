### 1. 简介

[Docker](https://www.docker.com/)是目前主流IT公司广泛接受和使用的，用于构建、管理和保护它们应用程序的工具。

容器，例如Docker允许开发人员在单个操作系统上隔离和运行多个应用程序，而不是为服务器上的每个应用程序专用一个虚拟机。使用容器更轻量级，可以降低成本、更好地使用资源和发挥更高的性能。

本文将使用Flask开发一个简单的Python web应用程序，并为“容器化”做好准备。然后创建一个Docker映像，并将其部署到测试和生产环境中。

**注意：** 请确保机器上已安装Docker，如果没有请参考[Docker官方安装教程](https://docs.docker.com/install/)。

### 2. Docker介绍

Docker是一种工具，它使开发人员能够交付他们的应用程序(以及库或其他依赖项)，确保他们可以使用正确的配置运行，而不受部署环境影响。

这是通过将应用程序隔离在单独的容器中来实现的，这些应用程序虽然被容器分隔开，但是却可以共享操作系统和其他资源。

Docker包含两部分:

* **[Docker Engine](https://docs.docker.com/engine/)** — 应用打包工具，用于封装应用程序。

* **[Docker Hub](https://hub.docker.com/)** — 用于管理云上容器应用程序的工具。

### 3.为何选择容器

了解容器的重要性和实用性非常重要，虽然它和直接将应用部署到服务器没有多大区别，但是当涉及到比较复杂的且相当吃资源的应用，尤其是多个应用部署在同一台服务器，或是同一应用要部署到多台服务器时。容器就变得非常有用。

在容器之前，这是通过 [VMWare](https://www.vmware.com/) 和 [Hypervisor](https://en.wikipedia.org/wiki/Hypervisor)等虚拟机解决的，但是它们在效率、速度和可移植性方面已被证明并不是最佳选择。

Docker容器是虚拟机的轻量级的替代品-与VM不同，我们不需要为它预先分配RAM、CPU或其他资源，也不需要为每个应用程序启动一个VM，仅仅只需要一个操作系统即可。

使用容器开发人员就不需要为不同环境制定特殊版本，这样可以专注于应用程序的核心业务逻辑。

### 4.创建Python应用

[Flask](http://flask.pocoo.org/)是Python的一个轻量级Web应用框架，简单易用，可以很快速地创建web应用。我们用它来创建此demo应用。

如果还没有安装Flask模块，可以使用下面命令安装:

```shell
$ pip install flask
```

安装成功后，新建一个应用目录，命名为`FlaskDemo`。并在该目录下创建应用代码文件`app.py`。

在`app.py`中，首先引入`Flask`模块，然后创建一个web应用:

```python
from flask import Flask

app = Flask(__name__)
```

然后定义路由`/`和其对应的请求处理程序:

```python
@app.route("/")
def index():  
  return """
  <h1>Python Flask in Docker!</h1>
  <p>A sample web-app for running Flask inside Docker.</p>
  """
```

最后，添加运行主程序并启动该脚本:

```python
if __name__ == "__main__":  
    app.run(debug=True, host='0.0.0.0')
```

```shell
$ python app.py
```

然后在浏览器中访问`http://localhost:5000/`,可以看到`Dockerzing Python app using Flask`这样的页面。

![](http://qiniu.spiderpy.cn/19-5-28/dockerizing-python-applications-1.png)


### 5.Dokcer打包应用

要在Docker上运行应用程序，首先必须构建一个容器，而且必须包含使用的所有依赖项——在我们的例子中只有Flask。因此，新建一个包含所有依赖包的 `requirements.txt` 文件，然后创建一个Dockerfile，该文件用来描述构建映像过程。

此外，当启动容器时还需要放开应用程序的`HTTP`端口。

#### 准备工作

`requirements.txt` 文件非常简单，只需要填入项目的依赖包和其对应版本即可：

```python
Flask==1.0.2 
```

接下来，需要将应用程序运行所需的所有Python文件都放在顶层文件夹中，例如，名为`app`的目录。

同时建议将主入口程序命名为 `app.py` ，将脚本中创建的Flask对象命名为 `app` 是一种通常的做法，这样也可以简化部署。

```python
FlaskApp  
    ├── requirements.txt
    ├── Dockerfile
    └── app
        └── app.py
        └── <other .py files>
```

#### 创建Dockerfile

Dockerfile本质上是一个文本文件，其中明确定义了如何为我们的项目构建Docker镜像。

接下来创建一个基于Ubuntu 16.04 和 Python 3.X的Dokcer镜像:
```python
FROM ubuntu:16.04

MAINTAINER jhao104 "j_hao104@163.com"

RUN apt-get update -y && \  
    apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3" ]

CMD [ "app/app.py" ] 
```

Dockerfile的基本指令有十三个,上面用到了部分；

* **FROM** - 所有Dockerfile的第一个指令都必须是 `FROM` ，用于指定一个构建镜像的基础源镜像，如果本地没有就会从公共库中拉取，没有指定镜像的标签会使用默认的latest标签，如果需要在一个Dockerfile中构建多个镜像，可以使用多次。

* **MAINTAINER** - 描述镜像的创建者，名称和邮箱。

* **RUN** - RUN命令是一个常用的命令，执行完成之后会成为一个新的镜像，通常用于运行安装任务从而向映像中添加额外的内容。在这里，我们需更新包，安装 `python3` 和 `pip` 。在第二个 `RUN` 命令中使用 `pip` 来安装 `requirements.txt` 文件中的所有包。

* **COPY** - 复制本机文件或目录，添加到指定的容器目录, 本例中将 `requirements.txt` 复制到镜像中。

* **WORKDIR** - 为RUN、CMD、ENTRYPOINT指令配置工作目录。可以使用多个WORKDIR指令，后续参数如果是相对路径，则会基于之前命令指定的路径。

* **ENTRYPOINT** - 在启动容器的时候提供一个默认的命令项。

* **RUN** - 运行 `app` 目录中的 `app.py` 。

#### Docker镜像构建原理

Docker镜像是使用 `Docker build` 命令构建的。在构建镜像时，Docker创建了所谓的“层(layers)”。每一层都记录了Dockerfile中的命令所导致的更改，以及运行命令后镜像的状态。

Docker在内部缓存这些层，这样在重新构建镜像时只需要重新创建已更改的层。例如，这里使用了 `ubuntu:16.04` 的基础镜像，相同容器的所有后续构建都可以重用它，因为它不会改变。但是，因为项目修改，在下次重新构建过程中 `app` 目录的内容可能会有所不同，因此只会重新构建这一层。

需要注意的是，每当重新构建某一层时，`Dockerfile` 中紧随其后的所有层也都需要重新构建。例如，我们首先复制 `requirements.txt` 文件，然后再复制应用程序的其余部分。这样之前安装的依赖项只要没有新的依赖关系，即使应用程序中的其他文件发生了更改，也不需要重新构建这一层。这一点在创建 `Dockerfiles` 时一定要注意。

因此，通过将 `pip` 安装与应用程序其余部分的部署分离，可以优化容器的构建过程。

#### 构建Docker镜像

现在 `Dockerfile` 已经准备好了，而且也了解了Docker的构建过程，接下来为我们的应用程序创建Docker映像:

```shell
docker build -t docker-flask:0.1 .
```

#### 调试模式运行

根据前面讲到的容器化的优点，开发的应用程序通过容器部署，这从一开始就确保了应用程序构建的环境是干净的，从而消除了交付过程中的意外情况。

但是呢，在开发应用程序的过程中，更重要的是要快速重新构建和测试，以检查验证过程中的每个中间步骤。为此，web应用程序的开发人员需要依赖于Flask等框架提供的自动重启功能（Debug模式下，修改代码自动重启）。而这一功能也可以在容器中使用。

为了启用自动重启，在启动Docker容器时将主机中的开发目录映射到容器中的app目录。这样Flask就可以监听主机中的文件变化(通过映射)来发现代码更改，并在检测到更改时自动重启应用程序。

此外，还需要将应用程序的端口从容器转发到主机。这是为了能够让主机上的浏览器访问应用程序。

因此，启动Dokcer容器时需要使用  _volume-mapping_ 和 _port-forwarding_ 选项：

```shell
docker run --name flask_app -v $PWD/app:/app -p 5000:5000 docker-flask:0.1
```

改命令将会执行以下操作:

* 基于之前构建的 `docker-flask` 镜像启动一个容器；

* 这个容器的名称被设置为 `flask_app` 。如果没有 `——name` 选项，Docker将为容器生成一个名称。显式指定名称可以帮助我们定位容器(用来停止等操作)；

* `-v` 选项将主机的app目录挂载到容器；

* `-p` 选项将容器的端口映射到主机。

现在可以通过`http://localhost:5000` 或者 `http://0.0.0.0:5000/` 访问到应用:

![](http://qiniu.spiderpy.cn/19-6-26/1.png)

如果我们在容器运行的时候，修改应用程序代码，Flask会检测到更改并重新启动应用程序。

![](http://qiniu.spiderpy.cn/19-06-26/2.gif)

要停止容器的话，可以使用 `Ctrl` + `C`, 并运行 `docker rm flask_app` 移除容器。

#### 生产模式运行

虽然直接使用Flask裸跑运行应用程序对于开发来说已经足够好了，但是我们需要在生产中使用更健壮的部署方法。

目前主流的部署方案是 `nginx` + `uwsgi`，下面我们将介绍如何为生产环境部署web应用程序。[Nginx](http://nginx.org/)是一个开源web服务器，[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/index.html)是一个快速、自我修复、开发人员和系统管理员友好的服务器。

首先，我们创建一个入口脚本，用来控制以开发模式还是生产模式启动我们的应用程序，这两者区别是选择直接运行python还是nginx模式。

然后再写一个简单shell启动脚本 `entry-point.sh`:
```shell
#!/bin/bash

if [ ! -f /debug0 ]; then  
  touch /debug0

  while getopts 'hd:' flag; do
    case "${flag}" in
      h)
        echo "options:"
        echo "-h        show brief help"
        echo "-d        debug mode, no nginx or uwsgi, direct start with 'python3 app/app.py'"
        exit 0
        ;;
      d)
        touch /debug1
        ;;
      *)
        break
        ;;
    esac
  done
fi

if [ -e /debug1 ]; then  
  echo "Running app in debug mode!"
  python3 app/app.py
else  
  echo "Running app in production mode!"
  nginx && uwsgi --ini /app.ini
fi  
```

然后创建[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/Configuration.html)配置文件 `app.ini`:
```python
[uwsgi]
plugins = /usr/lib/uwsgi/plugins/python3  
chdir = /app  
module = app:app  
uid = nginx  
gid = nginx  
socket = /run/uwsgiApp.sock  
pidfile = /run/.pid  
processes = 4  
threads = 2 
```

和nginx配置文件 **nginx.conf**:

```
user nginx;
worker_processes  4;
pid /run/nginx.pid;

events {
    worker_connections  20000;
}

http {
    include    mime.types;
    sendfile on;
    keepalive_timeout  65;
    gzip off;

    server {
        listen 80;
        access_log off;
        error_log off;

        location / { try_files $uri @flaskApp; }
        location @flaskApp {
            include uwsgi_params;
            uwsgi_pass unix:/run/uwsgiApp.sock;
        }
    }
}
```

最后，修改`Dockerfile` 将`nginx`和`uWSGI`安装到镜像,将配置文件复制到镜像中,并设置运行nginx所需的用户权限:
```python
FROM ubuntu:16.04

MAINTAINER jhao104 "j_hao104@163.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev && \
    apt-get install -y nginx uwsgi uwsgi-plugin-python3

COPY ./requirements.txt /requirements.txt
COPY ./nginx.conf /etc/nginx/nginx.conf

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

RUN adduser --disabled-password --gecos '' nginx\
  && chown -R nginx:nginx /app \
  && chmod 777 /run/ -R \
  && chmod 777 /root/ -R

ENTRYPOINT [ "/bin/bash", "/entry-point.sh"]

```

然后重新打包镜像:
```shell
docker build -t docker-flask:0.1 .
```

然后使用nginx启动应用程序：
```shell
docker run -d --name flaskapp --restart=always -p 8091:80 docker-flask:0.1
```

该镜像包含python、ngix、uwsgi完整环境，只需要在部署时指定端口映射便可以自动部署应用。要停止并删除此容器，请运行下面命令：
```shell
docker stop flaskapp && docker rm flaskapp
```

此外，如果我们仍然需要上面调试功能或修改部分代码，也可以像上面一样以调试模式运行容器:
```shell
docker run -it --name flaskapp -p 5000:5000 -v $PWD/app:/app docker-flask:0.1 -d debug
```

### 6.管理外部依赖

如果将应用程序作为容器交付时，需要记住的一个关键事项是，开发人员管理依赖项的责任增加了。除了识别和指定正确的依赖项和版本之外，还需要负责在容器环境中安装和设置这些依赖项。

在Python项目中管理安装依赖比较容易，可以使用`requirements.txt`指定依赖项和对应版本，然后通过 `pip` 安装。

需要重申的是是，无论何时修改 `requirements.txt` 文件，都需要重新构建Docker镜像。

#### 启动时安装依赖项

可能在某次版本更新时需要安装额外的依赖项。比如，在开发过程中使用了一个新的包。如果不希望每次都重新构建Docker镜像，或者希望在启动时使用最新的可用版本。可以通过修改启动程序在应用程序启动时运行安装程序来实现这一点。

同样，我们也可以安装额外的系统级包依赖项。修改 `entry-point.sh`:

```shell
#!/bin/bash

if [ ! -f debug0 ]; then
  touch debug0
  
  if [ -e requirements_os.txt ]; then
    apt-get install -y $(cat requirements_os.txt)
    
   fi
   if [-e requirements.txt ]; then
    pip3 install -r requirements.txt
   fi

  while getopts 'hd:' flag; do
    case "${flag}" in
      h)
        echo "options:"
        echo "-h        show brief help"
        echo "-d        debug mode, no nginx or uwsgi, direct start with 'python3 app/app.py'"
        exit 0
        ;;
      d)
        touch debug1
        ;;
      *)
        break
        ;;
    esac
  done
fi

if [ -e debug1 ]; then
  echo "Running app in debug mode!"
  python3 app/app.py
else
  echo "Running app in production mode!"
  nginx && uwsgi --ini /app.ini
fi

```

这样我们可以在 `requirements_os.txt` 中指定将要安装的系统软件包名称，这些包名以空格分隔放在同一行。他们将和 `requirements.txt` 中的Python依赖库一样在应用程序启动之前安装。

尽管这样对应用的迭代开发期间提供了便利，但是出于几个原因，在启动时安装依赖项不是一个好的实践：

* 它破坏了容器化的目标之一，即修复和测试由于部署环境的变化而不会改变的依赖关系；

* 增加了应用程序启动的额外开销，这将增加容器的启动时间；

* 每次启动应用程序时需要安装依赖项，这样对网络资源有要求。

