    DockerHub开启付费功能后，自动构建的功能不再免费开放了，这样Github的项目就不能再免费自动构建docker镜像并自动发布到DockerHub上。

## 前言

这里记录下使用 GitHub Actions持续集成服务自动构建发布镜像到DockerHub，目前GitHub Actions是免费开放的，所以Github上的项目都可以使用它来发布、测试、部署等等，非常方便。Github Actions [官方文档](https://docs.github.com/cn/actions)

## 配置

首先在项目中创建目录 `.github/workflows`， 然后在该目录中新建一个 `.yml` 文件，这里命名为 `docker-image.yml` 。 文件的名字没有实际意思，一个文件代表一个workflow任务。

文件内容如下(文件中`#`开头的为注释，是为方便理解加上去的):

```yaml
# docker-image.yml
name: Publish Docker image   # workflow名称，可以在Github项目主页的【Actions】中看到所有的workflow

on:   # 配置触发workflow的事件
  push:
    branches:   # master分支有push时触发此workflow
      - 'master'
    tags:       # tag更新时触发此workflow
      - '*'

jobs:  # workflow中的job

  push_to_registry:  # job的名字
    name: Push Docker image to Docker Hub
    runs-on: ubuntu-latest   # job运行的基础环境

    steps:  # 一个job由一个或多个step组成
      - name: Check out the repo
        uses: actions/checkout@v2   # 官方的action，获取代码

      - name: Log in to Docker Hub
        uses: docker/login-action@v1  # 三方的action操作， 执行docker login
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}  # 配置dockerhub的认证，在Github项目主页 【Settings】 -> 【Secrets】 添加对应变量
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract metadata (tags, labels) for Docker
        id: meta
        uses: docker/metadata-action@v3  # 抽取项目信息，主要是镜像的tag
        with:
          images: jhao104/proxy_pool

      - name: Build and push Docker image
        uses: docker/build-push-action@v2 # docker build & push
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

配置中大部分我都加上了注释，需要特别说明的是 `steps` 中的 `uses` 。 我们以第二个step `Log in to Docker Hub` 为例，正常情况下，我们应该是运行 `run docker login **` 。
这里使用了一个 action [docker/login-action](https://github.com/marketplace/actions/docker-login)，action 其实就是一系列step的组成，所以既然别人已经做好了，干嘛不直接用呢。所有可用的 action可以到 [这里](https://github.com/marketplace?type=actions) 查找。

## 使用

配置妥当之后，提交代码推送至github。按照本例中的配置，只要master分支有push事件或者tag有更新，就会触发Github Action，然后自动构建镜像推送至DockerHub。

可以在Github项目主页的【Actions】栏中查看每次执行详情，例如:

![](http://img.qiniu.spiderpy.cn/blog/52/1640934626.jpg)

可以点击每一个step查看输出日志。

上面的配置注意两个部分，一是step 2的Dockerhub认证配置，你需要将你的Dockerhub用户名和Token(在Dockerhub页面生成)配置为Github项目主页的 【Settings】 -> 【Secrets】的变量。
二是，step 3中将`images`的名字改为你自己的，镜像的tag会自动抽取，默认情况下，如果是分支，镜像tag则为分支名，如果为github tag 则会推送 tag 和 `latest` 两个镜像，具体配置参见 [docker-metadata-action](https://github.com/marketplace/actions/docker-metadata-action) 。 

