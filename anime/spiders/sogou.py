# -*- coding: utf-8 -*-
import scrapy
import json
from anime.items import AnimeItem
from anime.helpers import getUrlOfSogou


class SogouSpider(scrapy.Spider):
    name = 'sogou'
    page = 1
    # https://pic.sogou.com/pics?query=高清动漫&start=1&reqType=ajax
    # 目录类别
    imgCatalog = ['高清动漫', '火影忍者', '海贼王']
    catalogIndex = 0
    start_urls = [getUrlOfSogou(imgCatalog[catalogIndex], page)]

    def parse(self, response):
        # 结构化数据
        jsonresponse = json.loads(response.body_as_unicode())
        number = jsonresponse['itemsOnPage']
        items = jsonresponse['items']
        catalogName = self.imgCatalog[self.catalogIndex]
        # 获取数据
        for item in items:
            picItem = AnimeItem()
            picItem['title'] = item['title']
            picItem['picUrl'] = item['pic_url']
            picItem['width'] = item['width']
            picItem['height'] = item['height']
            picItem['thumbUrl'] = item['thumbUrl']
            picItem['thumbWidth'] = item['thumb_width']
            picItem['thumbHeight'] = item['thumb_height']
            picItem['tag'] = item['title']
            picItem['catalog'] = catalogName
            yield picItem

        # 递归
        if self.catalogIndex <= len(self.imgCatalog) - 1:
            # 已爬完
            if number == 0 and self.catalogIndex == len(self.imgCatalog) - 1:
                return picItem

            # 当前目录已爬完,切换目录
            if number == 0:
                self.catalogIndex += 1
                self.page = 1

            # 递归
            self.page = int(self.page) + int(number)
            yield scrapy.Request(
                getUrlOfSogou(catalogName, self.page),
                method='GET',
                callback=self.parse
            )
