> 环境： 14.04.1-Ubuntu

## 1、安装Nginx
```shell
apt-get install nginx
```
ubantu安装完Nginx后，文件结构大致为：

　　所有的配置文件都在 `/etc/nginx`下；

　　启动程序文件在 `/usr/sbin/nginx`下；

　　日志文件在 `/var/log/nginx/`下，分别是access.log和error.log；

　　并且在  `/etc/init.d`下创建了nginx启动脚本

安装完成后可以尝试启动nginx:
```shell
/etc/init.d/nginx start
```
然后能通过浏览器访问到 http://localhost/, 一切正常，如不能访问请检查原因。

## 2、安装PHP 和php-fpm

```shell
sudo apt-get install php5-fpm
sudo apt-get install php5-gd  # Popular image manipulation library; used extensively by Wordpress and it's plugins.
sudo apt-get install php5-cli   # Makes the php5 command available to the terminal for php5 scripting
sudo apt-get install php5-curl    # Allows curl (file downloading tool) to be called from PHP5
sudo apt-get install php5-mcrypt   # Provides encryption algorithms to PHP scripts
sudo apt-get install php5-mysql   # Allows PHP5 scripts to talk to a MySQL Database 
sudo apt-get install php5-readline  # Allows PHP5 scripts to use the readline function
```

查看php5运行进程：

```shell
ps -waux | grep php5
```

启动关闭php5进程

```shell
sudo service php5-fpm stop
sudo service php5-fpm start
sudo service php5-fpm restart
sudo service php5-fpm status
```


## 3、配置php和nginx

nginx的配置文件 `/etc/nginx/nginx.conf中include了/etc/nginx/sites-enabled/*`，因此可以去修改`/etc/nginx/sites-enabled`下的配置文件

```shell
vi /etc/nginx/sites-available/default
```

做如下修改：

```
location ~ \.php$ {
        #       fastcgi_split_path_info ^(.+\.php)(/.+)$;
                # NOTE: You should have "cgi.fix_pathinfo = 0;" in php.ini
                # With php5-cgi alone:
        #       fastcgi_pass 127.0.0.1:9000;
                # With php5-fpm:
        #       try_files $uri =404;
                fastcgi_pass unix:/var/run/php5-fpm.sock;
                fastcgi_index index.php;
                include fastcgi_params;
        }
```

还需要在`/etc/nginx/fastcgi_params`添加如下两句：
```
fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
fastcgi_param PATH_INFO $fastcgi_script_name;
```

然后reload Nginx：
```shell
sudo service nginx reload
```

## 4、验证php是否配置成功

新建phpinfo.php文件：
```shell
sudo vim /usr/share/nginx/html/phpinfo.php
```

内容如下：
```
<?php phpinfo(); ?>
```
然后通过浏览器访问：http://localhost/phpinfo.php 
能够看到php的详细信息则说明配置成功。
![php配置成功](http://ofcf9jxzt.bkt.clouddn.com/ssdb/p3.png)

## 5、下载phpssdbadmin

下载phpssdbadmin到`/usr/share/nginx/html`目录下：

```shell
cd /usr/share/nginx/html
git clone https://github.com/ssdb/phpssdbadmin.git
```


## 5、配置phpssdbadmin

修改phpssdbadmin的配置，修改`app/config/config.php`,将host和port改为ssdb配置的值：
```
'ssdb' => array(  
    'host' => '127.0.0.1',  
    'port' => '8888',  
),  
# 如果使用新版的phpssdbadmin，还需要修改用户名和密码，因为原始密码太简单不允许登录：
'login' => array(
                'name' => 'jinghao',
                'password' => 'jinghao123', // at least 6 characters
        ),
```


修改nginx的配置文件：
```shell
vim /etc/nginx/sites-enabled/default
```
添加：
```
location /phpssdbadmin {  
    try_files $uri $uri/ /phpssdbadmin/index.php?$args;  
    index index.php;  
}  
```
重启nginx，然后访问http://localhost/phpssdbadmin ,出现登录页面则配置成功。

![登陆页面](http://ofcf9jxzt.bkt.clouddn.com/ssdb/p1.png)
![详情界面](http://ofcf9jxzt.bkt.clouddn.com/ssdb/p2.png)

 