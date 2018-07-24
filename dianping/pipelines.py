# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo


class DianpingPipeline(object):
    def process_item(self, item, spider):
        print(item.values())
        with open("dianping_canyin.txt", "a") as outfile:
            outfile.write('|'.join([x.encode('gbk') for x in item.values()]) + '\n')
        return item

# class DianpingPipeline(object):
#     def process_item(self, item, spider):
#         print(item.values())
#         with open("dianping_canyin.txt", "a") as outfile:
#             outfile.write('|'.join([x for x in item.values()]) + '\n')
#         return item

class DianpingMongoPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        Info = dict(item)
        self.post.insert(Info)
        return item
