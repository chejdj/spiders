import scrapy


class CambridgeImageSpider(scrapy.Spider):
    name = 'cambridge_image'
    allowed_domains = ['dictionary.cambridge.org']
    start_urls = ['http://dictionary.cambridge.org/']

    def parse(self, response):
        pass
