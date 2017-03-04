# price-watcher
Get the price change of certain products on jd.com and send notify to wechat

这是一个简化版本，不需要数据库，只使用文本文件来存储相关信息。适合关注商品不太多的个人使用者。

使用时需先把 “sckey.example.py” 重命名为 “sckey.py”，然后用编辑器打开，引号内的'example_key'须替换为个人的Server酱SCKEY。

文件“products.txt”中保存自己感兴趣的商品编号及名称，需自己输入。

目录“price”中会自动创建多个TXT文件，名字为各个商品的编号，里面会记录对应商品的价格变化。

说明：
本爬虫只在 Python 3 下测试过，需要提前安装库 BeautifulSoup。