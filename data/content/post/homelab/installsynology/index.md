---
title: 在PVE上安装群晖
description: 记录一下在PVE服务器上折腾群晖的过程
date: 2023-10-03
lastmod: 2023-10-03
categories:
  - HomeLab
tags:
  - PVE
  - NAS

---
### 引导盘

一些概念

- 在自己的机子上安装群晖系统，需要一个安装了引导工具的引导盘。
- 引导盘运行时不会修改，仅用来引导群晖系统启动，不存放群晖系统
- 一般在Release页面提供写入u盘/硬盘的的img磁盘文件和vmware虚拟机用的vmdk文件
- ARPL有图形化界面修改设置/注入驱动，省去手动改配置文件的步骤
- 下面有几个版本的引导工具：
  - ARPL原版（作者已弃坑）
    https://github.com/fbelavenuto/arpl
  - ARPL汉化版
    https://github.com/wjz304/arpl-zh_CN
  - ARPL汉化修改版（最新）
    https://github.com/wjz304/arpl-i18n
  - Tinycore-Redpill另一个引导器
    https://github.com/pocopico/tinycore-redpill

步骤

1. 这里我选择使用"ARPL汉化修改版（最新）"，`wjz304/arpl-i18n`

2. 在其github的release页面下载`arpl-i18n-xx.x.x.img.zip`并解压
3. 如果在实体机安装，需要把这个`.img`文件写入U盘/硬盘。我选择在pve中安装，所以需要在pve中将其转换为磁盘文件，相当于写入硬盘了。

### 洗白

黑裙有很多功能没法使用，比如HEVC文件无预览图

如果要洗白，需要搞到一套对应机型真实的SN和MAC。

> 淘宝有SN卖，也可以网上找拍照拍到露出来SN和MAC的
>
> DS918+的机型有算号器可以用，所以后面安装的过程中机器型号我选择DS918+。

### 新建机器

在左侧边栏右键"`pve`"，新建虚拟机

- OS页

  - 选择"Do not use any media"

- System页

  - Machine: q35
  - SCSI Controller: VirtIO SCSI single

- Disks页

  - 如果能删除磁盘，可以现在就删掉

- CPU页

  - Sockets: 1
  - Cores: 视自己的硬件情况给

- Memory页

  - Memory: 视自己的硬件情况给，仅作文件服务2G已经够了

- Network页

  - Bridge: 我使用默认的vmbr0

    > 我的选项相当于实体机的网口接了虚拟的傻交换机，虚拟机接在交换机上，和实体机在同一层网络中

  - MAC address: 如果要洗白，填入拿到的MAC地址

- 点击完成

### 导入引导盘

1. 删除多余的硬件

   1. 左侧边栏中打开新建的群晖虚拟机，再打开"`Hardware`"页面
   2. 如果还有剩余的虚拟光驱，把所有的都删除
   3. 如果还有剩余的硬盘，把所有的都删除

2. 上传引导磁盘

   1. 在左侧边栏选择"`local(pve)`"
   2. 在"`ISO Images`"处上传引导磁盘文件`arpl-i18n-xx.x.x.img`
   3. pve会将其储存在`/var/lib/vz/template/iso`路径下
   4. 日志中也会有详细路径

3. 转换并添加引导磁盘

   1. 在左侧边栏选择节点"`pve`"，在"`Shell`"处运行命令

      ```
      qm importdisk <虚拟机id> <引导磁盘img文件路径> local-lvm
      ```

   2. 在左侧边栏找到群晖虚拟机，编辑刚刚导入的"`Unused Disk 0`"

   3. Bus/Device选择Sata，确定

4. 添加自己的磁盘

   1. 我的实体机上安装了一块nvme固态作为实体机系统盘，我想在上面虚拟一块小的磁盘作为群晖的系统盘。所以我又添加了一块Sata磁盘，并且勾选了`SSD emulation`.

5. 修改引导

   1. 打开"`Options`"页面，编辑"`Boot Order`"
   2. 确保只勾选了刚刚创建的引导盘，在我这里它是`sata0`并且`size=1G`

### 编译引导

1. 转到"`Console`"页面（vnc远程连接），开机
2. 选择启动选项的"`Configure Loader`"（默认就是），稍等其启动
3. 打开配置菜单
   - 页面上提示：`Access http://192.168.x.xxx:7681 to configure the loader`。通过浏览器访问这个链接可以打开菜单。
   - 页面上提示：`Call menu.sh to configure loader`。直接在屏幕上输入脚本名运行脚本也能打开菜单。
4. 进行配置
   1. Choose a language
      - 先调成中文`zh_CN`
   2. Choose a model / 选择型号
      - 选择机型，每个型号的功能都有些许不同，可以上网查
      - 这里我选择`DS918+`，因为洗白序列号比较好搞到
      - 如果列表中没有想要的机型，可以选择`Disable flags restriction`和`Show beta models`
   3. Choose a build number / 选择版本
      - 这里我选择了最新的版本
   4. Cmdline menu/ 设置Cmdline
      - 如果需要洗白，选择"`自定义SN`"和"`自定义MAC`"并填入
      - 如果之前在虚拟机设置中填入了MAC，这里可以不填
   5. Build the loader / 编译引导
      - 确保网络良好，脚本会自动从群晖官网下载基础引导文件
   6. 启动

### 安装系统

1. 在上面的菜单中选择启动，或者重启虚拟机后，会进入启动群晖系统过程。
2. 稍等其启动完成，出现提示"`在浏览器中访问https://192.168.x.xxx:5000`链接DSM"，根据提示在浏览器中打开链接，打不开就再等会
3. 根据步骤安装即可，注意几点：
   1. 关闭自动更新，选择手动更新
   2. 因为是黑群晖，所以跳过登录群晖账号