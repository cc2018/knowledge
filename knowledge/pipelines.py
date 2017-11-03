# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from pymongo import IndexModel, ASCENDING
from knowledge.items import CommonItem
import codecs

class MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient("localhost", 27017)
        db = client.knowledge
        self.doc = db.knowledge
        idx = IndexModel([('url', ASCENDING)], unique=True)
        self.doc.create_indexes([idx])
        # if your existing DB has duplicate records, refer to:
        # https://stackoverflow.com/questions/35707496/remove-duplicate-in-mongodb/35711737

    def process_item(self, item, spider):
        if isinstance(item, CommonItem):
            try:
                self.doc.update_one({'url': item['url']}, {'$set': dict(item)}, upsert=True)
            except Exception:
                pass
        return item

class FilePipelin(object):
    def __init__(self):
        self.root_dir = '/Users/caojian02/pro/knowledge/output/'
        self.files = {}

    def process_item(self, item, spider):
        if isinstance(item, CommonItem):
            file = None
            file_name = str(item['desc'])
            if file_name in self.files:
                file = self.files[file_name]
            else:
                path = self.root_dir + file_name
                file = codecs.open(self.root_dir + file_name + '.txt', 'w', encoding='utf-8')
                #file = open(self.root_dir + file_name + '.txt')
                self.files[file_name] = file

            if file is not None:
                file.write(item['title'])
                file.write('\n')
                file.write(item['content'])
                file.write('\n')
        return item

    def close(self):
        self.file.close()
