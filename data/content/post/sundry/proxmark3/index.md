---
title: PM3使用记录
description: Proxmark3 救砖、刷固件、自编译离线嗅探固件、自动嗅探密钥
date: 2024-09-25
categories:
  - 折腾
---
> 某日刷闲鱼的时候发现一个60包邮的砖掉的PM3，打算捡回来玩玩。在手上吃灰了一年之后开始折腾，先尝试使用树莓派烧写固件但是失败了，后面成功用JLink刷写固件。
>
> 以下大量引用网上的博客，别人已经写的很好了。无法访问的链接可以尝试使用网页时光机：https://archive.org/

### 关于Proxmark 3

什么是PM3？它有什么功能？市面上的硬件有什么版本？

- https://firefox2100.github.io/proxmark3/2020/10/12/Proxmark3/
- https://www.wasyoung.com/2019/11/30/337/

### 客户端和固件刷写

注意！预编译的固件较大，仅适配Flash容量为512kB的MCU。如果你是MCU是256kB的版本，将无法刷写预编译的固件。

- 刷写教程： https://github.com/Proxmark/proxmark3/wiki/Flashing/
- 固件下载： https://www.proxmarkbuilds.org/
- 关于Flash容量的说明： https://github.com/RfidResearchGroup/proxmark3/blob/master/doc/md/Use_of_Proxmark/4_Advanced-compilation-parameters.md#256kb-versions

### 救砖

需要准备一个JLink，出门左转淘宝购入。使用镊子短接54和55引脚，然后上电，使用JFlash刷写固件就好

按照这些文档去做就好

- https://pm3.echo.cool/index.php/2020/04/22/jlink%E5%88%B7%E5%86%99proxmark3%E5%9B%BA%E4%BB%B6/
- https://github.com/RfidResearchGroup/proxmark3/blob/master/doc/jtag_notes.md
- https://goatpr0n.farm/2019/09/initial-flashing/debricking-the-proxmark-v3-easy-w/-bus-pirate/
- https://forum.dangerousthings.com/t/how-to-unbrick-a-pm3-easy/9058
- https://shawinnes.com/unbricking-a-proxmark-iii-with-jtag/

### Mifare Classic 常用指令

为了避免自己忘记，列举一下常用的命令和参数。请自行阅读命令提示。

**破解**

```
hf mf fchk {--emu} {-k <HEX>}
hf mf autopwn {--ns} {-k <HEX>}
```

**读写**

```
hf mf dump {-f <KEYFILE>} {--ns}
hf mf restore
hf mf wipe
hf mf wrbl
```

**模拟**

```
hf mf sim
hf mf eclr
hf mf ekeyprn
hf mf eload
hf mf esave
hf mf eview
```

**在线嗅探** 

```
hf 14a sniff
hf mf list
```

在线嗅探模式下，就算有额外供电也不能拔出USB数据线。

### 编译离线嗅探固件

PM3的固件还是挺小的，折腾了半个钟不到就好了，相对于OpenWRT的编译还是很快的。

**参考链接**

- 在Linux上编译： https://github.com/RfidResearchGroup/proxmark3/blob/master/doc/md/Installation_Instructions/Linux-Installation-Instructions.md

- 配置编译参数： https://github.com/RfidResearchGroup/proxmark3/blob/master/doc/md/Use_of_Proxmark/4_Advanced-compilation-parameters.md#platform_extras

- 独立模式： https://github.com/RfidResearchGroup/proxmark3/wiki/Standalone-mode

- 添加自定义的独立模式： https://github.com/RfidResearchGroup/proxmark3/blob/master/armsrc/Standalone/readme.md

**说明**

- `HF_14ASNIFF`在RDV4上可以将嗅探记录保存在SPI Flash中，PM3 Easy上可以将嗅探记录保存在内存中
- 在`Makefile.platform`中配置`PLATFORM`和`STANDALONE`选项
- 将`fullimage.elf`烧录到PM3中
- 长按PM3上的按钮以进入离线工作模式

### 快速导出嗅探的密钥

我在windows上使用PM3客户端，所以在`pm3.bat`所在的目录下运行以下批处理脚本：

```bat
@echo off
cd "%~dp0client"
call setup.bat
::If you want to force the COM port use the -p parameter, example:
::bash pm3 -p COM3
bash pm3 -c "hf mf list" | grep key
pause
```

