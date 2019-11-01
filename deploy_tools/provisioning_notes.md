配置新网站
========

## 本地需要的工具

fabric==2.5
patchwork==1.0.1

## 服务器要求

Ubuntu==16.0.4

## 服务器需要安装的包:

* nginx
* Python 3
* Git
* pip
* virtualenv

```shell
sudo apt-get install nginx git python3 python3-pip
sudo pip3 install virtualenv
```

## 配置Nginx

* 参考nginx.template.conf
* 把SITENAME替换成所需的域名, 例如staging.my-domain.com

## Systemd任务

* 参考gunicorn-systemd.template.service
* 把SITENAME替换成所需的域名, 例如staging.my-domain.com

## 文件结构

假设有用户账户, HOME目录为`/home/username`

- /home/username
  - sites
    - SITENAME
        - database
        - source
        - static
        - virtualenv

## 最后

一键安装, 在此文件路径下执行:
```shell
$ fab -H user@host deploy
```
