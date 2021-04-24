# ServerStatus
云探针、多服务器探针、云监控、多服务器云监控

基于ServerStatus-Hotaru膜改版的套娃膜改版(实际上本README也是抄它的)。

主要将client改为通过http提交数据,以及将服务端换成了php以便减小部署成本(PHP is the best!)

默认图片素材来源: Pixiv:  86597206 默认背景来源：nisekoi.jp

如需用做商业用途请更换主题图片。

For commercial use, please replace the images.

若本仓库用到的一些素材侵犯了您的版权，请联系我处理，谢谢。

If some of the assets used in this repo infringe your copyright, please contact me, thanks.

## 特性

前端基于Vue 3.0和SemanticUI制作，如需修改前端建议自行修改打包（也可以尝试直接格式化打包后的js/css文件后修改，但是不建议）：

前端开源地址：https://github.com/CokeMine/Hotaru_theme

客户端支持Python版本：Python2.7 - Python3.7

客户端可以选择使用vnStat按月计算流量，会自动编译安装最新版本vnStat。如不使用vnStat，则默认计算流量方式为重启后流量清零。

服务端支持php版本:7.x - 8.x

服务端需要composer 2.x


## 安装方法

Composer:

请查看官网文档:https://getcomposer.org/doc/00-intro.md

服务端：

```bash
git clone https://github.com/shirakun/ServerStatus.git
cd ServerStatus
composer install
cp node.php.template node.php

```

然后将网站目录设置为`ServerStatus/public`即可

客户端：

先通过pip安装requests类库(`pip install requests`),其它参照原版:https://github.com/BotoX/ServerStatus

装好后修改配置文件,`SERVER`的值写完整的服务端api路径(`http://xxx.com/api.php`)

## 修改方法

配置文件：`node.php`

```php
"user" => [
        "name"     => "server name",
        "password" => "passwd",
        "location" => "self home",
        "type"     => "VDS",
        "host"     => "No",
        "disabled" => false,
        "region"   => "jp",
    ],
```

这里的key(`"user"`)对应客户端中`USER`的值相当于原版的username的作用

## 效果演示

![RktuH.png](https://img.ams1.imgbed.xyz/2021/02/04/1nfJF.png)

## 相关开源项目 ： 
* ServerStatus-Hotaru：https://github.com/CokeMine/ServerStatus-Hotaru
* ServerStatus-Toyo：https://github.com/ToyoDAdoubiBackup/ServerStatus-Toyo
* ServerStatus：https://github.com/BotoX/ServerStatus
* mojeda's ServerStatus: https://github.com/mojeda/ServerStatus
* BlueVM's project: http://www.lowendtalk.com/discussion/comment/169690#Comment_169690