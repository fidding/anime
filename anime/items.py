# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnimeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 图片标题
    title = scrapy.Field()

    # 图片
    picUrl = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    # 缩略图
    thumbUrl = scrapy.Field()
    thumbHeight = scrapy.Field()
    thumbWidth = scrapy.Field()
    # 标签
    tag = scrapy.Field()
    # 目录类别
    catalog = scrapy.Field()
    pass
