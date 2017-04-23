# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class WebMasterItem(scrapy.Item):
    urlName=scrapy.Field()
    url=scrapy.Field()
class WebPageItem(scrapy.Item):
    urlName=scrapy.Field()
    url=scrapy.Field()
class HouseInfoItem(scrapy.Item):
    urlID=scrapy.Field()
    totalprice=scrapy.Field()
    unitprice=scrapy.Field()
    roadplace=scrapy.Field()
    subway=scrapy.Field()
    floor=scrapy.Field()
    useyear=scrapy.Field()
    #numeric statics
    picNum=scrapy.Field()
    flag=scrapy.Field()
    careNum = scrapy.Field()
    watchNum = scrapy.Field()
