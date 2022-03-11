# bushu 用户手册

> 本文介绍 [微信刷步数(bushu)](https://github.com/ZHJ0125/bushu) 项目的使用方法。

此文档面向普通用户，如果您是开发者，请移步至[开发手册](./DevManual.md)。

顾名思义，本项目就是来帮助你躺着刷步数的。经测试，目前可以同步修改步数至微信运动和支付宝运动。

## 如何刷步数

本项目使用华米(小米)运动的API接口，实现步数同步。因此，在开始刷步数前，请先注册华米(小米)账号。

### 注册账号

您可以通过以下方式注册账号：

* 小米官网 - [https://www.mi.com/index.html](https://www.mi.com/index.html)
* 小米运动APP - [Apple Store](https://apps.apple.com/cn/app/%E5%B0%8F%E7%B1%B3%E8%BF%90%E5%8A%A8/id938688461) / [Mi Store](https://app.mi.com/details?id=com.xiaomi.hm.health)

如果注册账号出现问题，可参考[此教程](https://support.qq.com/products/151375/blog/12133)自行解决。

### 开刷

* 打开本项目网页：[https://zhj-bushu.herokuapp.com](https://zhj-bushu.herokuapp.com/)
* 依次输入`小米账号`、`密码`和要刷到的`步数`（***步数要小于4万***）
* 点击 `提交` 按钮即可（刷步数成功或失败都会有提示）

> 请不要频繁刷步数，若过于频繁地刷步数，有可能导致您的账号被封。

## Q&A

### 密码泄露？

您可能担心您的用户名或密码被泄露，不会的，请不必担心。

本项目中，刷步数的核心代码源自 [方块君](https://github.com/577fkj) 大佬的 [mimotion](https://github.com/577fkj/mimotion) 项目，在该项目中，仅涉及了对华米官方提供API接口的POST请求，没有任何数据的存储过程。

同时，在本项目中，也不涉及用户密码的存储操作。对此，您可以检查本项目的[源代码](https://github.com/ZHJ0125/bushu)。

如果您仍然担心密码泄露，您可以单独注册一个用于刷步数的华米(小米)账号，只用来刷步数。

### 会被封号？

大家可能会有疑问：刷步数会不会导致我的账号被封？如果您过于频繁地刷步数，我觉得会被封！

是这样的，由于华米官方API的请求数据中，需要包括地理位置、步数、运动时间、设备ID等多种类型的数据，而在 [mimotion](https://github.com/577fkj/mimotion) 项目中，会伪造一些地理位置数据，将其打包发送至API接口。

因此，有可能官方API接口会检测到**过于频繁的重复数据**，导致您的账号被封。

所以，***请尽量不要再短时间内频繁使用该接口***。

### 为什么做这个项目？

闲着没事做着玩的😂

前几天在 Telegram 的 [Shadowrocket](https://t.me/ShadowrocketApp) 官方群，有个大佬发了一个刷步数的iOS快捷指令，我试了试，居然真的可以刷步数，当时挺惊喜的。

后来搜了一下，原来网上有好多刷步数的教程、网站，比较出名的比如 [https://bushu.wang/](https://bushu.wang/)，以及这个[快捷指令](https://www.icloud.com/shortcuts/a759d3db3f9b4d24a318a343400f7b54)。总之，网上已经有很多类似项目了。

后来我在GitHub上找到了 [方块君](https://github.com/577fkj) 大佬的 [mimotion](https://github.com/577fkj/mimotion) 项目，这个项目使用python写的，只写了核心的请求代码，没有图形化界面。对比一下 [https://bushu.wang/](https://bushu.wang/)，总觉得 mimotion 有些简陋。于是，我开始在网上查找资料，想要为 mimotion 写一个图形(web)界面。

几天后，就有了本项目。

---

## 依赖项目

* [mimotion](https://github.com/577fkj/mimotion) ( Apache License 2.0 ) - 小米运动刷步数
* [Flask](https://github.com/pallets/flask) ( BSD 3-Clause "New" or "Revised" License ) - 用于构建 Web 应用程序的 Python 微框架

## 开源协议

* 本项目使用 [GNU General Public License v3.0](https://github.com/ZHJ0125/bushu/blob/main/LICENSE)  开源许可协议
* Gitee地址：https://gitee.com/zhj0125/bushu
* GitHub地址：https://github.com/ZHJ0125/bushu
