# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
class MyprojectPipeline(object):
    def __init__(self):
      self.nun =0

    def process_item(self, item, spider):
      title = item['title'].encode("utf-8")
      title = title.rstrip()
      filename = open(r'/home/ubuntu/project/xs/xs/'+title + '.text','w')
      print ('filename===>>>'+str(filename))  
      content= item['content'].encode("utf-8")
      filename.write(content)
      self.nun=self.nun+1
      return item

#    def close_spider(self, spider):
#        self.filename.close()
