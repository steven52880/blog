---
title: ZeroTier组网和自建Planet
description: 使用自建Planet加速组网，解决Windows下的重连过慢问题
date: 2023-11-30
lastmod: 2023-11-30
categories:
  - HomeLab
tags:
  - ZeroTier
  - Openwrt
  - NAT
  - 网络

---
## 原理

### NAT类型

NAT中文名为网络地址转换，简单来说就是传输层上路由器在LAN上的局域网IP和WAN上的对外IP进行转换。转换时会根据连接信息（源ip，源端口，目标ip，目标端口）查表来确定网络数据包属于哪一个连接。

根据转发数据包时查的表项不同，分为

- NAT0, OpenInternet, 没有经过NAT，使用公网IP
- NAT1, FullCone Nat, 全锥体 NAT
- NAT2, Address-Restricted Cone NAT, 地址限制型 NAT
- NAT3, Port-Restricted Cone NAT, 端口限制型 NAT
- NAT4, Symmetric NAT, 对称型 NAT

具体原理参考：[https://blog.kaaass.net/archives/1587](https://blog.kaaass.net/archives/1587)

现在家宽路由器PPPoE拨号，拿到的一般就是NAT1。

NAT类型越开放，P2P穿透就越容易成功。FullCone Nat的设备可以和任何其它设备成功建立连接。

可以通过STUN服务器测试自己网络的NAT类型。程序：[https://github.com/HMBSbige/NatTypeTester](https://github.com/HMBSbige/NatTypeTester)

### ZeroTier的P2P

ZeroTier客户端首先和官方维护的根服务器通信，

根服务器协调多个客户端，客户端之间基于UDP尝试通过NAT穿透建立P2P连接。如果能建立P2P连接，后续的通信将不经过中转服务器，否则客户端之间的流量将通过境外的中转服务器中转。

由于官方的根服务器在境外并不是很稳定，所以我选择自建Planet以加速建立P2P连接的过程。

## 搭建Planet

> 摘抄自：[https://github.com/Jonnyan404/zerotier-planet/issues/11](https://github.com/Jonnyan404/zerotier-planet/issues/11)
>
> -----
>
> 1. planet：核心角色，官方不允许自建私有，zerotier的行星服务器，用于管理全球所有的zerotier客户端的地址信息，帮助建立客户端间的**直接链接**，以及在无法建立**直接链接**时，作为中继服务器转发设备间的流量
> 2. controller：控制器，官方允许自建私有(不包含ui，可由用户自行实现，各接口使用json交互)，客户端的管理者，负责管理各个客户端间的配置信息
> 3. moon：官方允许自建私有，作为离客户端更近的中继服务器存在，可以使转发的效率更高
>
> -----
>
> 使用作者的docker, 最终中心节点显示为leaf, 测试移动4g和电信宽带延迟为500ms, 到中心节点分别为120ms和40ms, 实际没有走自定义的节点.
> **经过研究, 需要再进行设置**. 提供下思路, 如下:
>
> 1. compose需要增加ports: '9993:9993'和'9993:9993/udp', 服务器和防火墙也得放行
> 2. 进入容器, 生成moon.json
> 3. 拷贝moon.json到宿主机, 修改stableEndpoints
> 4. 在宿主机用[mkmoonworld-x86](https://github.com/kaaass/ZeroTierOne/releases/download/mkmoonworld-1.0/mkmoonworld-x86)生成行星文件
> 5. 把修改后的moon.json拷回容器, 在容器内生成moon文件, 创建moons.d文件夹, 放进去. 拷贝一份到宿主机备用
> 6. 把行星文件替换回容器
> 7. 重启容器
> 8. 把客户端的planet文件替换
> 9. 安卓端的话, 实测单独加载planet不生效. 加载moon文件, 关闭官方行星节点, 生效
>
> 具体参考 https://github.com/xubiaolin/docker-zerotier-planet 里面的代码实现和各种生成moon教程
>
> \######## 仅供参考 #########
>
> 1. 下载
>
>    ```
>    git clone https://github.com/Jonnyan404/zerotier-planet
>    cd zerotier-planet
>    vim docker-compose.yml
>    ```
>
> 2. 修改
>
>    ```
>    version: '2.0'
>    services:
>        ztncui:
>            container_name: ztncui
>            restart: always
>            environment:
>                - MYADDR=127.0.0.1  # 改成自己的服务器公网ip
>                - HTTP_PORT=3443
>                - HTTP_ALL_INTERFACES=yes
>                - ZTNCUI_PASSWD=root
>            ports:
>                - '3443:3443'  # 设置网页的端口
>                - '9993:9993'  # 作为中心节点，提供9993端口给客户端用，一般是9993
>                - '9993:9993/udp'
>            volumes:
>                - './zerotier-one:/var/lib/zerotier-one'
>                - './ztncui/etc:/opt/key-networks/ztncui/etc'
>                # 按实际路径挂载卷， 冒号前面是宿主机的， 支持相对路径
>            image: keynetworks/ztncui
>    ```
>
> 3. 运行
>
>    ```
>    docker-compose up -d
>    
>    docker images #　查看镜像
>    docker container ps -a # 查看容器
>    
>    docker exec -it ztncui bash # 进入容器
>    # 在容器内操作
>    cd /var/lib/zerotier-one
>    ls -l
>    # 生成moon配置文件
>    zerotier-idtool initmoon identity.public > moon.json
>    chmod 777 moon.json
>    ```
>
> 4. 新建一个terminal, 在**容器外**修改`moon.json`, 位置对应挂载位置
>
>    修改`stableEndpoints`, 注意格式和实际公网ip
>
>    ```
>    {
>     "id": "b72b5e9e1a",
>     "objtype": "world",
>     "roots": [
>      {
>       "identity": "b72b5e9e1a:0:a892e51d2ef94ef941e4c499af01fbc2903f7ad2fd53e9370f9ac6260c2f5d2484fd90756bec0c410675a81b7cf61d2bb885783bd6a8c28bce83bcab5f03fe14",
>       "stableEndpoints": ["127.0.0.1/9993"]
>      }
>     ],
>     "signingKey": "45f0613e569a0549c74293c39b30495b594a003534290e8ade9ef82877aa7505d7a73eeabfc22c97c404e4caaf9f3c9eed2b134d696935c966e28f523364f15f",
>     "signingKey_SECRET": "cc6afd67e7b7f84a92e2c8d3c2e7212c71e2ad0a4f5b3c03bf60ab1cd3b99281b57d9a2958d2bd8fc2bc77fdf2a1160099c2c61d3d9acc8cb311673ee120b4a6",
>     "updatesMustBeSignedBy": "45f0613e569a0549c74293c39b30495b594a003534290e8ade9ef82877aa7505d7a73eeabfc22c97c404e4caaf9f3c9eed2b134d696935c966e28f523364f15f",
>     "worldType": "moon"
>    }
>    ```
>
> 5. 在**容器内**生成moon文件
>
>    ```
>    zerotier-idtool genmoon moon.json
>    mkdir moons.d
>    cp *.moon moons.d/
>    ```
>
> 6. 在**容器外**生成planet文件
>
>    - 拷贝一份moon文件， 客户端可以用到
>
>    - 下载[mkmoonworld](https://github.com/kaaass/ZeroTierOne/releases/tag/mkmoonworld-1.0), 拷贝moon.json， 放在一个目录下
>
>    - ```
>      ./mkmoonworld-x86_64 ./moon.json
>      mv world.bin planet
>      ```
>
>    - ```
>      # 复制到容器内
>      docker cp ./planet ztncui:/var/lib/zerotier-one
>      ```
>
> 7. 重启容器
>
>    ```
>    docker restart ztncui
>    docker exec -it ztncui bash # 进入容器
>    # 在容器内操作
>    cd /var/lib/zerotier-one
>    #　查看ｍoon
>    zerotier-cli listmoons
>    ```
>
> 8. 访问`ip+端口`对应的设置页面
>
> 9. 替换客户端的planet文件并重启服务， 再加入网络， 在网页端授权

## 配置设备

如果设备要用自建的planet，需要把前一个步骤生成的planet文件覆盖设备上原有的官方planet文件。

配置文件路径：

- Windows: `C:\ProgramData\ZeroTier\One\`
- macOS: `/Library/Application Support/ZeroTier/One/`
- Linux: `/var/lib/zerotier-one/`
- FreeBSD/OpenBSD: `/var/db/zerotier-one/`

安卓端需要使用ZeroTier-Fix才能: https://github.com/kaaass/ZerotierFix

## Openwrt主路由配置

在主路由上安装ZeroTier，可以让局域网下所有设备都加入网络，非常方便。

> ZeroTier在Openwrt固件的配置路径
>
> - 配置目录: `/etc/config/zero/`
> - 配置文件：`/etc/config/zerotier`

对于硬路由，可以用Lede源码自编译包含ZeroTier的固件刷入，可以在LUCI Web界面上直接配置

对于软路由，可以用官方编译的镜像，然后用opkg安装，手动调整配置文件

网上有很多教程，这里暂时不详细描述。大概是安装zerotier-one，覆盖planet文件，配置加入网络，新建接口，配置接口防火墙这几步

记得配置防火墙允许`9993`端口的入站连接

Update:

需要注意，Lede固件的配置目录如上所属，官方OP固件则需要在配置文件中添加以下内容以指定ZeroTier配置目录

```
option config_path '/etc/config/zero'
```

参考链接：[https://openwrt.org/docs/guide-user/services/vpn/zerotier](https://openwrt.org/docs/guide-user/services/vpn/zerotier)

## Windows端自动重连

ZeroTier原版客户端在切换网络环境后并不能快速的重新建立连接，必须要等待很长时间才能连通。我选择使用计划任务程序在Windows系统切换WiFi后自动重启ZeroTier服务。

1. 创建计划任务

2. 常规

   - [x] 使用最高权限运行

3. 添加触发器

   - 开始任务：`发生事件时`
   - 日志：`Microsoft-Windows-WLAN-AutoConfig/Operational`
   - 源：`WLAN-AutoConfig`
   - 事件ID：`8001`

   > 可以在事件查看器中看到，`8001`事件表示成功连接到无线网络

4. 添加操作

   - 运行任务：`cmd /c "@sc stop ZeroTierOneService&@sc start ZeroTierOneService"`

5. 设置

   - 如果此任务已经运行，以下规则适用：`对新实例排队`

经过设置，在切换WiFi后系统会自动重启ZeroTier服务，大约5s就可以重新再建立连接了。