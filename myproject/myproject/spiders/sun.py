# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from myproject.items import MyprojectItem


class SunSpider(CrawlSpider):
    name = 'sun'
    allowed_domains = ['t66y.com']
    start_urls = ['https://t66y.com/thread0806.php?fid=20&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'page=\d+')),
        Rule(LinkExtractor(allow=r'htm_data/\d+/\d+/\d+.html'),callback ='parse_item'),
    )

    def parse_item(self, response):
        item = MyprojectItem()
        item['title'] = response.xpath('//tr[@class="tr1 do_not_catch"]//h4/text()').extract()
        item['content'] = response.xpath('//div[@class="tpc_content do_not_catch"]/text()').extract()
        yield item
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i
