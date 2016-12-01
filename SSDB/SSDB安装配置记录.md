>SSDB的性能很突出，与Redis基本相当了，Redis是内存型，容量问题是弱项，并且内存成本太高，SSDB针对这个弱点，使用硬盘存储，使用Google高性能的存储引擎LevelDB，适合大数据量处理并把性能优化到Redis级别，具有Redis的数据结构、兼容Redis客户端，还给出了从Redis迁移到SSDB的方案。

本文是将我安装和测试的步骤记录下来，总结成文档，便于日后使用。
## 1、编译安装

照着官方的教程下载安装：

### 下载：
```
wget --no-check-certificate https://github.com/ideawu/ssdb/archive/master.zip
```
### 解压：
```
unzip master
```
一切顺利，进入解压后的目录执行：
```
make
```
但是编译报错：
```
ERROR! autoconf required! install autoconf first
Makefile:4: build_config.mk: No such file or directory
make: *** No rule to make target `build_config.mk'.  Stop.
```
原来是没有autoconf不能实现自动编译，于是安装autoconf:
```
sudo apt-get update
sudo apt-get install autoconf
```
然后继续执行，又报错：
```
make[1]: g++: Command not found
make[1]: *** [db/builder.o] Error 127
```
原来是新买的vps没有安装gcc的编译器，于是又将其补上：
```
sudo apt-get install build-essential
```
然后继续make编译，顺利完成。
### 安装：
```
sudo make install
```

## 2、启动
默认配置是安装在 /usr/local/ssdb,进入该目录下:
```
./ssdb-server ssdb.conf
# 此命令会阻塞命令行

# 或者启动为后台进程(不阻塞命令行)
./ssdb-server -d ssdb.conf
```

## 3、停止

```
./ssdb-server ssdb.conf -s stop
```

## 参考

[官方文档](http://ssdb.io/docs/zh_cn/install.html)

[SSDB 安装部署及注意事项大全](http://www.izhangheng.com/ssdb/)

[SSDB项目地址](https://github.com/ideawu/ssdb)
