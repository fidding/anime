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
    imgCatalog = ['高清动漫', '火影忍者', '海贼王', '死神', '棋魂',
                  '钢之炼金术士', '犬夜叉', '网球王子', '全职猎人',
                  '名侦探柯南', '新世纪福音战士', '斩赤红之瞳', '灌篮高手',
                  '金色琴弦', '机动战士高达', '哆啦A梦', '浪客剑心',
                  '超时空要塞', '死神', '乱马二分之一', '美少女战士',
                  '反叛的鲁鲁修', '死亡笔记', '城市猎人', '银魂',
                  '家庭教师', '魔卡少女樱']
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
