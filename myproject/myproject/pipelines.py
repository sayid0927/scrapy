# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

import MySQLdb
from twisted.enterprise import adbapi


def _conditional_insert(tx, item):
    sql = "insert into jsbooks(author,title,url,pubday,comments,likes,rewards,views) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    params = (item['author'], item['title'], item['url'], item['pubday'], item['comments'], item['likes'],
              item['rewards'], item['reads'])
    tx.execute(sql, params)


def handle_error(failue, item, spider):
    print
    failue


class MyprojectPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        self.nun = 0

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        title = item['title'].encode("utf-8")
        title = title.rstrip()
        filename = open(r'/home/ubuntu/project/xs/xs/' + title + '.text', 'w')
        print('filename===>>>' + str(filename))
        content = item['content'].encode("utf-8")
        filename.write(content)
        query = self.dbpool.runInteraction(_conditional_insert, item)
        query.addErrback(self._handle_error, item, spider)
        self.nun = self.nun + 1
        return item

# def close_spider(self, spider):
#        self.filename.close()
