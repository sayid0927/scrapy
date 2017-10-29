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
        Rule(LinkExtractor(allow=r'htm_data/\d+/\d+/\d+.html'), callback='parse_item'),
    )

    def parse_item(self, response):
        print('respone.utl===>>>' + response.url)
        item = MyprojectItem()
        item['title'] = response.xpath('//tr[@class="tr1 do_not_catch"]//h4/text()').extract()[0]
        print('item>> title===>>>' + item['title'])
        content_list = response.xpath('//div[@class="tpc_content do_not_catch"]/text()|//span[@class="f16"]').extract()
        content = ''.join(content_list)
        item['content'] = content.replace('<p>', "").replace('</p>', "").replace('<br>', "\n").replace("1024", "").replace(
            '<span class="f16"><span style="display:inline-block;color:green">', "")
        #        item['content']=content
        item['url'] = response.url
        yield item
