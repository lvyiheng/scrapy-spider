# -*- coding: utf-8 -*-
from scrapy import Request,Spider
from meitu.items import MeituItem
import re
class MeitutSpider(Spider):
    name = 'meitut'
    allowed_domains = ['meitu.com']
    url = "http://www.meituba.com/xinggan/list81.html"
    def start_requests(self):
        yield Request(self.url,callback = self.get_list)
    def get_list(self,response):
        lilist = response.xpath('//div[@class="box_left3"]/div[@class="channel_picbox"]/div[@class="channel_list"]/ul/li')
        for li in lilist:
            nurl = li.xpath('./a/@href').extract_first()
            print(type(nurl))
            yield Request(nurl,callback=self.parse_list,dont_filter=True)
        
        
    def parse_list(self, response):
        
        yield Request(response.url,callback=self.parse,dont_filter=True)
        page = response.xpath('//div[@class="pages"]/ul/li[1]/a/text()').extract_first()
        page=re.findall("(\d+)",page)[0]    
        for page in range(2,int(page)+1):
            src = list(response.url)
            src[-5:-6]="_{}".format(page)
            self.a= "".join(src)
            yield Request(self.a,callback=self.parse,dont_filter=True)

    def parse(self,response):
        print(response)
        item = MeituItem()
        if not response.xpath('//div[@class="photo"]/a/img/@src'):
            pass
        
        else:
            src = response.xpath('//div[@class="photo"]/a/img/@src').extract_first()
            item['src'] = src.strip()
            yield item
            
            
            
            
            
            
            
            