# 儿童语料
本爬虫纯粹为学习使用

### 启动

```
# 查看所有spider
scrapy list
# 启动其中一个spider
scrapy crawl renti-spider
# sh启动所有spider
sh crawl.sh
```

### spider说明

可在settings.py 里设置一些参数

```
DOWNLOAD_DELAY: 设置同一个网站的延迟时间为1s，避免造成网站压力太大
ITEM_PIPELINES: 持久化中间间，这里提供了文件与mogondb两种方式
DOWNLOADER_MIDDLEWARES: 下载中间件，这里提供随机ua和随机cookie中间件
CONCURRENT_REQUESTS: 并行请求，默认为16
```
针对ip反爬虫，后面可加入免费代理变换ip

### 选择器

这里主要使用scrapy的内嵌xpath选择器，有时也用了css选择器

xpath选择器有几个小技巧：

```
已获取到各个a节点： 可以直接写item.xpath('@href').extract_first()，获取当前a节点的href
节点index：/p[i]/text(), 可以精确获取第几个子元素，还有first()，last(), 甚至通过表达式position()，如/p[position()>1]/text()：获取子节点大于第一个位置的所有p节点
```
