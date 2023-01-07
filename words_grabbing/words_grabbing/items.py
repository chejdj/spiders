# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WordsGrabbingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    headword = scrapy.Field()
    pos = scrapy.Field()
    level = scrapy.Field()
    english_trans = scrapy.Field()
    chinese_trans = scrapy.Field()
    # sentences = scrapy.Field()
    pos_detail = scrapy.Field()
