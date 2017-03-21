import scrapy
from tutorial.items import DmozItem
import urllib
import os   
import threading 
import time
import Queue
que = Queue.Queue()
threadlock = threading.Lock()
threads = []
n = 0
class mythread(threading.Thread):
    def __init__(self,que):
        threading.Thread.__init__(self) 
        self.que = que
        
    def run(self):
        global title,link,n
        conter = 0
        urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
        if threadlock.acquire():
            while conter <= 14:
                if link[n].startswith('/d/file/'):
                    link[n] = 'http://www.xiaohuar.com' + link[n]
                file_name = '%s.jpg'%(title[n])
                file_path = os.path.join('D:\\python\\tutorial\\test',file_name)
                urllib.urlretrieve(link[n],file_path)
                conter += 1
                n += 1
        threadlock.release()
        
class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.xiaohuar.com/2014.html"
        
    ]  

    def parse(self, response):
        global link,title
        res = []
        link = response.xpath('//a[@target="_blank"]//img[@width="210"]/@src').extract()
        title = response.xpath('//a[@target="_blank"]//img[@width="210"]/@alt').extract()
        for i in range(8):
            t = mythread(que)
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
