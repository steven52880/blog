---
title: 宁盾令牌(Dkey Token)转换为标准TOTP
description: 多装一个APP真的不太爽
date: 2023-10-09
lastmod: 2023-10-09
categories:
  - 折腾
tags:
  - UIC
---
学校某系统使用宁盾令牌(Dkey Token)进行二步验证，想将其转换为标准TOTP两步验证导入BitWarden中统一管理。

### 关于TOTP

介绍TOTP：

- Time-based One Time Password，时间同步一次性密码。
- 客户端和服务端保存同一个Secret密钥，同时保持正确的时钟
- 每30s/60s基于时间和Secret密钥生成新的口令

关于Secret密钥：

> The length of the shared secret MUST be **at least 128 bits**. This document RECOMMENDs a shared secret length of 160 bits.

> 在TOTP的URL中，`secret`参数包含共享的密钥，这个密钥是一个二进制数据。为了将它包含在URL中并确保URL友好，密钥会经过**Base32编码**。

### 抓包获取参数

在令牌绑定的页面上抓包，可以看到请求`refreshMobileToken`接口，其中部分信息如下：

```json
        "serial": "01****",
        "crypto": 1,
        "timeStep": 60,
        "passwordLength": 6,
        "activationCode": null,
        "model": 4,
        "seed": "to/9v3VzCUPtoNtVIZKnPmYFW0Y=",
```

### 从二维码获取参数

同时解码二维码，得到如下url（关键信息已抹去）：

`https://mtc.ndkey.com/mtc/appDownload/index.html#eyJ2ZXJzaW9uIj****......****NjMxMDAwfX0`

对`#`后面的部分进行base64解码，得到如下json：

```json
{"version":1,"serviceId":"SN1904########","companyName":"########","activationMethod":1,"expireTime":34247########,"token":{"serial":"01****","crypto":1,"seed":"b68ffdbf75730943eda0db552192a73e66055b46","timeStep":60,"passwordLength":6,"expireTime":34247########}}
```

### 计算密钥

对于抓包得到的json请求，其中的`seed`参数看起来像是经过**base64编码的密钥**。对其进行base64解码，得到二进制密钥，再进行base32编码，即可得到totp url中的secret。

对于二维码得到的json，其中的`seed`参数为**16进制表示的二进制密钥**。对其进行hex解码，得到二进制密钥，再进行base32编码，即可得到totp url中的secret。

尝试以上两种方法，得到的secret是相同的

> - 我使用这个网站进行编码/解码：[CyberChef](https://gchq.github.io/CyberChef/)
>
> - 使用这个工具进行base64解码时，需要**取消勾选**`Remove non-alphabet chars`

### 拼接字符串

- `[USERNAME]`：用户名
- `[SECRET]`：base32编码后的密钥，使用上述方法计算
- `[DIGITS]`：密码长度，为得到的参数中的`passwordLength`，我这里是6
- `[PERIOD]`：过期时间，为得到的参数中的`timeStep`，我这里是60

```url
otpauth://totp/[USERNAME]?secret=[SECRET]&algorithm=SHA1&digits=[DIGITS]&period=[PERIOD]
```

### 尝试

我这里拼接得到的字符串最终为：

```url
otpauth://totp/username?secret=W2H73P3VOMEUH3NA3NKSDEVHHZTAKW2G&algorithm=SHA1&digits=6&period=60
```

将其填入BitWarden中，可以正确生成TOTP口令。

