# -*- coding: utf-8 -*-
import re
import urllib2

import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from myproject.items import MyprojectItem

from downloader import Downloader

from myproject.spiders.hh import download


class SunSpider(CrawlSpider):
    name = 'sun'
    home_url='http://comic.sfacg.com'
    allowed_domains = ['comic.sfacg.com']
    start_urls = ['http://comic.sfacg.com/Catalog/?tid=2']
    URL = 'http://comic.sfacg.com'
    picture = 'http://coldpic.sfacg.com'

    def parse(self, response):

        manHuan_list = response.xpath('//li[@class="Conjunction"]//@href').extract()
        manHuan_nex_list = response.xpath('//ul[@class="nav pagebar"]/li/a/@href').extract()

        if len(manHuan_nex_list):

            for Nex_Url in manHuan_nex_list:
                yield scrapy.Request(Nex_Url, callback=self.parse)
        else:
            print ('manHuan_nex_list is NULL')

        if len(manHuan_list):
            for Info_Url in manHuan_list:
                yield scrapy.Request(Info_Url, callback=self.manHuan_Info)
        else:
            print ("manHuan_list is NULL")


    def manHuan_Info(self, response):


        manHuna_Book_Name=response.xpath('//td[@class="font_gray gray_link1"]//span/text()').extract()[0]

        manHuna_Book_Type = response.xpath('//ul[@class="Height_px22"]//a/text()').extract()[0]

        manHuna_Book_Auth = response.xpath('//ul[@class="Height_px22"]//a/text()').extract()[1]

        manHuna_Book_profile = response.xpath('//ul[@class="Height_px22"]/li/text()').extract()[4]

        manHuna_Book_title_url = response.xpath('//ul[@class="serialise_list Blue_link2"]//a/@href').extract()

        manHuna_Book_cover_url = response.xpath('//td[@class="comic_cover"]/img/@src').extract()[0]



        if manHuna_Book_Name.strip() == '':
            print 'manHuna_Book_Type is null'
            manHuna_Book_Name= 'null'
        else:
            manHuna_Book_Name= manHuna_Book_Name


        if manHuna_Book_Type.strip() == '':
            print 'manHuna_Book_Type is null'
            manHuna_Book_Type='null'
        else:
            manHuna_Book_Type = manHuna_Book_Type


        if manHuna_Book_Auth.strip() == '':
            print 'manHuna_Book_Auth is null'
            manHuna_Book_Auth = 'null'
        else:
            manHuna_Book_Auth = manHuna_Book_Auth


        if manHuna_Book_profile.strip() == '':
            print 'manHuna_Book_profile is null'
            manHuna_Book_profile='null'
        else:
            manHuna_Book_profile = manHuna_Book_profile


        if manHuna_Book_cover_url.strip() == '':
             print 'manHuna_Book_cover_url is null'
             manHuna_Book_cover_url = 'null'
        else:
            manHuna_Book_cover_url = manHuna_Book_cover_url

        if len(manHuna_Book_title_url):
            for Info_Url in manHuna_Book_title_url:
                title_url= self.home_url+Info_Url
                yield scrapy.Request(title_url,meta={'manHuna_Book_cover_url':manHuna_Book_cover_url,'manHuna_Book_Name':manHuna_Book_Name,'manHuna_Book_Type': manHuna_Book_Type,'manHuna_Book_Auth': manHuna_Book_Auth,'manHuna_Book_profile': manHuna_Book_profile},callback=self.manHuan_Title)
        else:
            print 'manHuna_Book_title_url is null'



    def manHuan_Title(self, response):

        manHuna_Book_Name = response.meta['manHuna_Book_Name']
        manHuna_Book_Type = response.meta['manHuna_Book_Type']
        manHuna_Book_Auth = response.meta['manHuna_Book_Auth']
        manHuna_Book_profile = response.meta['manHuna_Book_profile']
        manHuna_Book_cover_url = response.meta['manHuna_Book_cover_url']

        manHuna_Book_title = response.xpath('//div[@class="wrap"]/span/text()').extract()[0]
        manHuna_Book_img_url = self.get_section_page(response.url)

        if manHuna_Book_title.strip() == '':
            print 'manHuna_Book_title is null'
            manHuna_Book_title = 'null'
        else:
            manHuna_Book_title = manHuna_Book_title

        i = MyprojectItem()

        i['manHuna_Book_Name'] = manHuna_Book_Name
        i['manHuna_Book_Type'] = manHuna_Book_Type
        i['manHuna_Book_Auth'] = manHuna_Book_Auth
        i['manHuna_Book_profile'] = manHuna_Book_profile
        i['manHuna_Book_title'] = manHuna_Book_title
        i['manHuna_Book_img_url'] = manHuna_Book_img_url
        i['manHuna_Book_cover_url'] = manHuna_Book_cover_url

        yield i


    def download(url, user_agent='wswp', num_try=2):

        headers = {'User_agent': user_agent}
        request = urllib2.Request(url, headers=headers)
        try:
            html = urllib2.urlopen(request).read()
        except urllib2.URLError as e:
            print 'Download error', e.reason
            html = None
            if num_try > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    return download(url, user_agent, num_try - 1)
                elif e.code == 403:
                    return None
        return html

    def get_section_page(self, url):

        html = self.download(url)
        if html == None:
            return None
        soup = BeautifulSoup(html, "html.parser")
        results = soup.find_all(name='script', attrs={'type': 'text/javascript'})
        tt = len(results)
        js = results[tt - 1]
        mm = js.get('src')
        if mm == None:
            result = soup.find_all(name='script', attrs={'language': 'javascript'})
            js1 = result[1]
            mm = js1.get('src')
        html1 = self.download(self.URL + mm)
        List = []
        if html1 :
            list = html1.split(';')
            List = []
            for each in list:
                if 'picAy[' in each:
                    src = each.split('=')
                    List.append(self.picture + src[1][2:-1])
        else:
            return None

        return List

    def download(self,url, user_agent='wswp', num_try=2):

        headers = {'User_agent': user_agent}
        request = urllib2.Request(url, headers=headers)
        try:
            html = urllib2.urlopen(request).read()
        except urllib2.URLError as e:
            print 'Download error', e.reason
            html = None
            if num_try > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    return self.download(url, user_agent, num_try - 1)
                elif e.code == 403:
                    return None
        return html
