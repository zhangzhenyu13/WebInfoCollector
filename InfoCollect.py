from scrapy import cmdline
import os
import shutil
path="saved"
pages="Pages.csv"
r="resut.csv"
mainPage="mainDistrict.csv"
if os.path.exists(path)==False:
    os.mkdir(path)

choice=(input("1/2?\n"))
if choice in [1,2]:
    print "after finished ,move *.csv to  dir 'saved'"
if(choice==1):
    print "crawl for Pages Urls"
    cmdline.execute("scrapy crawl pageinfo".split())
elif choice==2:
    print "crawl for houseInfo"
    cmdline.execute("scrapy crawl houseinfo".split())

