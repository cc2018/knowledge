# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from knowledge.items import CommonItem
from knowledge.consts import consts

class GushiCommonSpider(scrapy.Spider):
    def is_root_url(self, url):
        for item in self.start_urls:
            if url.find(item) != -1:
                return True
        return False

    def gushi365_parse(self, response):
        is_root = self.is_root_url(response.url)
        if is_root:
            try:
                for item in response.xpath('//main[@id="main"]/article//h2/a'):
                    # 过滤一下url，如果已经爬过了，就不爬了
                    next_page_url = item.xpath('@href').extract_first()
                    if next_page_url is not None:
                        yield scrapy.Request(response.urljoin(next_page_url))

                #下一页的数据
                next_page = response.xpath('//span[@class="next"]/a/@href').extract_first()
                if next_page is not None:
                    yield scrapy.Request(response.urljoin(next_page))
            except Exception:
                pass
        else:
            try:
                ci = CommonItem()
                title = response.xpath('//main[@id="main"]/article//h1/text()').extract_first()
                title.replace('\r\n', '')
                ci['title'] = title
                content = "".join(response.xpath('//main[@id="main"]/article//span[@class="STYLE1"]/p/text()').extract())
                content = content.replace('\r\n', '')
                content = content.replace('\n', '')
                content = content.replace(' ', '')
                content = content.replace('\xa0', '')
                content = content.replace('\u3000', '')
                ci['content'] = content
                ci['url'] = response.url
                ci['desc'] = self.desc
                ci['type'] = self.type
                yield ci
            except Exception:
                pass

    def parse(self, response):
        # 这里要增加return 返回各个解析的生成器结果，因为parse是个生成器
        if response.url.find('gushi365') != -1:
            return self.gushi365_parse(response)

class YouerSpider(GushiCommonSpider):
    name = "youer-spider"
    start_urls = [
        'http://www.gushi365.com/youergushi/',
    ]
    type = consts.YOUER_TYPE
    desc = consts.YOUER_DESC

class ErtongSpider(GushiCommonSpider):
    name = "ertong-spider"
    start_urls = [
        'http://www.gushi365.com/xiaogushi/',
    ]
    type = consts.ERTONG_TYPE
    desc = consts.ERTONG_DESC

class ShuiqianSpider(GushiCommonSpider):
    name = "shuiqian-spider"
    start_urls = [
        'http://www.gushi365.com/shuiqiangushi/',
    ]
    type = consts.SHUIQIAN_TYPE
    desc = consts.SHUIQIAN_DESC

class YizhiSpider(GushiCommonSpider):
    name = "yizhi-spider"
    start_urls = [
        'http://www.gushi365.com/yizhigushi/',
    ]
    type = consts.YIZHI_TYPE
    desc = consts.YIZHI_DESC

class YuyanSpider(GushiCommonSpider):
    name = "yuyan-spider"
    start_urls = [
        'http://www.gushi365.com/yuyangushi/',
    ]
    type = consts.YUYAN_TYPE
    desc = consts.YUYAN_DESC

class MinjianSpider(GushiCommonSpider):
    name = "minjian-spider"
    start_urls = [
        'http://www.gushi365.com/minjiangushi/',
    ]
    type = consts.MINJIAN_TYPE
    desc = consts.MINJIAN_DESC
