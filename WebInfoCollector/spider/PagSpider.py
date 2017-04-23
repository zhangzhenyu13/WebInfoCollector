from scrapy import spiders
from scrapy import Selector
from scrapy import Request
from WebInfoCollector.items import WebPageItem,WebMasterItem
class WebSpider(spiders.Spider):
    name="pageinfo"
    download_delay = 0
    allowed_domains=["lianjia.com"]
    start_urls=["http://bj.lianjia.com/ershoufang/"]
    def parse_Url(self,response):
        sel=Selector(response)
        sites=sel.xpath('/html/body/div[3]/div[1]/dl[2]/dd/div[1]/div[2]/a')
        print "size of sub entries={}".format(len(sites))
        if len(sites)==0:
            print "Server ban!!!"
            return
        for site in sites:
            neighbor=site.xpath('text()').extract()
            url=site.xpath('@href').extract()
            urls = WebPageItem()
            try:
                urls["urlName"]=neighbor[0]
                urls["url"]="http://bj.lianjia.com"+url[0]
            except: exit(-1)
            yield urls
    def parse(self,response):

        sel = Selector(response)
        sites=sel.xpath('/html/body/div[3]/div[1]/dl[2]/dd/div[1]/div/a')
        print "size of entries={}".format(len(sites))
        if len(sites)==0:
            print "Server ban!!!"
            return
        for site in sites:
            disctrict=site.xpath('text()').extract()[0]
            siteUrl = "http://bj.lianjia.com"+site.xpath("@href").extract()[0]
            mainUrls=WebMasterItem()
            mainUrls["urlName"]=disctrict
            mainUrls["url"]=siteUrl
            yield mainUrls
            yield Request(siteUrl,self.parse_Url)
