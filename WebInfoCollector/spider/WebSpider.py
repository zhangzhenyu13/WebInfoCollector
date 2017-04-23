from scrapy import spiders
from scrapy import Selector
from scrapy import Request
import codecs
import random
from WebInfoCollector.items import HouseInfoItem
class WebSpider(spiders.Spider):
    name="houseinfo"
    download_delay = 0
    maxPageNum=100
    allowed_domains=["lianjia.com"]
    start_urls=[]
    def setDelay(self):
        random.seed()
        self.download_delay=random.randint(0,1)
    def __init__(self):
        f=codecs.open('saved/Pages.csv', mode='rb', encoding='utf-8')
        count=0
        for line in f.readlines():
            s=line.split(",")
            print "adding",line
            print s[1]
            LenS=len(s[1])-1
            url=s[1]
            url=url[0:LenS]
            self.start_urls.append(url)
            count=count+1
            if(count>1000):
                break
            pass
        f.close()
#req method1
    def parse_subPage(self,response):
        print "in sub page",response.url
        sel = Selector(response)
        #price
        price={}
        price["totalprice"]=sel.xpath('/html/body/div[5]/div[2]/div[2]/span[1]/text()').extract()
        price["unitprice"]=sel.xpath('/html/body/div[5]/div[2]/div[2]/div[1]/div[1]/span/text()').extract()
        #place
        place={}
        place["roadlabel"]=sel.xpath('/html/body/div[5]/div[2]/div[4]/div[2]/span[2]/text()[2]').extract()
        place["subway"]=sel.xpath('/html/body/div[5]/div[2]/div[4]/div[2]/a/text()').extract()
        #
        floor=sel.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[2]/text()').extract()
        useY=sel.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[5]/text()').extract()
        #flag info
        flaginfos=sel.xpath('/html/body/div[7]/div[1]/div[2]/div/div[@class="baseattribute clear"]')
        flags=0
        for flag in flaginfos[1:]:
            s=flag.xpath('div[2]/text()').extract()
            flags=flags+len(s[0])
        #gather info

        item=HouseInfoItem()
        item["urlID"]=response.url
        item["totalprice"]=eval(price["totalprice"][0])
        item["unitprice"]=eval(price["unitprice"][0])
        if place["roadlabel"] is not None and len(place["roadlabel"])>0:
            if len((place["roadlabel"][0]).strip())<1:
                item["roadplace"] ='100'
            else:
                item["roadplace"] =place["roadlabel"][0]
        else:
            item["roadplace"] ='100'
        if place["subway"] is not None and len(place["subway"])>0:
            item["subway"]="1"
        else:
            item["subway"]="0"
        item["floor"]=floor[0][0:3]
        item["useyear"]=useY[0]
        item["picNum"]=len(sel.xpath('//*[@id="thumbnail2"]/ul/li'))
        item["flag"]=flags
        item["careNum"] = eval(sel.xpath('//*[@id="favCount"]/text()').extract()[0])
        item["watchNum"] = eval(sel.xpath('//*[@id="cartCount"]/text()').extract()[0])
        self.setDelay()
        yield item
        pass
#req nextPage
    def parse_next(self,response):
        pass
#main method for req queue
    def parse(self,response):
        pageNum=1
        url=response.url
        url=url[0:len(url)-1]
        pos = url.rfind('/')
        matchstr=url[pos+1:]
        if matchstr.find("pg")==0:
            pageNum = eval(url[pos + 1 + 2:])
            url=url[0:pos+1]

        else:
            url=url+"/"
        #get the list of the items
        sel = Selector(response)
        sites = sel.xpath('//li[@class="clear"]/div[@class="info clear"]')
        print "size of items = {}".format(len(sites))
        if len(sites)==0:
            print "Server ban!!!"
            return
        #handle the items
        limitN=30
        print
        i=0
        webID=''
        for site in sites:
            if i> limitN:
                break

            i=i+1
            siteUrl = site.xpath("div[1]/a/@href").extract()
            yield Request(siteUrl[0],self.parse_subPage)
            if i==1:
                webID=siteUrl[0]
                try:
                    if response.meta["pageID"]==webID:
                        print "Same Page Visited!!!"
                        return
                except:
                    print "Compare Error cause by 1st None Para!!!"

            pass
        #req for next page
        pageNum = pageNum + 1
        next_page_url = url +"pg"+ str(pageNum)+"/"
        if pageNum <= self.maxPageNum:
            print "nextPage", next_page_url
            self.setDelay()
            yield Request(url=next_page_url,meta={"pageID":webID},callback=self.parse)
            pass
        else:
            print "maxLimitPageNum="+str(self.maxPageNum)
            return
