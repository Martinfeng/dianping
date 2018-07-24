# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    star = scrapy.Field()
    review_num = scrapy.Field()
    avgprice = scrapy.Field()
    shop_tag = scrapy.Field()
    circle = scrapy.Field()
    addr = scrapy.Field()
    link = scrapy.Field()
    score_list = scrapy.Field()
    coord = scrapy.Field()
    tele = scrapy.Field()
    pass
