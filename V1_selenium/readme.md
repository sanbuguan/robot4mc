##### 美餐点餐自动化(selenium实现)

使用python + selenium直接对美餐网进行UI操作，进行点餐。由于美餐的UI经常进行维护，因为需要不断的维护和更新代码，**目前此代码已经停止维护！**请参考V2版本。

基本原理：
通过读取config目录下的用户信息及点餐的配置，通过selenium进行点击点餐。由于selenium无法获取到某些元素，辅助用Jquery的方法进行查找。用户登陆操作后使用pickle进行cookie的序列化进行保存，后续登陆直接加载cookie。

启用python flask进行结果的查看和日志浏览。