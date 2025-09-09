---
title: 【STM32系列教程】0x01 如何自学
description: 最重要的一集！最棒的STM32的自学资料和自学方法~
slug: STM32-0x01
date: 2024-09-09
lastmod: 2025-09-10
categories:
  - STM32系列教程
tags:
  - STM32
---
### 关于怎么搜索

**抛弃百度，善用谷歌**

互联网上的中文计算机资源和英文资源比起来差的十万八千里。可以说中文计算机资源生态就是依托答辩。CSDN上大量从不明来源复制粘贴的低质量博客、各种采集站/反代站在搜索引擎的权重反而还高。所以，抛弃百度吧。

**英文互联网上有着大量的优质内容**，包括各种教程+各种论坛里的反馈帖子，大概率能找到想要的内容。

我们实验室的wifi已经内置了魔法上网功能，宿舍上谷歌需要自备魔法上网工具。

### 前置知识

嵌入式开发属于较为底层、接近硬件电路的一种计算机开发，所以了解一些硬件电路知识和计算机结构知识对于学习STM32有很大的帮助。

UIC在大二开设了Computer Organization的课程，其中有较为相关的内容，但是学习的不深。

你可以选择自学网络上非常出名的*CMU CS15213: CSAPP*课程。它的难度较大，但是可以很好的帮助你理解计算机系统。

### 关于STM32的自学资料

STM32有多种开发方式，我们使用STM32Cube和HAL库开发，网上找资料时需要<u>注意教程是用什么方式开发的</u>。

手册不是用来通读的，是在用到对应内容的时候用来查阅的。比如STM32F4HAL库手册，我通常会先阅读`HAL xxxxx Generic Driver`中`xxxxx Firmware driver API description`的`How to use this driver`部分，然后再去浏览部分会用到的接口函数。这样能较大的提高效率。

以下是最推荐的嵌入式自学资料，希望大家自学时能时常翻阅官方手册

- STM32 官方教程（初级入门教程）
  https://wiki.stmicroelectronics.cn/stm32mcu/wiki/Category:Getting_started_with_STM32_system_peripherals
- RM0090 STM32F4 芯片手册（重点看芯片和外设的架构图，有中文版）
  https://www.st.com/resource/en/reference_manual/dm00031020-stm32f405-415-stm32f407-417-stm32f427-437-and-stm32f429-439-advanced-arm-based-32-bit-mcus-stmicroelectronics.pdf
- UM1725 STM32F4 HAL库手册（重点看HAL库使用方法和API参考）
  https://www.st.com/resource/en/user_manual/um1725-description-of-stm32f4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
- B站江协科技教程（重点看原理解释，原理讲的很清楚，特别是他自己总结的结构框图；不用看代码）
  https://www.bilibili.com/video/BV1th411z7sn/

以下是其它的自学资料

- Digikey的STM32入门教程，包括视频和文档但不是很全
  https://www.youtube.com/playlist?list=PL3bNyZYHcRSU0dQwTXOE5xWLeKfyh1ktT
- DeepBlue的STM32入门教程
  https://deepbluembedded.com/stm32-arm-programming-tutorials/
- B站中科大RM教程（有人推荐，没有看过）
  https://search.bilibili.com/all?keyword=%E4%B8%AD%E7%A7%91%E5%A4%A7%20rm
- B站华工RM教程（有人推荐，没有看过）
  https://space.bilibili.com/352976834

你可以在以下地方寻找教程

- [B站](https://bilibili.com)
- [Google](https://google.com)
- [Youtube](https://youtube.com)

### 如何通过网络获取想要的知识

[【RM论坛】线上取经指南](https://bbs.robomaster.com/article/810113)

[【RM论坛】提问的（RM版本）](https://bbs.robomaster.com/article/810096)  
原文链接：[How to Ask Questions The Smart Way （zh_CN）](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md)

**请务必阅读**！

简单概括一下，

- 提问之前：
    - 仔细读一读**官方文档**，检查教程是否遗漏步骤，看看FAQ有没有你遇到的问题
    - **谷歌**搜索，**多看论坛里的帖子**，别人大概率也遇到过同样问题
    - 不要提出[不该问的问题](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md#%E4%B8%8D%E8%AF%A5%E9%97%AE%E7%9A%84%E9%97%AE%E9%A2%98)
- 提问的时候
    - 描述**运行环境**（硬件配置、操作系统、软件版本号）
    - 描述**所做的操作**，最好是能复现问题的操作
    - 描述诊断测试/**诊断步骤**
    - 描述提问前是如何去研究和理解这个问题的。
    - 提供报错信息和**log**

### 关于ChatGPT

注册和使用需要非大陆+非港澳的手机号+ip地址

u1s1这玩意真挺不错，能解决一些模糊搜索的问题/总结内容帮助快速理解知识点，但是对于稍微复杂点的概念经常性出现描述错误。建议反复提问或用谷歌查证一下。