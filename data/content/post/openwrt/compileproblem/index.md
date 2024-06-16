---
title: 解决OpenWRT自编译时卡慢、编译失败等问题
description: 解决因为网络问题造成的OpenWRT编译时下载失败、编译慢等问题，提高编译成功率
date: 2024-06-16
lastmod: 2024-06-16
categories:
  - HomeLab
tags:
  - OpenWRT
---

在执行`make`命令编译OpenWrt的部分插件时需要联网下载文件，并且部分下载过程不遵循系统代理设置。所以在国内这样网络环境糟糕的地方就很容易造成编译失败。

以下的设置，可以很大程度上解决编译失败、编译慢的问题，提高编译成功率



首先必须要确认已经安装了所有的依赖！根据项目readme的提示，执行`apt update`和`apt install`

更换网络环境是最好的办法，几乎可以解决所有问题

- 租用网络环境好的VPS进行编译
- 使用透明代理，比如在路由器上安装“网络加速软件”

设置代理选项

- 设置系统代理选项

  ```shell
  export http_proxy=http://192.168.0.x:7890
  export https_proxy=http://192.168.0.x:7890
  ```

- 设置git代理选项

  ```shell
  git config --global http.proxy http://192.168.0.x:7890
  git config --global https.proxy http://192.168.0.x:7890
  ```

- 使用`proxychains`进行编译

  ```shell
  # install
  apt install proxychains
  
  # config (/etc/proxychains.conf)
  nano /etc/proxychains.conf
  
  socks5 192.168.0.x 7890
  
  # run progran
  proxychains <command>
  ```

编译时可以尝试的操作

- 先执行`make download`进行单线程下载，再`make -j12`进行多线程编译
- 使用`make V=s`显示编译详情，查看卡死的位置
- 遇到网络卡顿，尝试使用代理软件上的“Close All Connections”按钮

