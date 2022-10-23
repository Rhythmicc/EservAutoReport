<h1 style="text-align: center"> EservAutoReport </h1>

！！！免责声明：本项目仅供学习，用作它途发生的一切后果与本项目无关！！！

## 安装

```shell
pip3 install git+https://github.com/Rhythmicc/EservAutoReport.git -U
```

## 使用

```shell
cup-ear --help
```

初次运行会自动引导配置，其中`用户名`和`密码`需要填写统一认证登录账号密码，`区县`可以不填；`email`如果填写，表示启用邮箱通知，你需要正确填写相关配置项。

配置表(`~/.EservAutoReport_config`)样例:

```json
{
  "username": "__学号__",
  "password": "__密码__",
  "province": "北京市",
  "city": "昌平区",
  "district": "", // 区县
  "address": "城北街道东关二条14-2号阳光学生公寓",
  "remote-url": "", // 远程的Selenium服务端，比如 http://1.1.1.1:4444/wd/hub；为空表示使用本机Selenium
  "email": "__你的邮箱__",
  "email_password": "__你的邮箱秘钥__",
  "smtp": "__SMTP服务地址__",
  "to": "__收件地址__"
}
```
