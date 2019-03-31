import scrapy
from scrapy import Spider,Request
from bs4 import BeautifulSoup
from android_bus.items import ArticleItem
class androidbus_spider(scrapy.Spider):
    name="androidbus"
    allowed_domains = ['www.apkbus.com']
    start_urls = 'http://www.apkbus.com/plugin.php?id=cxy_common_blog&sort=2&cat_id=0&page=1'
    base_url='http://www.apkbus.com/'
    def start_requests(self):
        yield Request(self.start_urls,callback=self.parse_blog)


    def parse_blog(self,response):
        soup = BeautifulSoup(response.text,'lxml')
        for item in soup.find_all("div",class_="row"):
            if item is None:
                break
            article = ArticleItem()
            item_a= item.find("a")
            article['link'] = self.base_url+ item_a.get('href')
            article['title'] = item_a.find('h2').string
            description = item.find("div",class_="preview")
            if not description is None:
                article['description'] = description.string
            article['author'] =item.find("span").string
            article['time'] = item.find("span",style="color:#a8a8a8;").string
            yield article
        nextLink = self.base_url+soup.find("a",class_="nxt").get('href')
        if not nextLink is None:
            print("nextLink is "+nextLink)
            yield Request(nextLink,callback=self.parse_blog)


            
        
