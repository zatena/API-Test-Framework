接口自动化框架说明
=====

本接口测试框架服务于基于http请求的接口请求
---------

# 环境准备

`Python3`以上版本

$ pip3 install -r requirements.txt

# 当前服务对象
特赞大平台业务

# git 构建地址 <br>
[仓库地址](git clone git@git.tezign.com:Tester/API-Test-Framework.git "git clone git@git.tezign.com:Tester/API-Test-Framework.git")


# git shell command <br>
whoami <br>
pwd <br>
virtualenv -p /usr/bin/python3 venv <br>
source venv/bin/activate <br>
pip3 install -r requirements.txt <br>
python3 run.py <br>

## 接口用例开发注意事项：<br>
### 数据依赖两种格式
#### 第一种 预期结果判断，在本用例响应结果中判断
项目完结.1.projectStatus:8 <br>
* 1 获取的projectStatus实际位置顺序 <br>
* 8 预期结果 <br>

#### 第二种 用例应用，在其他用例的返回结果中取值，用到本用例
* 以下数值为该数据在响应结果里的实际位置 <br>

数据依赖存在于请求地址中表现为：<br>
"caseUrl": "/withdraw/getProjectTradingRecord?withdrawId=获取提现记录表.1.id"<br>
数据依赖存在于请求参数中表现为：<br>
 "body": { <br>
 "proProjectIds": ["设计师查看确认函.1.projectId"], <br>
 "projectIds": [], <br>
 "withdrawId": "获取提现记录表.1.id" <br>
} <br>

主要方法说明
------

#### 1. run.py
执行入口：执行所有以tezign**开始的json文件

#### 2. util/common.py
通用方法：执行用例，数据处理，解析和生成测试报告的方法

#### 3. core
底层方法

#### 4. model
执行结果处理，存储，生成报告的各类方法

#### 5.constants.py
常量方法：如测试数据、地址，邮件配置，数据库配置等常量的存储







# Api-Test-Framework
# Disadvantage: number控制，case体量大了以后不好维护；数据依赖基于大量的全局变量，case多了以后，也会变得很麻烦。
