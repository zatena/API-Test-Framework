Automation for SOP

This repo try to do api automation for sop by some python libs


Installation and dependence

Need python3 to run the automation scripts, also need some other libs, such as:

$ pip3 install -r requirements.txt


You can run the "run_regression_" scripts, and the report.html will be created automatically


git clone git@git.tezign.com:Tester/API-Test-Framework.git
whoami 
pwd
#切换成虚拟环境并构建依赖
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
# 执行回归测试脚本
python3 run_regression.py


case开发注意事项：
获取新添加人才列表.1.total:2
1是想获取的第几个total
2是实际的结果的索引

