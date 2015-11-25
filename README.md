# 招领服务

## 结构说明

基于web.py构建
>
```
.
├── app.py          入口地址
├── config.py       配置信息
├── controller      页面控制目录
│   ├── __init__.py   		url路由写在此处
│   ├── index.py            首页
│   ├── notify.py           通知
│   ├── phone.py            手机绑定
│   └── weibo.py         
├── lib             模块库
│   ├── __init__.py   
│   ├── cookie.py         cookie操作模块
│   ├── email.py          邮件模块
│   ├── bbs_nku.py        南开BBS模块
│   ├── bbs_tju.py        天大BBS接口模块
│   ├── response.py       特殊格式(json)响应模块
│   ├── sms.py            短信模块
│   ├── user.py           用户信息模块
│   ├── validate.py       验证模块
│   └── yunyin.py         云印接口模块
├── model        数据库model 
│   ├── js		js目录
│   └── css     css目录
├── static      静态文件  
│   ├── js			    js目录
│   └── css     	    css目录
└── templates        模板
    ├── index.html          首页
    └── record.html         记录页
```
>
