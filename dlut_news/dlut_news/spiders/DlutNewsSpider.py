import scrapy
import json
import re
from scrapy import Spider,Request
from bs4 import BeautifulSoup
from dlut_news.items import NewsItem

class DlutNewsSpider(scrapy.Spider):
    name="dlut_news"
    allowed_domains = ["http://ssdut.dlut.edu.cn"]
    base_news_url="http://ssdut.dlut.edu.cn/index/bkstz/"
    news_url="http://ssdut.dlut.edu.cn/index/bkstz.htm"
    def start_requests(self):
        yield Request(self.news_url,callback=self.parse_news)

    def parse_news(self,response):
        soup = BeautifulSoup(response.text,'lxml')
        for li in soup.find_all(id=re.compile("^lineu")):
            item = NewsItem()
            li=li.find("a")
            print(li)
            for field in item.fields:
                data = li.get(field)
                if field == 'href':
                    data=data.replace("..",self.allowed_domains[0])
                item[field]=data
            yield item
        nextLink =soup.find(attrs={'class':'Next'})
        print(nextLink)
        if not nextLink is None:
            link =nextLink.get('href')
            link=link.strip("bkstz/")
            print(link)
            yield Request(self.base_news_url+link,callback=self.parse_news,dont_filter=True)


