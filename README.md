# robot4mc
Automatic robot to order dinner on mei_can 



公司使用美餐网的点餐平台供应工作餐，但是由于工作忙开会等原因，经常要饿肚子。
研究下美餐的点餐规律，因此开发了一个小小的点餐自动化工具，也造福身边饿肚子的小伙伴。



v1 selenium 实现：由于变更维护的原因，目前已经停止维护

v2 requests实现：使用美餐的接口进行点餐，避免美餐UI维护，导致功能无法实现。



------

总体功能介绍：

mian.py  负责加载plan已经初始化当日的列表

meican_action.py 负责根据plan生成对应的点餐计划，支持全局随机，指定菜单随机，以及跳过某日点餐

getalllists.py 主要负责和美餐网的交互，调用各种接口，进行实际的操作



提供点餐调试模式及命令行功能：

python getalllists.py -h

usage: getalllists.py [-h] [-c] [-o ORDER] [-d] username

meican order cmd line ...

positional arguments:
  username              meican username

optional arguments:

-h, --help            show this help message and exit

-c, --check           meican order check

-o ORDER, --order ORDER
                        meican order dinner

-d, --delete          meican order del



