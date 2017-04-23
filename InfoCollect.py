from scrapy import cmdline
import os
import shutil
path="saved"
pages="Pages.csv"
r="resut.csv"
mainPage="mainDistrict.csv"
if os.path.exists(path)==False:
    os.mkdir(path)
print "crawl for houseInfo"
cmdline.execute("scrapy crawl houseinfo".split())

