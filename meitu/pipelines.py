 # -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
class ImagePipeline(ImagesPipeline):
    def file_path(self,request,response=None,info=None):
        file_name = str(time.time())+".jpg"
        print(file_name)
        return file_name
    def item_completed(self,results,item,info):
        image_paths = [x['path'] for ok ,x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item
    def get_media_requests(self, item, info):

            
        yield Request(item['src'])
    
#    pass
#        
    
import pymongo       
class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
                mongo_uri = crawler.settings.get('MONGO_URI'),
                mongo_db = crawler.settings.get('MONGO_DB')
                )
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    def process_item(self,item,spider):
        self.db[item.collection].insert(dict(item))
        return item
    def close_spider(self,spider):
        self.client.close()
            