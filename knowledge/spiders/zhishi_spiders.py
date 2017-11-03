# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from knowledge.items import CommonItem
from knowledge.consts import consts


class ZhishiCommonSpider(scrapy.Spider):
    def is_root_url(self, url):
        for item in self.start_urls:
            if item == url or url.find('index_') != -1 or url.find('List_') != -1:
                return True
        return False

    def thn21_parse(self, response):
        is_root = self.is_root_url(response.url)
        if is_root:
            for item in response.xpath('//div[@id="V"]/p'):
                # 过滤一下url，如果已经爬过了，就不爬了
                next_page_url = item.css('a::attr(href)').extract_first()
                if next_page_url is not None:
                    yield scrapy.Request(next_page_url)
        else:
            ci = CommonItem()
            title = response.xpath('//div[@class="ti"]/h2/text()').extract_first()
            title.replace('\r\n', '')
            ci['title'] = title
            content = "".join(response.xpath('//div[@id="V"]/p[position()>1]/text()').extract())
            content = content.replace('上一篇：', '')
            content = content.replace('下一篇：', '')
            content = content.replace('\r\n', '')
            content = content.replace(' ', '')
            content = content.replace('\xa0', '')
            content = content.replace('\u3000', '')
            ci['content'] = content
            ci['url'] = response.url
            ci['desc'] = self.desc
            ci['type'] = self.type
            yield ci

    def jianbihua_parse(self, response):
        # jianbihua 人体知识结果解析
        if self.is_root_url(response.url):
            # zhishi urls
            for item in response.css('.Lists10w_box ul li'):
                # 过滤一下url，如果已经爬过了，就不爬了
                next_page_url = item.css("a::attr(href)").extract_first()
                if next_page_url is not None:
                    yield scrapy.Request(response.urljoin(next_page_url))

            #下一页的数据
            next_page = response.xpath('//div[@class="showpage"]/a[text()="下一页"]/@href').extract_first()
            if next_page is not None:
                yield scrapy.Request(response.urljoin(next_page))
        else:
            desc = response.css('.jieshao10w')
            if desc is not None:
                ci = CommonItem()
                # for item in desc.xpath('//p'):
                ci['title'] = desc.xpath('//p[1]/strong/text()').extract_first()
                content = "".join(desc.xpath('//p[position()>1]/text()').extract())
                content = content.replace('\r\n', '')
                content = content.replace('\xa0', '')
                content = content.replace('\u3000', '')
                ci['content'] = content
                ci['url'] = response.url
                ci['desc'] = self.desc
                ci['type'] = self.type
                yield ci

    def tom61_parse(self, response):
        # tom61 人体知识结果解析
        if self.is_root_url(response.url):
            for item in response.xpath('//dl/dd/a'):
                # 过滤一下url，如果已经爬过了，就不爬了
                next_page_url = item.xpath('@href').extract_first()
                if next_page_url is not None:
                    yield scrapy.Request(response.urljoin(next_page_url))
            #下一页的数据
            next_page = response.xpath('//a[text()="下一页"]/@href').extract_first()
            if next_page is not None:
                yield scrapy.Request(response.urljoin(next_page))
        else:
            desc = response.xpath('//div[@class="t_news"]')
            if desc is not None:
                ci = CommonItem()
                # for item in desc.xpath('//p'):
                ci['title'] = response.xpath('//div[@class="t_news"]/h1/text()').extract_first()
                content = "".join(response.xpath('//div[@class="t_news"]/div/p/text()').extract())
                content = content.replace('\u3000', '')
                content = content.replace('\xa0', '')
                content = content.replace(' ', '')
                content = content.replace('\r\n', '')
                ci['content'] = content
                ci['url'] = response.url
                ci['desc'] = self.desc
                ci['type'] = self.type
                yield ci

    def parse(self, response):
        # 这里要增加return 返回各个解析的生成器结果，因为parse是个生成器
        if response.url.find('thn21') != -1:
            return self.thn21_parse(response)
        elif response.url.find('jianbihua') != -1:
            return self.jianbihua_parse(response)
        elif response.url.find('tom61') != -1:
            return self.tom61_parse(response)

class RentiSpider(ZhishiCommonSpider):
    name = "renti-spider"
    start_urls = [
        'http://www.jianbihua.org/weishime/renti/',
        'http://www.thn21.com/Article/wai/5551_4.html',
        'http://www.tom61.com/shiwangeweishime/qimiaoderenti/',
    ]
    type = consts.RENTI_TYPE
    desc = consts.RENTI_DESC

class ShenghuoSpider(ZhishiCommonSpider):
    name = "shenghuo-spider"
    start_urls = [
        'http://www.jianbihua.org/weishime/shenghuo/',
        'http://www.thn21.com/Article/wai/5551.html',
        'http://www.tom61.com/shiwangeweishime/jiankangdeshenghuo/',
    ]
    type = consts.SHENGHUO_TYPE
    desc = consts.SHENGHUO_DESC

class ChangshiSpider(ZhishiCommonSpider):
    name = "changshi-spider"
    start_urls = [
        'http://www.jianbihua.org/weishime/changshi/',
        'http://www.tom61.com/shiwangeweishime/shenbiandechangshi/',
    ]
    type = consts.CHANGSHI_TYPE
    desc = consts.CHANGSHI_DESC

class DongwuSpider(ZhishiCommonSpider):
    name = "dongwu-spider"
    start_urls = [
        'http://www.jianbihua.org/weishime/dongwu/',
        'http://www.thn21.com/Article/wai/5551_2.html',
        'http://www.tom61.com/shiwangeweishime/keaidedongwu/',
    ]
    type = consts.DONGWU_TYPE
    desc = consts.DONGWU_DESC

class ZhiwuSpider(ZhishiCommonSpider):
    name = "zhiwu-spider"
    start_urls = [
        'http://www.jianbihua.org/weishime/zhiwu/',
        'http://www.tom61.com/shiwangeweishime/youqudezhiwu/',
    ]
    type = consts.ZHIWU_TYPE
    desc = consts.ZHIWU_DESC

class DiqiuSpider(ZhishiCommonSpider):
    name = "diqiu-spider"
    start_urls = [
        'http://www.jianbihua.org/weishime/diqiu/',
        'http://www.tom61.com/shiwangeweishime/meilidediqiu/',
    ]
    type = consts.DIQIU_TYPE
    desc = consts.DIQIU_DESC

class YuzhouSpider(ZhishiCommonSpider):
    name = "yuzhou-spider"
    start_urls = [
        'http://www.jianbihua.org/weishime/yuzhou/',
        'http://www.thn21.com/Article/wai/5551_5.html',
        'http://www.tom61.com/shiwangeweishime/shenmideyuzhou/',
    ]
    type = consts.YUZHOU_TYPE
    desc = consts.YUZHOU_DESC

class KejiSpider(ZhishiCommonSpider):
    name = "keji-spider"
    start_urls = [
        'http://www.jianbihua.org/weishime/keji/',
        'http://www.thn21.com/Article/wai/5551_6.html',
        'http://www.thn21.com/Article/wai/5551_7.html',
        'http://www.tom61.com/shiwangeweishime/shenqidekeji/',
    ]
    type = consts.KEJI_TYPE
    desc = consts.KEJI_DESC

class JunshiSpider(ZhishiCommonSpider):
    name = "junshi-spider"
    start_urls = [
        'http://www.thn21.com/Article/wai/5551_3.html',
        'http://www.tom61.com/shiwangeweishime/junshiyujiaotong/',
    ]
    type = consts.JUNSHI_TYPE
    desc = consts.JUNSHI_DESC

class ShulihuaSpider(ZhishiCommonSpider):
    name = "shulihua-spider"
    start_urls = [
        'http://www.tom61.com/shiwangeweishime/shulihuazhimi/',
    ]
    type = consts.SHULIHUA_TYPE
    desc = consts.SHULIHUA_DESC

class LishiSpider(ZhishiCommonSpider):
    name = "lishi-spider"
    start_urls = [
        'http://www.tom61.com/shiwangeweishime/zhongwailishi/',
    ]
    type = consts.LISHI_TYPE
    desc = consts.LISHI_DESC

class WenhuaSpider(ZhishiCommonSpider):
    name = "wenhua-spider"
    start_urls = [
        'http://www.tom61.com/shiwangeweishime/wenhuayishu/',
    ]
    type = consts.WENHUA_TYPE
    desc = consts.WENHUA_DESC
