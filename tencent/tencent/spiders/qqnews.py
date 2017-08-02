# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from tencent.items import TencentItem
from datetime import datetime
import chardet


class qqnews(scrapy.Spider):
    name = "qqnews"  # 爬虫名字
    allowed_domains = ["qq.com"]  # 域名限制
    download_delay = 1
    start_urls = []
    rules = (
        Rule(LinkExtractor(allow=r"http://news.qq.com/a/20170801/\d+\.htm"),
             # 这里需根据具体年份考虑 /14/是指年份 /08\d+/ 是指月份 这个可参考一个网易新闻的地址：http://tech.163.com/16/1119/09/C67P02V400097U81.html 
             callback="parse", follow=True)
    )
    baseurl = 'http://news.qq.com/a/20170801/'
    add = '031607'
    url = baseurl+add+'.htm'
    #print(url)
    start_urls.append(url)
    def parse(self, response):
        qqnews = TencentItem()
        #print(response.url)
        try:
            qqnews['url'] = response.url#url地址
            qqnews['title'] = response.xpath('//html/head/title/text()').extract()#标题
            #时间中的秒数为整数
            qqnews['date'] = str(datetime.now().replace(microsecond=0))#抓取时间
            charset = chardet.detect(response.body)#网页编码
            qqnews['charset'] = charset['encoding']
            yield qqnews
        except:
            pass
        n = response.url.strip().split('/')[-1][:-4]
        #print(n)
        for site in Selector(response).xpath('//div[@class="bd"]/ul[@bosszone="jhRE"]'):
            #qqnews['url'] = site.xpath('.//li/a/@href').extract()
            #qqnews['title'] = site.xpath('.//span[@class="txt"]/text()').extract()
            #yield qqnews
            for url in response.selector.xpath("//a/@href").re(r'^http://news.qq.*'):
                yield scrapy.Request(url, callback=self.parse)
