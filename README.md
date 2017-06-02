# 微信图片转自定义表情机器人-qiqi-7

### 简介

微信中的表情包重度用户们经常从微信推文或微博等SNS软件中以图片的格式保存表情包，然而微信斗图这种严肃活动，发图片表情显得不够专业。还好，微信图片转自定义表情机器人解决了这个问题，自动将图片转为自定义表情方便添加，让用户在这场没有硝烟的战争中占据优势。

### 依赖

本机器人基于Python3开发

* 微信个人号API

	[wxpy](https://github.com/youfou/wxpy)

* PIL

* os

### 原理

wxpy使用web版微信的接口，通过wxpy获取用户发送的消息。
微信会将图片以png发送，自定义表情以gif格式发送。
该机器人的工作主要是将png图片转换成gif图片回复，并在图片过大时进行压缩。

### 相关项目
[微信个人斗图机器人—奇奇七号](https://vinci7.github.io/qiqi-7/)

[斗图啦微信机器人](https://www.doutula.com/faq)

[腾讯优图 · 开放平台](http://open.youtu.qq.com/welcome/index)





