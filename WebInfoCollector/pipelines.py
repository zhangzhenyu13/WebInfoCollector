# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
from items import WebPageItem,WebMasterItem,HouseInfoItem

class WebinfocollectorPipeline(object):
    def __init__(self):
        #page info
        self.file1 = codecs.open('mainDistrict.csv', mode='wb', encoding='utf-8')
        self.file2 = codecs.open('Pages.csv', mode='wb', encoding='utf-8')
        #main info
        self.file = codecs.open('result.csv', mode='wb', encoding='utf-8')
        s="urlID,totalPrice,unitPrice,roadplace,subway,floor,useyear,"+\
            "flaginfo,careNum,watchNUm\n"
        self.file.write(s)
    def process_item(self, item, spider):

        if isinstance(item, WebPageItem):
            print "saving\n", item
            self.file2.write(item["urlName"] + ":" + item["url"] + "\n")
        elif isinstance(item, WebMasterItem):
            print "saving\n", item
            self.file1.write(item["urlName"] + ":" + item["url"] + "\n")
        elif isinstance(item,HouseInfoItem):
            print "writing",item
            s=item["urlID"]+","+str(item["totalprice"])+","+str(item["unitprice"])+","+item["roadplace"]+\
              ","+item["subway"]+","+item["floor"]+","+item["useyear"]+","+str(item["flag"])+","+\
                str(item["careNum"])+","+str(item["watchNum"])+"\n"
            self.file.write(s)
            pass

        else:
            print "Wrong type!!!"
            exit(-2)

